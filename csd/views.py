from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from csd.models import Counterpart, Entry


@view_config(route_name='comment', request_method='POST')
def comment(request):  # pragma: no cover
    """check whether a blog post for the datapoint does exist.

    if not, create one and redirect there.
    """
    cls = Entry if request.matchdict['type'] == 'Entry' else Counterpart
    obj = cls.get(request.matchdict['id'])
    return HTTPFound(request.blog.post_url(obj, request, create=True))
