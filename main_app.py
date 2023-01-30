from datetime import datetime

import flet as ft
from django.urls import path
from django.utils.translation import gettext as _

from flet_django.pages import GenericPage, GenericApp
from flet_django.middlewares import simple_view_middleware, urls_middleware
from flet_django.views import FtView
from tasks.todo_app import TodoApp
from tasks.models import Task
# from .apps import
from django.apps import apps as django_apps  # https://docs.djangoproject.com/en/4.1/ref/applications/
from flet_django.controls import ModelTableControl
from dateutil import relativedelta


def home(_page: GenericPage):
    return FtView(
        controls=[
            ft.AppBar(title=ft.Text("ToDo app"), bgcolor=ft.colors.SURFACE_VARIANT),
            TodoApp()
        ]
    )


def tasks(_page: GenericPage, date_from=None, period: relativedelta = None, title: str = "Tasks"):
    filters = {}
    if date_from is not None:
        filters["date_added__gte"] = date_from
        if period is not None:
            filters["date_added__lt"] = date_from + period
    return FtView(
        controls=[
            ft.AppBar(title=ft.Text(title), bgcolor=ft.colors.SURFACE_VARIANT),
            ModelTableControl(
                model=Task,
                filters=filters
            )
        ]
    )


def month_archive(page: GenericPage, year: int, month: int):
    return tasks(
        page,
        datetime.datetime(year=year, month=month, day=1),
        relativedelta.relativedelta(months=1),
        "Monthly Tasks"
    )


def year_archive(page: GenericPage, year: int):
    return tasks(
        page,
        datetime.datetime(year=year, month=1, day=1),
        relativedelta.relativedelta(years=1),
        "Yearly Tasks"
    )


def tasks_2003(page: GenericPage):
    return tasks(
        page,
        datetime.datetime(year=2023, month=1, day=1),
        relativedelta.relativedelta(years=1),
        "2023 Tasks"
    )


urlpatterns = (
    path('tasks/2023/', tasks_2003),
    path('tasks/<int:year>/', year_archive),
    path('tasks/<int:year>/<int:month>/', month_archive),
    path('tasks/', tasks),
    path('', home, name="home")
)

middlewares = [
    urls_middleware(urls=urlpatterns)
]

main = GenericApp(
    middlewares=middlewares
)
