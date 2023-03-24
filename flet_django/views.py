from dataclasses import dataclass
from dataclasses import field
from typing import Optional, Type, Callable
from typing import Union

import flet as ft
from flet_core import Control

from flet_django.types import CLIENT_CLASS


def get_app_bar(page, title: str = '', action_params: Optional[dict] = None, **kwargs) -> ft.AppBar:
    action_params = action_params or {}

    new_kwargs = dict(
        title=ft.Text(value=title),
        actions=page.navigation.get_actions(**action_params)
    )
    new_kwargs.update(kwargs)

    return ft.AppBar(**new_kwargs)


@dataclass
class GenericViewFactory:
    client: CLIENT_CLASS
    kwargs: dict = field(default_factory=dict)

    def get_view(self, controls, **kwargs):
        return ft.View(controls=controls, **kwargs)

    def set_nav_bar(self, controls, **nav_bar_params):
        if self.client.navigation:
            nav_bar = self.nav_bar_factory(**nav_bar_params)
            controls.append(nav_bar)
        return controls

    def nav_bar_factory(self, **nav_bar_params) -> ft.NavigationBar:
        return self.client.navigation.get_bar(**nav_bar_params)

    def set_app_bar(self, controls, **app_bar_params):
        if app_bar_params:
            app_bar = self.app_bar_factory(**app_bar_params)
            controls = [app_bar, ] + controls
        return controls

    def app_bar_factory(self, **app_bar_params) -> ft.AppBar:
        return get_app_bar(self.client, **app_bar_params)

    def __call__(self,
                 controls: list[Control],
                 nav_bar_params: Optional[dict] = None,
                 app_bar_params: Optional[dict] = None,
                 **kwargs,
                 ):

        new_kwargs = dict(
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        new_kwargs.update(self.kwargs)
        new_kwargs.update(kwargs)

        nav_bar_params = nav_bar_params or {}
        app_bar_params = app_bar_params or {}
        if 'nav_bar_params' in new_kwargs:
            current_nav_bar_params = nav_bar_params
            nav_bar_params = new_kwargs.pop('nav_bar_params')
            nav_bar_params.update(current_nav_bar_params)

        if 'app_bar_params' in self.kwargs:
            current_app_bar_params = app_bar_params
            app_bar_params = new_kwargs.pop('app_bar_params')
            app_bar_params.update(current_app_bar_params)

        view = self.get_view(controls=controls, **new_kwargs)
        view.controls = self.set_nav_bar(view.controls, **nav_bar_params)
        view.controls = self.set_app_bar(view.controls, **app_bar_params)

        return view


#################################################
#                   OLD CODE                    #
#################################################


def ft_view(
    page: CLIENT_CLASS,
    controls: list[Control],
    nav_bar_params: Optional[dict] = None,
    app_bar_params: Optional[dict] = None,
    app_bar_factory: Callable = get_app_bar,
    **kwargs,
):
    new_kwargs = dict(
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    if page.app.view_params:
        new_kwargs.update(page.app.view_params)

    if 'nav_bar_params' in new_kwargs:
        current_nav_bar_params = nav_bar_params or {}
        nav_bar_params = new_kwargs.pop('nav_bar_params')
        nav_bar_params.update(current_nav_bar_params)

    if 'app_bar_params' in new_kwargs:
        current_app_bar_params = app_bar_params or {}
        app_bar_params = new_kwargs.pop('app_bar_params')
        app_bar_params.update(current_app_bar_params)

    new_kwargs.update(kwargs)

    if page.navigation:
        nav_bar_params = nav_bar_params or {}
        controls.append(page.navigation.get_bar(**nav_bar_params))

    if app_bar_params:
        app_bar = app_bar_factory(page, **app_bar_params)
        controls = [app_bar, ] + controls

    return ft.View(controls=controls, **new_kwargs)
