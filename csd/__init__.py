from pyramid.config import Configurator

from clldutils import svg
from clld.web.app import MapMarker
from clld.interfaces import IMapMarker, IValue, IValueSet, ILanguage

# we must make sure custom models are known at database initialization!
from csd import models


_ = lambda s: s
_('Value')
_('Values')
_('Parameter')
_('Parameters')


class CsdMapMarker(MapMarker):
    def __call__(self, ctx, req):
        lang = None
        if IValueSet.providedBy(ctx):
            lang = ctx.language
        elif IValue.providedBy(ctx):
            lang = ctx.valueset.language
        elif ILanguage.providedBy(ctx):
            lang = ctx
        if lang:
            return svg.data_url(svg.icon(('t' if lang.proto else 'c') + lang.color))
        return super(CsdMapMarker, self).__call__(ctx, req)  # pragma: no cover


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.registry.registerUtility(CsdMapMarker(), IMapMarker)
    return config.make_wsgi_app()
