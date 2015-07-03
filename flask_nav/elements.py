from flask import url_for, request, current_app
from markupsafe import Markup

from . import get_renderer


class NavigationItem(object):
    def render(self, renderer=None, **kwargs):
        return Markup(
            get_renderer(current_app, renderer)(**kwargs).visit(self)
        )


class LinkItem(NavigationItem):
    title = ''

    def get_url(self):
        pass


class View(LinkItem):
    def __init__(self, title, endpoint, *args, **kwargs):
        self.title = title
        self.endpoint = endpoint
        self.url_for_args = args
        self.url_for_kwargs = kwargs

    def get_url(self):
        return url_for(self.endpoint,
                       *self.url_for_args,
                       **self.url_for_kwargs)

    @property
    def active(self):
        # this is a better check because it takes arguments into account
        return request.path == self.get_url()


class TagItem(NavigationItem):
    def __init__(self, title, **attribs):
        self.title = title
        self.attribs = attribs


class Label(NavigationItem):
    def __init__(self, title):
        self.title = title


class Link(TagItem):
    pass


class Separator(NavigationItem):
    pass


class Subgroup(NavigationItem):
    def __init__(self, title, *items):
        self.title = title
        self.items = items


class Navbar(Subgroup):
    id = 'nav_no_id'