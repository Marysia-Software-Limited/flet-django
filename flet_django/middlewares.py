from abc import ABC
from dataclasses import dataclass
from typing import Callable
from typing import Optional

from django.urls import resolve, Resolver404

import flet as ft
from flet_core import Control

from .routes import FtViewRoute
from .types import CLIENT_CLASS


@dataclass
class GenericMiddleware(ABC):
    page: CLIENT_CLASS
    route: str

    def parse_route(self):
        return None

    def parse_view(self, view):
        return view


def simple_view_middleware(
    controls: Optional[list[Control]] = None,
    text: Optional[str] = None,
    view: Optional[Callable[[CLIENT_CLASS], ft.View]] = None,
    **kwargs
):
    if controls is None:
        controls = [ft.Text(text)]
    if view is None:
        def __view(page: CLIENT_CLASS):
            return page.get_view(
                controls=controls,
                **kwargs
            )

        view = __view

    class SimpeViewMiddleware(GenericMiddleware):

        def parse_route(self):
            return view

    return SimpeViewMiddleware


def urls_middleware(urls: tuple):
    class UrlsMiddleware(GenericMiddleware):
        def parse_route(self):
            try:
                result = resolve(self.route, urls)
                return FtViewRoute(
                    control=result.func,
                    name=result.url_name,
                    route=self.route,
                    args=result.args,
                    kwargs=result.kwargs
                )
            except Resolver404:
                return None

    return UrlsMiddleware
