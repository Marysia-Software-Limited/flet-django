import flet as ft
from django.urls import include, path

from flet_django.pages import GenericPage, GenericApp
from flet_django.views import ft_view
from flet_django.navigation import Fatum

import tasks.ft_urls
from tasks.todo_app import TodoApp


def home(page: GenericPage):
    return ft_view(
        page,
        controls=[TodoApp()],
        app_bar_params=dict(title="ToDo app")
    )


urlpatterns = [
    path('tasks', include(tasks.ft_urls)),
    path('', home, name="home")
]

destinations = [
    Fatum("/", icon=ft.icons.HOME, selected_icon=ft.icons.HOME_OUTLINED, label="home"),
    Fatum("/tasks", icon=ft.icons.LIST, selected_icon=ft.icons.LIST_OUTLINED, label="tasks", action=False),
]

app_bar_params = dict(bgcolor=ft.colors.SURFACE_VARIANT)
view_params = dict(app_bar_params=app_bar_params)

# main = GenericApp(
#     urls=urlpatterns,
#     destinations=destinations,
#     init_route="/",
#     view_params=view_params
# )
main = GenericApp(controls=[ft.Text("Hello World!"),])
