from __future__ import unicode_literals


def test_markup_italic():
    from csd.util import markup_italic

    assert '%s' % markup_italic('a {b} c |d| e') == '<span>a <i>b</i> c <i>d</i> e</span>'
