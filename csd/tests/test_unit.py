from __future__ import unicode_literals
from unittest import TestCase


class Tests(TestCase):
    def test_markup_italic(self):
        from csd.util import markup_italic

        self.assertEquals(
            '%s' % markup_italic('a {b} c |d| e'),
            '<span>a <i>b</i> c <i>d</i> e</span>')
