from abc import ABC
from dataclasses import dataclass
from typing import Optional

import flet as ft
from flet_core import Control


@dataclass
class FtView(ABC):
    controls: Optional[list[Control]] = None
    text: Optional[str] = None
    vertical_alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.CENTER
    horizontal_alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.CENTER

    def __post_init__(self) -> None:
        if self.controls is None:
            self.controls = [ft.Text(self.text)]

    def __call__(self):
        return ft.View(
            controls=self.controls,
            vertical_alignment=self.vertical_alignment,
            horizontal_alignment=self.horizontal_alignment
        )
