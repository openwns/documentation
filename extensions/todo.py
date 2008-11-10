# -*- coding: utf-8 -*-
"""
    sphinx.ext.todo
    ~~~~~~~~~~~~~~~

    Allow todos to be inserted into your documentation. Inclusion
    of todos can be switched of by a configuration variable. The
    todolist directive collects all todos of your project and lists
    them along with a backlink to the original location

    :copyright: 2008 Daniel Bültmann
    :license: BSD.
"""

from docutils import nodes
from docutils.parsers.rst.directives import admonitions
from sphinx.util.compat import make_admonition

class todoNode(nodes.Admonition, nodes.Element): pass

class todolist(nodes.General, nodes.Element): pass

def todo_directive(name, arguments, options, content, lineno,
                   content_offset, block_text, state, state_machine):

    env = state.document.settings.env

    targetid = "todo-%s" % env.index_num
    env.index_num += 1
    targetnode = nodes.target('', '', ids=[targetid])

    ad = make_admonition(todoNode, name, ['Todo'], options,
                         content, lineno, content_offset,
                         block_text, state, state_machine)

    # Attach a list of all todos to the environment
    # The todolist works with the collected todo nodes
    if not hasattr(env, 'all_todos'):
        env.all_todos = []

    todoInfo = {}
    todoInfo['docname'] = env.docname
    todoInfo['lineno'] = lineno
    todoInfo['todo'] = ad[0].deepcopy()
    todoInfo['target'] = targetnode

    env.all_todos.append( todoInfo )

    return [targetnode] + ad 


def process_todo_nodes(app, doctree, fromdocname):

    env = doctree.document.settings.env

    if not app.config['include_todos']:
        for node in doctree.traverse(todoNode):
            
            try:
                node.replace_self([])
            except:
                node.parent.replace(node, [])
            
        env.all_todos = []


def todolist_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    """ Simply insert an empty todolist node which will be replaced later
    when process_todolist is called"""

    p = todolist("")
    return [p]

def process_todolist(app, doctree, fromdocname):
    """ Replace all todolist nodes with a list of the collected
    todos. Augment each todo with a backlink to the original
    location """

    env = doctree.document.settings.env

    for node in doctree.traverse(todolist):

        if not app.config['include_todos']:
            node.replace_self([])
            return

        content = []

        for todoInfo in env.all_todos:
           
            description = "The original entry is located in %s:%d and can be found " % (todoInfo['docname'],
                                                                                        todoInfo['lineno'])
            textnode = nodes.literal(description, description)

            # Create a reference
            newnode = nodes.reference('', '')
            innernode = nodes.emphasis("here", "here")
            newnode['refdocname'] = todoInfo['docname']
            newnode['refuri'] = app.builder.get_relative_uri(fromdocname, todoInfo['docname'])
            newnode['refuri'] += "#" + todoInfo['target']["refid"]
            newnode.append(innernode)

            # Put it in the text
            textnode.append(newnode)

            # Insert into the todolist
            content.append(todoInfo['todo'])
            content.append(textnode)


        node.replace_self(content)

def visit_todoNode(self, node):
    self.visit_admonition(node)

def depart_todoNode(self, node):
    self.depart_admonition(node)

def setup(application):

    application.add_node(todolist)
    application.add_node(todoNode)

    from sphinx.htmlwriter import HTMLTranslator as htranslator
    setattr(htranslator, 'visit_todoNode', visit_todoNode)
    setattr(htranslator, 'depart_todoNode', depart_todoNode)
    
    from sphinx.latexwriter import LaTeXTranslator as ltranslator
    setattr(ltranslator, 'visit_todoNode', visit_todoNode)
    setattr(ltranslator, 'depart_todoNode', depart_todoNode)

    from sphinx.textwriter import TextTranslator as ttranslator
    setattr(ttranslator, 'visit_todoNode', visit_todoNode)
    setattr(ttranslator, 'depart_todoNode', depart_todoNode)

    application.add_config_value('include_todos', False, False)
    application.add_directive('todo', todo_directive, 1, (0, 0, 1))
    application.add_directive('todolist', todolist_directive, 1, (0, 0, 1))
    application.connect('doctree-resolved', process_todolist)
    application.connect('doctree-resolved', process_todo_nodes)
