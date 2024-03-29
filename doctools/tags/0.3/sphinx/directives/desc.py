# -*- coding: utf-8 -*-
"""
    sphinx.directives.desc
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2007-2008 by Georg Brandl.
    :license: BSD.
"""

import re
import string

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes


ws_re = re.compile(r'\s+')

# ------ information units ---------------------------------------------------------

def desc_index_text(desctype, currmodule, name):
    if desctype == 'function':
        if not currmodule:
            return '%s() (built-in function)' % name
        return '%s() (in module %s)' % (name, currmodule)
    elif desctype == 'data':
        if not currmodule:
            return '%s (built-in variable)' % name
        return '%s (in module %s)' % (name, currmodule)
    elif desctype == 'class':
        return '%s (class in %s)' % (name, currmodule)
    elif desctype == 'exception':
        return name
    elif desctype == 'method':
        try:
            clsname, methname = name.rsplit('.', 1)
        except ValueError:
            if currmodule:
                return '%s() (in module %s)' % (name, currmodule)
            else:
                return '%s()' % name
        if currmodule:
            return '%s() (%s.%s method)' % (methname, currmodule, clsname)
        else:
            return '%s() (%s method)' % (methname, clsname)
    elif desctype == 'attribute':
        try:
            clsname, attrname = name.rsplit('.', 1)
        except ValueError:
            if currmodule:
                return '%s (in module %s)' % (name, currmodule)
            else:
                return name
        if currmodule:
            return '%s (%s.%s attribute)' % (attrname, currmodule, clsname)
        else:
            return '%s (%s attribute)' % (attrname, clsname)
    elif desctype == 'opcode':
        return '%s (opcode)' % name
    elif desctype == 'cfunction':
        return '%s (C function)' % name
    elif desctype == 'cmember':
        return '%s (C member)' % name
    elif desctype == 'cmacro':
        return '%s (C macro)' % name
    elif desctype == 'ctype':
        return '%s (C type)' % name
    elif desctype == 'cvar':
        return '%s (C variable)' % name
    else:
        raise ValueError("unhandled descenv: %s" % desctype)


# ------ functions to parse a Python or C signature and create desc_* nodes.

py_sig_re = re.compile(r'''^([\w.]*\.)?        # class names
                           (\w+)  \s*          # thing name
                           (?: \((.*)\) )? $   # optionally arguments
                        ''', re.VERBOSE)

py_paramlist_re = re.compile(r'([\[\],])')  # split at '[', ']' and ','

def parse_py_signature(signode, sig, desctype, env):
    """
    Transform a python signature into RST nodes.
    Return (fully qualified name of the thing, classname if any).

    If inside a class, the current class name is handled intelligently:
    * it is stripped from the displayed name if present
    * it is added to the full name (return value) if not present
    """
    m = py_sig_re.match(sig)
    if m is None:
        raise ValueError
    classname, name, arglist = m.groups()

    add_module = True
    if env.currclass:
        if classname and classname.startswith(env.currclass):
            fullname = classname + name
            # class name is given again in the signature
            classname = classname[len(env.currclass):].lstrip('.')
            add_module = False
        elif classname:
            # class name is given in the signature, but different
            fullname = env.currclass + '.' + classname + name
        else:
            # class name is not given in the signature
            fullname = env.currclass + '.' + name
            add_module = False
    else:
        fullname = classname and classname + name or name

    if classname:
        signode += addnodes.desc_classname(classname, classname)
    # exceptions are a special case, since they are documented in the
    # 'exceptions' module.
    elif add_module and env.config.add_module_names and \
           env.currmodule and env.currmodule != 'exceptions':
        nodetext = env.currmodule + '.'
        signode += addnodes.desc_classname(nodetext, nodetext)

    signode += addnodes.desc_name(name, name)
    if not arglist:
        if desctype in ('function', 'method'):
            # for callables, add an empty parameter list
            signode += addnodes.desc_parameterlist()
        return fullname, classname
    signode += addnodes.desc_parameterlist()

    stack = [signode[-1]]
    for token in py_paramlist_re.split(arglist):
        if token == '[':
            opt = addnodes.desc_optional()
            stack[-1] += opt
            stack.append(opt)
        elif token == ']':
            try:
                stack.pop()
            except IndexError:
                raise ValueError
        elif not token or token == ',' or token.isspace():
            pass
        else:
            token = token.strip()
            stack[-1] += addnodes.desc_parameter(token, token)
    if len(stack) != 1:
        raise ValueError
    return fullname, classname


c_sig_re = re.compile(
    r'''^([^(]*?)          # return type
        ([\w:]+)  \s*      # thing name (colon allowed for C++ class names)
        (?: \((.*)\) )?    # optionally arguments
        (\s+const)? $      # const specifier
    ''', re.VERBOSE)
