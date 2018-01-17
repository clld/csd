import pytest

pytest_plugins = ['clld']


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/languages'),
        ('get_dt', '/values?iSortingCols=1&iSortCol_0=3&sSearch_3=o'),
        ('get_dt',
         '/values?parameter=1204&iSortingCols=2&iSortCol_0=0&sSearch_1=*&iSortCol_1=1'),
        ('get_dt', '/values?language=op'),
        ('get_dt', '/values?language=psi'),
        ('get_html', '/valuesets/ch-828'),
        ('get_html', '/sources/marten'),
        ('get_html', '/sources'),
        ('get_dt', '/sources'),
        ('get_html', '/parameters'),
        ('get_dt', '/parameters?sSearch_2=abstract'),
        ('get_html', '/parameters/14'),
        ('get_html', '/parameters/1178'),
        ('get_html', '/parameters/1178.snippet.html'),
        ('get_json', '/parameters/1178.geojson'),
        ('get_html', '/languages/op.snippet.html?parameter=1201'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
