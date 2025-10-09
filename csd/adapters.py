from clld.db.models.common import Parameter, Dataset, Language, Value
from clld.web.adapters import get_adapter
from clld.interfaces import IRepresentation
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