c_funcptr_sig_re = re.compile(
    r'''^([^(]+?)          # return type
        (\( [^()]+ \)) \s* # name in parentheses
        \( (.*) \)         # arguments
        (\s+const)? $      # const specifier
    ''', re.VERBOSE)
c_funcptr_name_re = re.compile(r'^\(\s*\*\s*(.*?)\s*\)$')

# RE to split at word boundaries
wsplit_re = re.compile(r'(\W+)')

# These C types aren't described in the reference, so don't try to create
# a cross-reference to them
stopwords = set(('const', 'void', 'char', 'int', 'long', 'FILE', 'struct'))

def parse_c_type(node, ctype):
    # add cross-ref nodes for all words
    for part in filter(None, wsplit_re.split(ctype)):
        tnode = nodes.Text(part, part)
        if part[0] in string.letters+'_' and part not in stopwords:
            pnode = addnodes.pending_xref(
                '', reftype='ctype', reftarget=part, modname=None, classname=None)
            pnode += tnode
            node += pnode
        else:
            node += tnode

def parse_c_signature(signode, sig, desctype):
    """Transform a C (or C++) signature into RST nodes."""
    # first try the function pointer signature regex, it's more specific
    m = c_funcptr_sig_re.match(sig)
    if m is None:
        m = c_sig_re.match(sig)
    if m is None:
        raise ValueError('no match')
    rettype, name, arglist, const = m.groups()

    signode += addnodes.desc_type("", "")
    parse_c_type(signode[-1], rettype)
    try:
        classname, funcname = name.split('::', 1)
        classname += '::'
        signode += addnodes.desc_classname(classname, classname)
        signode += addnodes.desc_name(funcname, funcname)
        # name (the full name) is still both parts
    except ValueError:
        signode += addnodes.desc_name(name, name)
    # clean up parentheses from canonical name
    m = c_funcptr_name_re.match(name)
    if m:
        name = m.group(1)
    if not arglist:
        if desctype == 'cfunction':
            # for functions, add an empty parameter list
            signode += addnodes.desc_parameterlist()
        return name

    paramlist = addnodes.desc_parameterlist()
    arglist = arglist.replace('`', '').replace('\\ ', '') # remove markup
    # this messes up function pointer types, but not too badly ;)
    args = arglist.split(',')
    for arg in args:
        arg = arg.strip()
        param = addnodes.desc_parameter('', '', noemph=True)
        try:
            ctype, argname = arg.rsplit(' ', 1)
        except ValueError:
            # no argument name given, only the type
            parse_c_type(param, arg)
        else:
            parse_c_type(param, ctype)
            param += nodes.emphasis(' '+argname, ' '+argname)
        paramlist += param
    signode += paramlist
    if const:
        signode += addnodes.desc_classname(const, const)
    return name


opcode_sig_re = re.compile(r'(\w+(?:\+\d)?)\s*\((.*)\)')

def parse_opcode_signature(signode, sig):
    """Transform an opcode signature into RST nodes."""
    m = opcode_sig_re.match(sig)
    if m is None:
        raise ValueError
    opname, arglist = m.groups()
    signode += addnodes.desc_name(opname, opname)
    paramlist = addnodes.desc_parameterlist()
    signode += paramlist
    paramlist += addnodes.desc_parameter(arglist, arglist)
    return opname.strip()


option_desc_re = re.compile(
    r'(/|-|--)([-_a-zA-Z0-9]+)(\s*.*?)(?=,\s+(?:/|-|--)|$)')

def parse_option_desc(signode, sig):
    """Transform an option description into RST nodes."""
    count = 0
    firstname = ''
    for m in option_desc_re.finditer(sig):
        prefix, optname, args = m.groups()
        if count:
            signode += addnodes.desc_classname(', ', ', ')
        signode += addnodes.desc_name(prefix+optname, prefix+optname)
        signode += addnodes.desc_classname(args, args)
        if not count:
            firstname = optname
        count += 1
    if not firstname:
        raise ValueError
    return firstname


