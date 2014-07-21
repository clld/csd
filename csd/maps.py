from clld.web.maps import ParameterMap


class EntryMap(ParameterMap):
    def get_options(self):
        return {'show_labels': True, 'max_zoom': 10}


def includeme(config):
    config.register_map('parameter', EntryMap)