from clld.interfaces import IParameter
from clld.web.adapters.geojson import GeoJsonParameter


class GeoJsonEntry(GeoJsonParameter):
    def feature_properties(self, ctx, req, valueset):
        return {
            'values': list(valueset.values),
            'label': ', '.join(v.name for v in valueset.values)}


def includeme(config):
    config.register_adapter(GeoJsonEntry, IParameter)
