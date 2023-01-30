from abc import ABC
from dataclasses import dataclass

from django.urls import resolve, Resolver404

import flet as ft
from flet_core import Control

from .routes import FtViewRoute
from .views import FtView


@dataclass
class FtMiddleware(ABC):
    page: ABC
    route: str

    def parse_route(self):
        return None

    def parse_view(self, view):
        return view


def simple_view_middleware(
    controls: list[Control] = None,
    text: str = None,
    vertical_alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
):
    if controls is None:
        controls = [ft.Text(text)]

    class SimpeViewMiddleware(FtMiddleware):

        def parse_route(self):
            def view(_):
                return FtView(
                    controls=controls,
                    vertical_alignment=vertical_alignment,
                    horizontal_alignment=horizontal_alignment
                )

            return view

    return SimpeViewMiddleware


def urls_middleware(urls: tuple):
    class UrlsMiddleware(FtMiddleware):
        def parse_route(self):
            try:
                result = resolve(self.route, urls)
                return FtViewRoute(
                    control=result.function,
                    name=result.url_name,
                    route=self.route,
                    args=result.args,
                    kwargs=result.kwargs
                )
            except Resolver404:
                return None

    return UrlsMiddleware
