import datetime

import flet as ft
from dateutil import relativedelta

from flet_django.controls import ModelTableControl
from flet_django.pages import GenericClient
from flet_django.views import ft_view
from tasks.models import Task


def tasks(page: GenericClient, date_from=None, period: relativedelta = None, title: str = "Tasks"):
    filters = {}
    if date_from is not None:
        filters["date_add__gte"] = date_from
        if period is not None:
            filters["date_add__lt"] = date_from + period
    return page.get_view(
        controls=[ModelTableControl(
                model=Task,
                filters=filters
            )
        ],
        app_bar_params=dict(title=title)
    )


def month_archive(page: GenericClient, year: int, month: int):
    return tasks(
        page,
        datetime.datetime(year=year, month=month, day=1),
        relativedelta.relativedelta(months=1),
        "Monthly Tasks"
    )


def year_archive(page: GenericClient, year: int):
    return tasks(
        page,
        datetime.datetime(year=year, month=1, day=1),
        relativedelta.relativedelta(years=1),
        "Yearly Tasks"
    )


def tasks_2003(page: GenericClient):
    return tasks(
        page,
        datetime.datetime(year=2023, month=1, day=1),
        relativedelta.relativedelta(years=1),
        "2023 Tasks"
    )
