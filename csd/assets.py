from clld.web.assets import environment
from clldutils.path import Path

import csd


environment.append_path(
    Path(csd.__file__).parent.joinpath('static').as_posix(), url='/csd:static/')
environment.load_path = list(reversed(environment.load_path))
