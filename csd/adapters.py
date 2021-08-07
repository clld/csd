try:
    from xhtml2pdf import pisa
except ImportError:  # pragma: no cover
    class pisa(object):
        @staticmethod
        def CreatePDF(*args, **kw):
            print("ERROR: xhtml2pdf is not installed!")

from clld.db.meta import DBSession
from clld.db.models.common import Parameter, Dataset, Language, Value
from clld.web.adapters import get_adapter
from clld.interfaces import IRepresentation, ICldfConfig
from clld.interfaces import IParameter
from clld.web.adapters.geojson import GeoJsonParameter
from clld.web.adapters.cldf import CldfConfig
from clld.web.adapters.download import Download
from clld.web.util.helpers import charis_font_spec_css

from csd.util import markup_form


css_tmpl = """
    {0}

    html,body {{
        font-family: 'charissil';
    }}
    @page title_template {{ margin-top: 5cm; }}
    @page regular_template {{
        size: a4 portrait;
        @frame header_frame {{           /* Static Frame */
            -pdf-frame-content: header_content;
            left: 50pt; width: 512pt; top: 50pt; height: 40pt;
        }}
        @frame content_frame {{          /* Content Frame */
            left: 50pt; width: 512pt; top: 90pt; height: 632pt;
        }}
        @frame footer_frame {{           /* Another static Frame */
            -pdf-frame-content: footer_content;
            left: 50pt; width: 512pt; top: 772pt; height: 20pt;
        }}
    }}
    div.title {{ margin-bottom: 5cm; text-align: center; }}
    h1 {{ font-size: 30mm; text-align: center; }}
    h2 {{ -pdf-keep-with-next: true; }}
    h3 {{ -pdf-keep-with-next: true; }}
    p {{ -pdf-keep-with-next: true; }}
    p.separator {{ -pdf-keep-with-next: false; font-size: 6pt; }}
"""

html_tmpl = """
<html><head><style>%s</style></head><body>
    <div id="header_content" style="text-align: center;">%s</div>

    <div id="footer_content" style="text-align: center;">
        <pdf:pagenumber> of <pdf:pagecount>
    </div>
    <pdf:nexttemplate name="title_template" />
    <p>&nbsp;<p>
    <p>&nbsp;<p>
    <p>&nbsp;<p>
    <p>&nbsp;<p>
    <div class="title">
    %s
    </div>
    <pdf:nexttemplate name="regular_template" />
    <pdf:nextpage />
    %s
    </body></html>
"""


class Pdf(Download):  # pragma: no cover
    ext = 'pdf'
    description = "CSD as printable PDF file"

    def asset_spec(self, req):
        return '.'.join(Download.asset_spec(self, req).split('.')[:-1])

    def create(self, req, filename=None, verbose=True):
        html = []
        chars = []
        for entry in DBSession.query(Parameter).order_by(Parameter.name).limit(10000):
            if entry.name[0] not in chars:
                html.append('<h2>%s</h2>' % entry.name[0])
                chars.append(entry.name[0])
            html.append('<h3>%s</h3>' % entry.name)
            adapter = get_adapter(
                IRepresentation, entry, req, ext='snippet.html')
            html.append(adapter.render(entry, req))
            html.append('<p class="separator">&nbsp;<p>')
    
        with open(self.abspath(req).as_posix(), 'wb') as fp:
            pisa.CreatePDF(
                html_tmpl % (
                    css_tmpl.format(charis_font_spec_css()),
                    req.dataset.name,
                    """
<h1 style="font-size: 12mm;">%s</h1>
<blockquote style="font-size: 7mm;">edited by %s</blockquote>""" % (
                    req.dataset.name,
                    req.dataset.formatted_editors()),
                    ''.join(html)),
                dest=fp)


class GeoJsonEntry(GeoJsonParameter):
    def feature_properties(self, ctx, req, valueset):
        return {
            'values': list(valueset.values),
            'label': ', '.join(markup_form(v.name) for v in valueset.values)}


def includeme(config):
    config.register_download(Pdf(Dataset, 'csd'))
    config.register_adapter(GeoJsonEntry, IParameter)
