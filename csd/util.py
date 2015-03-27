from __future__ import unicode_literals, print_function, absolute_import, division
import re

from clld.interfaces import IRepresentation
from clld.db.meta import DBSession
from clld.db.models.common import Language, Parameter
from clld.web.util.helpers import link, button, icon
from clld.web.util.htmllib import HTML, literal
from clld.web.adapters import get_adapter


META_LANG_PATTERN = re.compile('\{(?P<word>[^\}]+)\}')


def markup_form(s):
    if not s:
        return s
    parts = []
    pos = 0
    for match in META_LANG_PATTERN.finditer(s):
        parts.append(HTML.i(s[pos:match.start()]))
        parts.append(match.group('word') + ':')
        pos = match.end()
    parts.append(HTML.i(s[pos:]))
    return HTML.span(*parts)


def markup_italic(s):
    def bar_split(p):
        return [HTML.i(pp) if j % 2 else pp for j, pp in enumerate(p.split('|'))]

    if not s:
        return s
    parts = []
    pos = 0
    for match in META_LANG_PATTERN.finditer(s):
        parts.extend(bar_split(s[pos:match.start()]))
        parts.append(HTML.i(match.group('word')))
        pos = match.end()
    parts.extend(bar_split(s[pos:]))
    return HTML.span(*parts)


def comment_button(req, obj, class_=''):
    return HTML.form(
        button(icon('comment'), type='submit', class_=class_, title='comment'),
        class_='inline',
        method='POST',
        action=req.route_url('comment', type=obj.__class__.__name__, id=obj.id))


def parameter_detail_html(request=None, context=None, **kw):
    return {
        #'languages': {l.id.upper(): l for l in DBSession.query(Language)},
        'dict_entry': get_adapter(IRepresentation, context, request, ext='snippet.html'),
    }


def insert_links(req, s):
    def repl(m):
        try:
            int(m.group('id'))
            cls = Parameter
        except:
            cls = Language
        obj = cls.get(m.group('id').lower(), default=None)
        if obj:
            return link(req, cls.get(m.group('id').lower()))
        return '---%s---' % m.group('id')

    return markup_italic(literal(re.sub('\*\*(?P<id>[A-Z0-9]+)\*\*', repl, s)))
