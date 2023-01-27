import flet as ft

from django.utils.translation import gettext as _

FIELDS_MODELS = {
    'IntegerField': 'text',
    'DurationField': None,
    'ManyToOneRel': None,
    'DateTimeField': 'date',
    'FileField': 'file',
    'TextField': 'text',
    'ImageField': None,
    'ForeignKey': None,
    'CharField': 'text',
    'BigIntegerField': 'text',
}


class ModelFormControl(ft.UserControl):

    def __init__(
            self,
            obj=None,
            title=None,
            **form_params
    ):
        super().__init__()

        self.obj = obj
        self.title = title or ft.Text(str(obj))
        self.content = ft.Text("PLACE FOR YOUR FORM")

    def build(self):
        return ft.Card(
            ft.Container(
                ft.Column([
                    ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL),
                    self.content,
                ]),
                padding=10,
            ),
        )

    def refresh_data(self, *args):
        self.update()

    def did_mount(self):
        self.refresh_data()
