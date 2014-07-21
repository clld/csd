from clld.web.app import get_configurator, MapMarker
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
            return req.static_url('csd:static/icons/%s.png' % lang.color)
        return super(CsdMapMarker, self).__call__(ctx, req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = get_configurator('csd', (CsdMapMarker(), IMapMarker), settings=settings)
    config.include('clldmpg')
    config.include('csd.datatables')
    config.include('csd.adapters')
    config.include('csd.maps')
    return config.make_wsgi_app()
