from abc import ABC
from dataclasses import dataclass, field
from typing import Callable, Iterable, Dict


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
        return self.control(page, *args, **kwargs)
