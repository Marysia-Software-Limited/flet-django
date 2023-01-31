from dataclasses import dataclass
from typing import Optional, Type, Callable

import flet as ft
from flet_core import Control

from flet_django.types import PAGE_CLASS


class GenericView(ft.View):
    def __init__(self, controls: Optional[list[Control]] = None, text: Optional[str] = None,
                 vertical_alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.CENTER,
                 horizontal_alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.CENTER,
                 **kwargs):
        super().__init__(
            controls=controls or [ft.Text(text)],
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
            **kwargs
        )


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
    view_class: Type[GenericView] = GenericView,
    nav_bar_params: Optional[dict] = None,
    app_bar_params: Optional[dict] = None,
    app_bar_factory: Callable = get_app_bar,
    **kwargs,
):
    new_kwargs = page.app.view_params or {}

    if 'nav_bar_params' in new_kwargs:
        current_nav_bar_params = nav_bar_params or {}
        nav_bar_params = new_kwargs.pop('nav_bar_params')
        nav_bar_params.update(current_nav_bar_params)

    if 'app_bar_params' in new_kwargs:
        current_app_bar_params = app_bar_params or {}
        app_bar_params = new_kwargs.pop('app_bar_params')
        app_bar_params.update(current_app_bar_params)

    if 'view_class' in new_kwargs:
        default_view_class = new_kwargs.pop('view_class')
        view_class = view_class or default_view_class

    if 'app_bar_factory' in new_kwargs:
        default_app_bar_factory = new_kwargs.pop('app_bar_factory')
        app_bar_factory = app_bar_factory or default_app_bar_factory

    new_kwargs.update(kwargs)

    if page.navigation:
        nav_bar_params = nav_bar_params or {}
        controls.append(page.navigation.get_bar(**nav_bar_params))

    if app_bar_params:
        app_bar = app_bar_factory(page, **app_bar_params)
        controls = [app_bar, ] + controls

    return view_class(controls=controls, **new_kwargs)
