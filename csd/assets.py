from clld.web.assets import environment
from path import path

import csd


environment.append_path(
    path(csd.__file__).dirname().joinpath('static'), url='/csd:static/')
environment.load_path = list(reversed(environment.load_path))
