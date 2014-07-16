from clld.tests.util import TestWithSelenium

import csd


class Tests(TestWithSelenium):
    app = csd.main({}, **{'sqlalchemy.url': 'postgres://robert@/csd'})
