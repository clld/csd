from __future__ import unicode_literals, print_function, absolute_import, division
import re

from clld.db.meta import DBSession
from clld.db.models.common import Language
from clld.web.util.helpers import link


def parameter_detail_html(request=None, context=None, **kw):
    return {
        'languages': {l.id.upper(): l for l in DBSession.query(Language)},
    }


def insert_language_links(req, s, languages):
    def repl(m):
        return link(req, languages[m.group('id')])

    p = '(?P<id>%s)' % '|'.join(languages.keys())
    return re.sub(p, repl, s)
