from zope.interface import implementer
from six import string_types
import requests

from clld.interfaces import IBlog
from clld.lib import wordpress

from csd.models import Entry, Counterpart


@implementer(IBlog)
class Blog(object):
    def __init__(self, settings, prefix='blog.'):
        if prefix + 'host' in settings:
            self.host = settings[prefix + 'host']
            self.wp = wordpress.Client(
                self.host, settings[prefix + 'user'], settings[prefix + 'password'])
        else:
            self.host, self.wp = None, None

    def url(self, path=None):
        path = path or '/'
        if not path.startswith('/'):
            path = '/' + path
        return '%s%s' % (self.host, path)

    def _set_category(self, **cat):
        return list(self.wp.set_categories([cat]).values())[0]

    @staticmethod
    def slug(obj):
        prefix = 'value' if isinstance(obj, Counterpart) else 'parameter'
        return '{0}-{1.id}/'.format(prefix, obj)

    def _post_url(self, obj):
        try:
            return requests.get(self.url(self.slug(obj)), timeout=1)
        except requests.Timeout:
            return

    def post_url(self, obj, req, create=False):
        res = self._post_url(obj)
        if create and (not res or not self.wp.get_post_id_from_path(None, res=res)):
            # create categories if missing:
            languageCat, entryCat = None, None

            for cat in self.wp.get_categories():
                if cat['name'] == 'Languages':
                    languageCat = cat['id']
                if cat['name'] == 'Entries':
                    entryCat = cat['id']

            # now create the post:
            if isinstance(obj, Counterpart):
                categories = [
                    dict(name=obj.valueset.parameter.name, parent_id=entryCat),
                    dict(name=obj.valueset.language.name, parent_id=languageCat)]
            else:
                categories = [dict(name=obj.name, parent_id=entryCat)]

            prefix = 'Counterpart' if isinstance(obj, Counterpart) else 'Entry'
            self.wp.create_post(
                '%s %s' % (prefix, obj.name),
                'Discuss CSD %s <a href="%s">%s</a>.' % (
                    prefix, req.resource_url(obj), obj.name),
                categories=categories,
                published=True,
                wp_slug=self.slug(obj))
        return res.url

    def feed_url(self, obj, req):
        if isinstance(obj, string_types):
            return self.url(obj)
        res = self._post_url(obj)
        if res:
            return res.url + 'feed'
