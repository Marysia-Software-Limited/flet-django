from abc import ABC
from dataclasses import dataclass, field
from typing import Callable, Iterable, Dict

import flet as ft

@dataclass
class FtViewRoute(ABC):
    route: str
    name: str
    control: Callable
    args: Iterable = field(default_factory=list)
    kwargs: Dict = field(default_factory=dict)

    def __call__(self, page, *args, **kwargs):
        args += self.args
        kwargs.update(self.kwargs)
        result = self.control(page, *args, **kwargs)
        if isinstance(result, ft.View):
            result.route = self.route
        return result
