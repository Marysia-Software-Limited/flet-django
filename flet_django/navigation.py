from abc import ABC
from dataclasses import dataclass, field
from typing import Optional, List, Callable

import flet as ft
from flet.types import PaddingValue
from flet_core import Control

from flet_django.types import PAGE_CLASS, DESTINATION_CLASS


@dataclass
class Navigare(ABC):
    page: PAGE_CLASS
    destinations: Optional[List[DESTINATION_CLASS]] = field(default_factory=list)
    selected_index: Optional[int] = None

    def on_change(self) -> Callable:
        def __on_change(e):
            """
            Define the NavigationBar control behaviour.

            :param e: event
            :return: return routing url depending on
                a chosen button of NavigationBar control
            """
            try:
                index = int(e.data)
                self.selected_index = index
                destiny = self.destinations[index]
                self.page.route = destiny.route

            except ValueError:
                print(f"Can't parse index value:{e.data}")
            except IndexError:
                print(f"Can't found destiny for index:{e.data}")

        return __on_change

    def get_bar(self, *args, **kwagrs):
        destinations = []
        index = -1
        for destiny in self.destinations:
            if destiny.nav_bar:
                destinations.append(destiny.get_bar())

                # for a case if selected index is not set on beginning
                # recognize current view and set it as selected
                index += 1
                if self.selected_index is None and destiny.route == self.page.route:
                    self.selected_index = index

        new_kwargs = dict(
            on_change=self.on_change(),
            destinations=destinations,
            selected_index=self.selected_index
        )
        new_kwargs.update(kwagrs)
        return ft.NavigationBar(*args, **new_kwargs)

    def get_rail(self, *args, **kwagrs):
        new_kwargs = dict(
            on_change=self.on_change(),
            destinations=[destiny.get_rail() for destiny in self.destinations if destiny.nav_rail]
        )
        new_kwargs.update(kwagrs)
        return ft.NavigationRail(*args, **new_kwargs)

    def get_actions(self, button_factory: Callable = None, **kwargs):
        return [destiny.get_button(self.page, button_factory, **kwargs) for destiny in self.destinations if destiny.action]


@dataclass
class Fatum(ABC):
    route: str
    icon: Optional[str] = None
    icon_content: Optional[Control] = None
    selected_icon: Optional[str] = None
    selected_icon_content: Optional[Control] = None
    label: Optional[str] = None
    label_content: Optional[Control] = None,
    padding: PaddingValue = None,
    nav_bar: bool = True
    nav_rail: bool = True
    action: bool = True

    def get_bar(self, *args, **kwagrs):
        new_kwargs = dict(
            icon=self.icon,
            icon_content=self.icon_content,
            selected_icon=self.selected_icon,
            selected_icon_content=self.selected_icon_content,
            label=self.label
        )
        new_kwargs.update(kwagrs)
        return ft.NavigationDestination(*args, **new_kwargs)

    def get_rail(self, *args, **kwagrs):
        new_kwargs = dict(
            icon=self.icon,
            icon_content=self.icon_content,
            selected_icon=self.selected_icon,
            selected_icon_content=self.selected_icon_content,
            label=self.label,
            label_content=self.label_content,
            padding=self.padding
        )
        new_kwargs.update(kwagrs)
        return ft.NavigationRailDestination(*args, **new_kwargs)

    def get_button(self, page, button_factory: Optional[Callable] = None, **kwargs):

        def __button_factory(destiny, **button_kwargs):
            selected: bool = destiny.route == page.route

            def __on_click(e):
                if selected:
                    page.pop()
                else:
                    page.route = destiny.route

            new_kwargs = dict(
                icon=destiny.icon,
                selected_icon=destiny.selected_icon,
                tooltip=destiny.label,
                selected=selected,
                on_click=__on_click
            )
            new_kwargs.update(button_kwargs)
            return ft.IconButton(**new_kwargs)

        button_factory = button_factory or __button_factory

        return button_factory(self, **kwargs)
