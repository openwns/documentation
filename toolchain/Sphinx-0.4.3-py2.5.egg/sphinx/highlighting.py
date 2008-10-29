# -*- coding: utf-8 -*-
"""
    sphinx.highlighting
    ~~~~~~~~~~~~~~~~~~~

    Highlight code blocks using Pygments.

    :copyright: 2007-2008 by Georg Brandl.
    :license: BSD.
"""

import sys
import cgi
import re
import parser

from sphinx.util.texescape import tex_hl_escape_map

try:
    import pygments
    from pygments import highlight
    from pygments.lexers import PythonLexer, PythonConsoleLexer, CLexer, \
         TextLexer, RstLexer
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter, LatexFormatter
    from pygments.filters import ErrorToken
    from pygments.style import Style
    from pygments.styles import get_style_by_name
    from pygments.styles.friendly import FriendlyStyle
    from pygments.token import Generic, Comment, Number
except ImportError:
    pygments = None
else:
    class SphinxStyle(Style):
        """
        Like friendly, but a bit darker to enhance contrast on the green
        background.
        """

        background_color = '#eeffcc'
        default_style = ''

        styles = FriendlyStyle.styles
        styles.update({
            Generic.Output: '#333',
            Comment: 'italic #408090',
            Number: '#208050',
        })

    lexers = dict(
        none = TextLexer(),
        python = PythonLexer(),
        pycon = PythonConsoleLexer(),
        rest = RstLexer(),
        c = CLexer(),
    )
    for _lexer in lexers.values():
        _lexer.add_filter('raiseonerror')


escape_hl_chars = {ord(u'@'): u'@at[]',
                   ord(u'['): u'@lb[]',
                   ord(u']'): u'@rb[]'}

# used if Pygments is not available
_LATEX_STYLES = r'''
\newcommand\at{@}
\newcommand\lb{[}
\newcommand\rb{]}
'''


parsing_exceptions = (SyntaxError, UnicodeEncodeError)
if sys.version_info < (2, 5):
    # Python <= 2.4 raises MemoryError when parsing an
    # invalid encoding cookie
    parsing_exceptions += MemoryError,


class PygmentsBridge(object):
    def __init__(self, dest='html', stylename='sphinx'):
        self.dest = dest
        if not pygments:
            return
        if stylename == 'sphinx':
            style = SphinxStyle
        elif '.' in stylename:
            module, stylename = stylename.rsplit('.', 1)
            style = getattr(__import__(module, None, None, ['']), stylename)
        else:
            style = get_style_by_name(stylename)
        self.hfmter = {False: HtmlFormatter(style=style),
                       True: HtmlFormatter(style=style, linenos=True)}
        self.lfmter = {False: LatexFormatter(style=style, commandprefix='PYG'),
                       True: LatexFormatter(style=style, linenos=True,
                                            commandprefix='PYG')}

    def unhighlighted(self, source):
        if self.dest == 'html':
            return '<pre>' + cgi.escape(source) + '</pre>\n'
        else:
            # first, escape highlighting characters like Pygments does
            source = source.translate(escape_hl_chars)
            # then, escape all characters nonrepresentable in LaTeX
            source = source.translate(tex_hl_escape_map)
            return '\\begin{Verbatim}[commandchars=@\\[\\]]\n' + \
                   source + '\\end{Verbatim}\n'

    def highlight_block(self, source, lang, linenos=False):
        if not pygments:
            return self.unhighlighted(source)
        if lang == 'python':
            if source.startswith('>>>'):
                # interactive session
                lexer = lexers['pycon']
            else:
                # maybe Python -- try parsing it
                src = source + '\n'

                # Replace "..." by a mark which is also a valid python expression
                # (Note, the highlighter gets the original source, this is only done
                #  to allow "..." in code and still highlight it as Python code.)
                mark = "__highlighting__ellipsis__"
                src = src.replace("...", mark)

                # lines beginning with "..." are probably placeholders for suite
                src = re.sub(r"(?m)^(\s*)" + mark + "(.)", r"\1"+ mark + r"# \2", src)

                # if we're using 2.5, use the with statement
                if sys.version_info >= (2, 5):
                    src = 'from __future__ import with_statement\n' + src

                if isinstance(src, unicode):
                    # Non-ASCII chars will only occur in string literals
                    # and comments.  If we wanted to give them to the parser
                    # correctly, we'd have to find out the correct source
                    # encoding.  Since it may not even be given in a snippet,
                    # just replace all non-ASCII characters.
                    src = src.encode('ascii', 'replace')
                try:
                    parser.suite(src)
                except parsing_exceptions:
                    return self.unhighlighted(source)
                else:
                    lexer = lexers['python']
        else:
            if lang in lexers:
                lexer = lexers[lang]
            else:
                lexer = lexers[lang] = get_lexer_by_name(lang)
                lexer.add_filter('raiseonerror')
        try:
            if self.dest == 'html':
                return highlight(source, lexer, self.hfmter[bool(linenos)])
            else:
                hlsource = highlight(source, lexer, self.lfmter[bool(linenos)])
                return hlsource.translate(tex_hl_escape_map)
        except ErrorToken:
            # this is most probably not the selected language,
            # so let it pass unhighlighted
            return self.unhighlighted(source)

    def get_stylesheet(self):
        if not pygments:
            if self.dest == 'latex':
                return _LATEX_STYLES
            # no HTML styles needed
            return ''
        fmter = (self.dest == 'html' and self.hfmter or self.lfmter)[0]
        return fmter.get_style_defs()
