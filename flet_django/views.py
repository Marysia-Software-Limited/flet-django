from dataclasses import dataclass
from dataclasses import field
from typing import Optional, Type, Callable
from typing import Union

import flet as ft
from flet_core import Control

from flet_django.types import PAGE_CLASS


@dataclass
class GenericViewFactory:
    page: PAGE_CLASS
    kwargs: dict = field(default_factory=dict)

    def get_view(self, controls, **kwargs):
        return ft.View(controls=controls, **kwargs)

    def __call__(self, controls, **kwargs):
        new_kwargs = self.kwargs.copy()
        new_kwargs.update(kwargs)
        return self.get_view(controls=controls, **new_kwargs)





@dataclass
class ViewFactory(GenericViewFactory):

    def app_bar_factory(self, title: str = '', action_params: Optional[dict] = None, **kwargs) -> ft.AppBar:
        action_params = action_params or {}

        new_kwargs = dict(
            title=ft.Text(value=title),
            actions=self.page.navigation.get_actions(**action_params)
        )
        new_kwargs.update(kwargs)

        return ft.AppBar(**new_kwargs)

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

        if 'nav_bar_params' in new_kwargs:
            current_nav_bar_params = nav_bar_params or {}
            nav_bar_params = new_kwargs.pop('nav_bar_params')
            nav_bar_params.update(current_nav_bar_params)

        if 'app_bar_params' in self.kwargs:
            current_app_bar_params = app_bar_params or {}
            app_bar_params = new_kwargs.pop('app_bar_params')
            app_bar_params.update(current_app_bar_params)

        if self.page.navigation:
            controls.append(self.page.navigation.get_bar(**nav_bar_params))

        if app_bar_params:
            app_bar = self.app_bar_factory(self.page, **app_bar_params)
            controls = [app_bar, ] + controls

        return self.get_view(controls=controls, **new_kwargs)


#################################################
#                   OLD CODE                    #
#################################################
def get_app_bar(page, title: str = '', action_params: Optional[dict] = None, **kwargs) -> ft.AppBar:
    action_params = action_params or {}

    new_kwargs = dict(
        title=ft.Text(value=title),
        actions=page.navigation.get_actions(**action_params)
    )
    new_kwargs.update(kwargs)

    return ft.AppBar(**new_kwargs)


def ft_view(
    page: PAGE_CLASS,
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
