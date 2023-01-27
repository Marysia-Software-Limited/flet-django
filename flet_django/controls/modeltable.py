import flet as ft

from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import Q

ERROR_MSG = "-Err-"

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
    'BooleanField': 'bool',
}


# Data column
class Col:

    def __init__(self, name: str, label, field_type=None, width=None, on_sort=None):
        if isinstance(label, ft.Control):
            self.label = label
        else:
            self.label = ft.Text(label)
        self.name = name
        self.width = width
        self.type = field_type
        self.on_sort = on_sort

    def build_header(self):
        return ft.DataColumn(
            label=self.label,
            on_sort=self.on_sort,
        )

    def build_cell(self, obj):
        return ft.DataCell(
            content=ft.Text(
                str(
                    getattr(
                        obj,
                        self.name,
                        _("cell_error")
                    )
                ),
                width=self.width
            )
        )


def text_filter_kwargs(field_name: str, value: str):
    return {
        f"{field_name}__icontains": value.lower()
    }


class ModelTableControl(ft.UserControl):

    def __init__(
        self,
        model,
        columns=None,
        order=None,
        rows_per_page=10,
        title=None,
        filters=None,
        auto_filter=True,
        get_data_table=None,
        **data_table_params
    ):
        super().__init__()

        self.model = model
        self.order = order
        self.current_page = 1
        self.rows_per_page = rows_per_page
        self.num_pages = 1
        self.num_rows = 0
        self.title = title or model.__name__
        self.filters = filters
        self.auto_filter = auto_filter
        self.data_table_params = data_table_params

        self.v_current_page = ft.Text(str(self.current_page))
        self.v_search = ft.TextField(
            hint_text=_("Search..."),
            dense=True,
            on_change=self.on_search_auto,
            prefix_icon=ft.icons.SEARCH,
            border=ft.InputBorder.NONE,
            filled=False,
            on_submit=self.on_search_submit
        )
        self.v_count = ft.Text()

        if columns is None:
            self.columns = list(self.get_columns())
        else:
            self.columns = columns

        self.fields_indexes = {col.name: i for i, col in enumerate(self.columns)}

        if get_data_table is None:
            self.data_table = ft.DataTable(
                columns=[col.build_header() for col in self.columns],
                rows=[],
                **data_table_params
            )
        else:
            self.data_table = get_data_table(self)

    def get_columns(self):

        fields = self.model._meta.get_fields()

        def __on_sort(e):
            sorted_field_name = self.columns[e.column_index].name
            self.order = sorted_field_name if e.ascending else f"-{sorted_field_name}"
            self.refresh_data()

        for field in fields:
            class_name = field.__class__.__name__
            field_type = FIELDS_MODELS.get(class_name, None)
            if field_type is not None:
                name = field.name
                label = field.verbose_name or field.name

                yield Col(name=name, label=label, field_type=field_type, on_sort=__on_sort)

    def set_page(self, page=None, delta=0):
        if page is not None:
            self.current_page = page
        elif delta:
            self.current_page += delta
        else:
            return
        self.refresh_data()

    def next_page(self, e):
        self.set_page(delta=1)

    def prev_page(self, e):
        if self.current_page > 1:
            self.set_page(delta=-1)

    def goto_first_page(self, e):
        self.set_page(page=1)

    def goto_last_page(self, e):
        self.set_page(page=self.num_pages)

    def build_rows(self):
        qs = self.model.objects.all()

        if self.order:
            qs = qs.order_by(self.order)

        if self.v_search.value:
            q = Q()
            for column in self.columns:
                if column.type == "text":
                    q |= Q(**text_filter_kwargs(column.name, self.v_search.value))
            qs = qs.filter(q)

        if self.filters is not None:
            qs = qs.filter(**self.filters)

        self.num_rows = qs.count()
        paginator = Paginator(qs, self.rows_per_page)
        p_int, p_add = divmod(self.num_rows, self.rows_per_page)
        self.num_pages = p_int + (1 if p_add else 0)
        page_qs = paginator.page(self.current_page)
        # Load
        return [ft.DataRow(cells=[col.build_cell(obj) for col in self.columns])
                for obj in page_qs]

    def build(self):
        return ft.Card(
            ft.Container(
                ft.Column(
                    [
                        ft.Text(self.title, style=ft.TextThemeStyle.HEADLINE_SMALL),
                        ft.Row(
                            controls=[self.data_table],
                            scroll=ft.ScrollMode.ALWAYS,
                            spacing=10,
                        ),
                        ft.Row([
                            ft.IconButton(ft.icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=self.goto_first_page,
                                          tooltip=_("First page")),
                            ft.IconButton(ft.icons.KEYBOARD_ARROW_LEFT, on_click=self.prev_page,
                                          tooltip=_("Prev page")),
                            self.v_current_page,
                            ft.IconButton(ft.icons.KEYBOARD_ARROW_RIGHT, on_click=self.next_page,
                                          tooltip=_("Next page")),
                            ft.IconButton(ft.icons.KEYBOARD_DOUBLE_ARROW_RIGHT, on_click=self.goto_last_page,
                                          tooltip=_("Last page")),
                            self.v_search,
                            self.v_count,
                            ft.IconButton(ft.icons.REFRESH, on_click=self.refresh_data, tooltip=_("Refresh")),
                            ft.Slider(
                                min=10,
                                max=90,
                                divisions=8,
                                value=self.rows_per_page,
                                label=_("{value} rows per page"),
                                on_change=self.on_per_page_changed
                            ),
                        ]),
                    ],
                    scroll=ft.ScrollMode.ALWAYS
                ),
                padding=25,
            ),
        )

    def on_search_auto(self, e):
        if self.auto_filter:
            self.goto_first_page(e)

    def on_search_submit(self, e):
        self.goto_first_page(e)

    def on_per_page_changed(self, e):
        self.rows_per_page = int(e.control.value)
        self.refresh_data()

    def refresh_data(self, *args):
        self.data_table.rows = self.build_rows()
        if self.order:
            ascending = self.order[0] != '-'
            field_name = self.order if ascending else self.order[1:]
            order_index = self.fields_indexes[field_name]
            self.data_table.sort_ascending = ascending
            self.data_table.sort_column_index = order_index
        else:
            self.data_table.sort_ascending = None
            self.data_table.sort_column_index = None
        self.v_count.value = _("{} rows").format(self.num_rows)
        self.v_current_page.value = f"{self.current_page}/{self.num_pages}"
        self.update()

    def did_mount(self):
        self.refresh_data()
