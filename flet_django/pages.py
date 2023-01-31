from dataclasses import dataclass, field
from abc import abstractmethod
from collections import defaultdict
from importlib import import_module
from typing import Type, Iterable, TypeVar, Callable, Dict, Optional, List

import flet as ft
from flet_core import Control

from django.conf import settings
from .middlewares import GenericMiddleware, urls_middleware, simple_view_middleware
from .navigation import Fatum, Navigare
from .types import PAGE_CLASS


@dataclass
class GenericApp:
    middlewares: list[Type[GenericMiddleware]] = field(default_factory=list)
    urls: Optional[Iterable] = None
    controls: Optional[list[Control]] = None
    destinations: Optional[List[Fatum]] = None
    page_class: Optional[Type[PAGE_CLASS]] = None
    view_params: Optional[dict] = None
    init_route: str = '/'

    def __call__(self, page):
        return self.page_class(app=self, ft_page=page)

    def __post_init__(self):

        engine = import_module(settings.SESSION_ENGINE)
        # pylint: disable=E0116
        # value is a class
        self.SessionStore = engine.SessionStore

        if self.page_class is None:
            self.page_class = GenericPage

        if self.urls is not None:
            self.middlewares.append(urls_middleware(urls=tuple(self.urls)))

        if self.controls is not None:
            self.middlewares.append(simple_view_middleware(controls=self.controls))


@dataclass
class GenericPage:
    app: GenericApp
    ft_page: ft.Page
    navigation: Optional[Navigare] = None
    on_route_change: Optional[Callable[[ft.RouteChangeEvent], None]] = None
    on_view_pop: Optional[Callable[[ft.ViewPopEvent], None]] = None
    __current_route: Optional[str] = None

    def __post_init__(self) -> None:

        if self.app.destinations:
            self.navigation = self.navigation or Navigare(self, self.app.destinations)

        self.session = self.app.SessionStore()
        self.ft_page.on_route_change = self._route_change
        self.ft_page.on_view_pop = self._pop_view

        self.ft_page.views.pop()  # remove empty view from top

        self.route = self.app.init_route

    def _route_change(self, e: ft.RouteChangeEvent) -> None:
        if self.on_route_change is None:
            self.route = e.route
        else:
            self.on_route_change(e)

    def _pop_view(self, e: ft.ViewPopEvent) -> None:
        if self.on_view_pop is None:
            self.pop()
        else:
            self.on_view_pop(e)

    @property
    def route(self):
        return self.__current_route

    def parse_route(self, route: str) -> Callable:
        __middlewares = []
        view = None
        for middleware_class in self.app.middlewares:
            middleware = middleware_class(page=self, route=route)
            __middlewares.append(middleware)
            view = middleware.parse_route()
            if view is not None:
                break
        while len(__middlewares):
            middleware = __middlewares.pop()
            view = middleware.parse_view(view)

        return view

    @route.setter
    def route(self, route: str):
        self.__current_route = route
        view = self.parse_route(route)
        self.append_view(view)
        self.update()

    def append_view(self, view: Callable):
        self.ft_page.views.append(view(self))

    def update(self):
        self.ft_page.update()

    def go(self, route: str):
        self.route = route

    def pop(self) -> None:
        if len(self.ft_page.views) == 1:
            return
        self.ft_page.views.pop()
        top_view = self.ft_page.views[-1]
        self.ft_page.go(top_view.route)