def desc_directive(desctype, arguments, options, content, lineno,
                   content_offset, block_text, state, state_machine):
    env = state.document.settings.env
    node = addnodes.desc()
    node['desctype'] = desctype

    noindex = ('noindex' in options)
    node['noindex'] = noindex
    # remove backslashes to support (dummy) escapes; helps Vim's highlighting
    signatures = map(lambda s: s.strip().replace('\\', ''), arguments[0].split('\n'))
    names = []
    clsname = None
    for i, sig in enumerate(signatures):
        # add a signature node for each signature in the current unit
        # and add a reference target for it
        sig = sig.strip()
        signode = addnodes.desc_signature(sig, '')
        signode['first'] = False
        node.append(signode)
        try:
            if desctype in ('function', 'data', 'class', 'exception',
                            'method', 'attribute'):
                name, clsname = parse_py_signature(signode, sig, desctype, env)
            elif desctype in ('cfunction', 'cmember', 'cmacro', 'ctype', 'cvar'):
                name = parse_c_signature(signode, sig, desctype)
            elif desctype == 'opcode':
                name = parse_opcode_signature(signode, sig)
            elif desctype == 'cmdoption':
                optname = parse_option_desc(signode, sig)
                if not noindex:
                    targetname = 'cmdoption-' + optname
                    signode['ids'].append(targetname)
                    state.document.note_explicit_target(signode)
                    env.note_index_entry('pair', 'command line option; %s' % sig,
                                         targetname, targetname)
                    env.note_reftarget('option', optname, targetname)
                continue
            elif desctype == 'describe':
                signode.clear()
                signode += addnodes.desc_name(sig, sig)
                continue
            else:
                # another registered generic x-ref directive
                rolename, indextemplate, parse_node = additional_xref_types[desctype]
                if parse_node:
                    fullname = parse_node(env, sig, signode)
                else:
                    signode.clear()
                    signode += addnodes.desc_name(sig, sig)
                    # normalize whitespace like xfileref_role does
                    fullname = ws_re.sub('', sig)
                if not noindex:
                    targetname = '%s-%s' % (rolename, fullname)
                    signode['ids'].append(targetname)
                    state.document.note_explicit_target(signode)
                    if indextemplate:
                        indexentry = indextemplate % (fullname,)
                        indextype = 'single'
                        colon = indexentry.find(':')
                        if colon != -1:
                            indextype = indexentry[:colon].strip()
                            indexentry = indexentry[colon+1:].strip()
                        env.note_index_entry(indextype, indexentry,
                                             targetname, targetname)
                    env.note_reftarget(rolename, fullname, targetname)
                # don't use object indexing below
                continue
        except ValueError, err:
            # signature parsing failed
            signode.clear()
            signode += addnodes.desc_name(sig, sig)
            continue             # we don't want an index entry here
        # only add target and index entry if this is the first description of the
        # function name in this desc block
        if not noindex and name not in names:
            fullname = (env.currmodule and env.currmodule + '.' or '') + name
            # note target
            if fullname not in state.document.ids:
                signode['names'].append(fullname)
                signode['ids'].append(fullname)
                signode['first'] = (not names)
                state.document.note_explicit_target(signode)
                env.note_descref(fullname, desctype, lineno)
            names.append(name)

            env.note_index_entry('single',
                                 desc_index_text(desctype, env.currmodule, name),
                                 fullname, fullname)

    subnode = addnodes.desc_content()
    # needed for automatic qualification of members
    clsname_set = False
    if desctype in ('class', 'exception') and names:
        env.currclass = names[0]
        clsname_set = True
    elif desctype in ('method', 'attribute') and clsname and not env.currclass:
        env.currclass = clsname.strip('.')
        clsname_set = True
    # needed for association of version{added,changed} directives
    if names:
        env.currdesc = names[0]
    state.nested_parse(content, content_offset, subnode)
    if clsname_set:
        env.currclass = None
    env.currdesc = None
    node.append(subnode)
    return [node]

desc_directive.content = 1
desc_directive.arguments = (1, 0, 1)
desc_directive.options = {'noindex': directives.flag}

desctypes = [
    # the Python ones
    'function',
    'data',
    'class',
    'method',
    'attribute',
    'exception',
    # the C ones
    'cfunction',
    'cmember',
    'cmacro',
    'ctype',
    'cvar',
    # the odd one
    'opcode',
    # for command line options
    'cmdoption',
    # the generic one
    'describe',
    'envvar',
]

for _name in desctypes:
    directives.register_directive(_name, desc_directive)

# Generic cross-reference types; they can be registered in the application;
# the directives are either desc_directive or target_directive
additional_xref_types = {
    # directive name: (role name, index text, function to parse the desc node)
    'envvar': ('envvar', 'environment variable; %s', None),
}


# ------ target --------------------------------------------------------------------

def target_directive(targettype, arguments, options, content, lineno,
                     content_offset, block_text, state, state_machine):
    """Generic target for user-defined cross-reference types."""
    env = state.document.settings.env
    rolename, indextemplate, _ = additional_xref_types[targettype]
    # normalize whitespace in fullname like xfileref_role does
    fullname = ws_re.sub('', arguments[0].strip())
    targetname = '%s-%s' % (rolename, fullname)
    node = nodes.target('', '', ids=[targetname])
    state.document.note_explicit_target(node)
    if indextemplate:
        indexentry = indextemplate % (fullname,)
        indextype = 'single'
        colon = indexentry.find(':')
        if colon != -1:
            indextype = indexentry[:colon].strip()
            indexentry = indexentry[colon+1:].strip()
        env.note_index_entry(indextype, indexentry, targetname, targetname)
    env.note_reftarget(rolename, fullname, targetname)
    return [node]

target_directive.content = 0
target_directive.arguments = (1, 0, 1)
