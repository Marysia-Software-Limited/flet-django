import flet as ft
from django.utils.translation import gettext as _
from tasks.todo_app import TodoApp
# from .apps import
from django.apps import apps as django_apps  # https://docs.djangoproject.com/en/4.1/ref/applications/
from flet_django.controls import ModelTableControl

app_models = {}
app_navs = []


def nav_on_click(model_name, page):
    def __on_click_wrapper(event):
        page.go(f"/{model_name}")

    return __on_click_wrapper


def get_navs(main_view: bool, page):
    navs_buttons = []
    if not main_view:
        navs_buttons.append(ft.ElevatedButton("Todo", on_click=lambda _: page.go("/")), )
    for model_name, model in app_models.items():
        navs_buttons.append(ft.ElevatedButton(f"{model.__name__}", on_click=nav_on_click(model_name, page)))

    return ft.Row(controls=navs_buttons)


def main(page: ft.Page):
    page.title = _("Let it be.")
    page.horizontal_alignment = "center"
    page.scroll = "auto"
    page.update()

    # generate generic model controls

    for model_name, model in django_apps.all_models['tasks'].items():
        app_models[model_name] = model

    def route_change(route):

        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(title=ft.Text("ToDo app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    TodoApp(),
                    get_navs(True, page),
                ]
            )
        )
        if page.route[1:] in app_models:
            model_name = page.route[1:]
            model_view = ModelTableControl(app_models[model_name])
            page.views.append(
                ft.View(
                    route=f"/{model_name}",
                    controls=[
                        ft.AppBar(title=ft.Text(model.__name__), bgcolor=ft.colors.SURFACE_VARIANT),
                        model_view,
                        get_navs(False, page),
                    ]
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main)
