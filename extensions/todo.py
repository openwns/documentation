# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst.directives import admonitions
from sphinx.util.compat import make_admonition

app = None

class todoNode(nodes.Admonition, nodes.Element): pass

class todolist(nodes.General, nodes.Element): pass

from docutils.transforms import TransformError, Transform
class TodoList(Transform):

    default_priority = 710

    def apply(self):
        global app
        allTodos = []        

        if app.config['todo']:

            if not hasattr(self.document.settings.env, "all_todos"):
                return

            for (node, target) in self.document.settings.env.all_todos:
                allTodos += node.deepcopy()
                
            self.startnode.replace_self(allTodos)

def todo_directive(name, arguments, options, content, lineno,
                   content_offset, block_text, state, state_machine):

    env = state.document.settings.env

    import pdb
    pdb.set_trace()

    targetid = "todo-%s" % env.index_num
    env.index_num += 1
    targetnode = nodes.target('', '', ids=[targetid])

    ad = make_admonition(todoNode, name, ['Todo'], options,
                         content, lineno, content_offset,
                         block_text, state, state_machine)
    ad[0].tagname = 'todo'

    if not hasattr(env, 'all_todos'):
        env.all_todos = []

    env.all_todos.append( (ad[0], targetnode) )

    return ad + [targetnode]


def todolist_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):

    p = nodes.pending(TodoList)
    state_machine.document.note_pending(p)
    return [p]

def process_todolist(app, doctree):

    pass

def process_todo_nodes(app, doctree):

    if not app.config['todo']:
        for node in doctree.traverse(lambda n: n.tagname == 'todo'):
            node.replace_self([])
    else:
        process_todolist(app, doctree)

def visit_todoNode(self, node):
    self.visit_admonition(node)

def depart_todoNode(self, node):
    self.depart_admonition(node)

def setup(application):
    global app
    app = application

    app.add_node(todolist)
    app.add_node(todoNode)

    from sphinx.htmlwriter import HTMLTranslator as htranslator
    setattr(htranslator, 'visit_todoNode', visit_todoNode)
    setattr(htranslator, 'depart_todoNode', depart_todoNode)
    
    from sphinx.latexwriter import LaTeXTranslator as ltranslator
    setattr(ltranslator, 'visit_todoNode', visit_todoNode)
    setattr(ltranslator, 'depart_todoNode', depart_todoNode)

    from sphinx.textwriter import TextTranslator as ttranslator
    setattr(ttranslator, 'visit_todoNode', visit_todoNode)
    setattr(ttranslator, 'depart_todoNode', depart_todoNode)

    # (default, needs fresh doctrees if changed)
    app.add_config_value('todo', False, False)
    app.add_directive('todo', todo_directive, 1, (0, 0, 1))
    app.add_directive('todolist', todolist_directive, 1, (0, 0, 1))
    #app.connect('doctree-read', process_todo_nodes)
    #app.connect('doctree-read', process_todolist)
