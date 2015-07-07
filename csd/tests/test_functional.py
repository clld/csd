from path import path

from clld.tests.util import TestWithApp

import csd


class Tests(TestWithApp):
    __cfg__ = path(csd.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get_html('/')
        self.app.get_html('/languages')

    def test_misc(self):
        self.app.get_dt('/values')
        self.app.get_dt('/values?parameter=1204&iSortingCols=2&iSortCol_0=0&sSearch_1=*&iSortCol_1=1')
        self.app.get_dt('/values?language=op')
        self.app.get_html('/sources/marten')
        self.app.get_html('/sources')
        self.app.get_html('/parameters')
        self.app.get_dt('/parameters')
        self.app.get_html('/parameters/14')
        self.app.get_html('/parameters/1178')
        self.app.get_json('/parameters/1178.geojson')
        self.app.get_html('/languages/op.snippet.html?parameter=1201')
