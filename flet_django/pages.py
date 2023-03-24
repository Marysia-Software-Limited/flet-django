from dataclasses import dataclass, field
from abc import abstractmethod
from collections import defaultdict
from importlib import import_module
from typing import Type, Iterable, TypeVar, Callable, Dict, Optional, List
from typing import Union

import flet as ft
from flet_core import Control

from django.conf import settings

from .middlewares import GenericMiddleware, urls_middleware, simple_view_middleware
from .navigation import Destiny, Navigare
from .views import GenericViewFactory
from .types import CLIENT_CLASS


@dataclass
class GenericApp:
    middlewares: list[Type[GenericMiddleware]] = field(default_factory=list)
    urls: Optional[Iterable] = None
    controls: Optional[list[Control]] = None
    view: Optional[Callable[[CLIENT_CLASS], ft.View]] = None
    text: Optional[str] = None
    destinations: Optional[List[Destiny]] = None
    client_class: Optional[Type[CLIENT_CLASS]] = None
    view_params: dict = field(default_factory=dict)
    init_route: str = '/'
    view_factory: Callable[
            [CLIENT_CLASS],
            Callable[
                [list[Control], ...],
                ft.View
            ],
        ] = GenericViewFactory

    def __call__(self, page):
        page.scroll = ft.ScrollMode.ALWAYS
        return self.client_class(app=self, page=page)

    def __post_init__(self):

        try:
            engine = import_module(settings.SESSION_ENGINE)
            # pylint: disable=E0116
            # value is a class
            self.SessionStore = engine.SessionStore
        except Exception as _:
            self.SessionStore = lambda: {}

        if self.client_class is None:
            self.client_class = GenericClient

        if self.urls is not None:
            self.middlewares.append(urls_middleware(urls=tuple(self.urls)))

        simple_views_params = [self.controls, self.view, self.text]
        if any(simple_views_params):
            self.middlewares.append(simple_view_middleware(controls=self.controls, view=self.view, text=self.text))


@dataclass
class GenericClient:
    app: GenericApp
    page: ft.Page
    navigation: Optional[Navigare] = None
    on_route_change: Optional[Callable[[ft.RouteChangeEvent], None]] = None
    on_view_pop: Optional[Callable[[ft.ViewPopEvent], None]] = None
    __current_route: Optional[str] = None

    def __post_init__(self) -> None:

        if self.app.destinations:
            self.navigation = self.navigation or Navigare(self, self.app.destinations)

        self.session = self.app.SessionStore()
        self.page.on_route_change = self._route_change
        self.page.on_view_pop = self._pop_view

        self.page.views.pop()  # remove empty view from top

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
    def get_view(self):
        return self.app.view_factory(self, self.app.view_params)

    @property
    def route(self):
        return self.__current_route

    def parse_route(self, route: str) -> Callable:
        __middlewares = []
        if route[0] != '/':  # absolute paths only
            route = f"/{route}"
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

    @property
    def dialog(self) -> Optional[ft.AlertDialog]:
        return self.page.dialog if self.page else None

    @dialog.setter
    def dialog(self, new_dialog: ft.AlertDialog):
        self.page.dialog = new_dialog
        new_dialog.open = True
        self.update()

    def append_view(self, view: Callable):
        view_control = view(self)
        self.page.views.append(view_control)

    def update(self, *controls):
        self.page.update(*controls)

    def go(self, route: str):
        self.route = route

    def pop(self) -> None:
        if len(self.page.views) == 1:
            return
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
