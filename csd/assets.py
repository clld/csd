import pathlib

from clld.web.assets import environment

import csd


environment.append_path(
    str(pathlib.Path(csd.__file__).parent.joinpath('static')), url='/csd:static/')
environment.load_path = list(reversed(environment.load_path))
