from clld.interfaces import IParameter
from clld.web.adapters.geojson import GeoJsonParameter

from csd.util import markup_form


class GeoJsonEntry(GeoJsonParameter):
    def feature_properties(self, ctx, req, valueset):
        return {
            'values': list(valueset.values),
            'label': ', '.join(markup_form(v.name) for v in valueset.values)}


def includeme(config):
    config.register_adapter(GeoJsonEntry, IParameter)
