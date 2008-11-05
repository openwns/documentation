# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst.directives import admonitions
from sphinx.util.compat import make_admonition

app = None

class todolist(nodes.General, nodes.Element):

    allTodos = []

def addTodo(todo):
    todolist.allTodos.append(todo.deepcopy())

def todo_directive(name, arguments, options, content, lineno,
                   content_offset, block_text, state, state_machine):

    ad = make_admonition(nodes.note, 'todo', arguments, options,
                         content, lineno, content_offset,
                         block_text, state, state_machine)
    ad[0].tagname = 'todo'

    addTodo(ad[0])

    return ad


def todolist_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    return [todolist()]

def process_todolist(app, doctree, docname):

    if app.config['todo']:
        allTodos = []

        allTodos += [orig.deepcopy() for orig in todolist.allTodos]

        for node in doctree.traverse(lambda n: n.tagname == 'todolist'):
            node.replace_self(allTodos)

def process_todo_nodes(app, doctree, docname):

    if not app.config['todo']:
        for node in doctree.traverse(lambda n: n.tagname == 'todo'):
            node.replace_self([])
    else:
        process_todolist(app, doctree, docname)

def setup(application):
    global app
    app = application

    app.add_node(todolist)
    
    # (default, needs fresh doctrees if changed)
    app.add_config_value('todo', False, False)
    app.add_directive('todo', todo_directive, 1, (0, 0, 1))
    app.add_directive('todolist', todolist_directive, 1, (0, 0, 1))
    app.connect('doctree-resolved', process_todo_nodes)
    app.connect('doctree-resolved', process_todolist)
