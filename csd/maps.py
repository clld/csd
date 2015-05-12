from clld.web.maps import ParameterMap, Map


class EntryMap(ParameterMap):
    def get_options(self):
        return {'show_labels': True, 'max_zoom': 10}


class LanguoidsMap(Map):
    def get_options(self):
        return {'show_labels': True, 'max_zoom': 10}


def includeme(config):
    config.register_map('parameter', EntryMap)
    config.register_map('languages', LanguoidsMap)