from datetime import datetime
from django.utils.translation import gettext as _
from django.core.management.base import BaseCommand
import flet as ft

from tasks.models import Task


def main(page: ft.Page):

    columns = []
    fields = [
        ("name", _("Task"),),
        ("is_done", _("Is done")),
        ("date_add", _("Creation date"))
    ]

    for field, label in fields:
        columns.append(ft.DataColumn(
                    ft.Text(label),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ))

    rows = []

    for task in Task.objects.all():
        row = []
        for field, label in fields:
            row.append(ft.DataCell(ft.Text(getattr(task, field, ""))))
        rows.append(ft.DataRow(row))


    page.add(
        ft.DataTable(
            # width=700,
            bgcolor="yellow",
            border=ft.border.all(2, "red"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, "blue"),
            horizontal_lines=ft.border.BorderSide(1, "green"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=100,
            data_row_color={"hovered": "0x30FF0000"},
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=columns,
            rows=rows,
        ),
    )


class Command(BaseCommand):
    help = _('Show simple task list')

    def handle(self, *args, **options):
            try:
                self.stdout.write(self.style.MIGRATE_HEADING('Let run flutter app.'))
                ft.app(target=main)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Flutter app error: {e}'))
            self.stdout.write(self.style.SUCCESS('Finish running flutter app.'))


def parse_date(date_txt: str):
    try:
        return datetime.strptime(date_txt, "%d.%m.%Y %H:%M:%S")
    except Exception as e:
        return e
