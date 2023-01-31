import flet
from flet import (
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    Tab,
    Tabs,
    Text,
    TextField,
    UserControl,
    colors,
    icons,
)
from django.utils.translation import gettext as _
from .models import Task


class TaskView(UserControl):

    def __init__(self, task: Task, task_status_change, task_delete):
        super().__init__()
        self.task = task
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    @classmethod
    def create(cls, task_name, task_status_change, task_delete):
        task = Task(name=task_name)
        task.save()
        return cls(task, task_status_change, task_delete)

    def build(self):
        self.display_task = Checkbox(
            value=self.task.is_done, label=self.task.name, on_change=self.status_changed
        )
        self.edit_name = TextField(expand=1)

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip=_("Edit Task"),
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip=_("Delete Task"),
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip=_("Update Task"),
                    on_click=self.save_clicked,
                ),
            ],
        )
        return Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True

        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def status_changed(self, e):
        self.task.is_done = self.display_task.value
        self.task.save()
        self.task_status_change(self)

    @property
    def is_done(self):
        return self.task.is_done

    @classmethod
    @property
    def active(cls):
        return Task.objects.filter(is_done=False, delete=False).count()

    @classmethod
    def delete_completed(cls):
        Task.objects.filter(is_done=True).update(delete=True)

    def delete(self):
        self.task.delete = True
        self.task.save()

    def delete_clicked(self, e):
        self.delete()
        self.task_delete(self)


class TodoApp(UserControl):
    def build(self):
        self.new_task = TextField(
            hint_text=_("What You will, will be done."),
            expand=True,
            on_submit=self.add_clicked
        )
        self.tasks = Column()
        for task in Task.objects.filter(delete=False):
            task_view = TaskView(task, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task_view)

        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="all"), Tab(text="active"), Tab(text="completed")],
        )

        self.items_left = Text(_("0 wills to do"))

        # application's root control (i.e. "view") containing all other controls
        return Column(
            width=600,
            controls=[
                Row([Text(value="Todos", style="headlineMedium")], alignment="center"),
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
                                OutlinedButton(
                                    text=_("Done with what is done."), on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        if self.new_task.value:
            task_view = TaskView.create(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task_view)
            self.new_task.value = ""
            self.update()

    def task_status_change(self, task_view):
        self.update()

    def task_delete(self, task_view):
        self.tasks.controls.remove(task_view)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        TaskView.delete_completed()
        for task_view in self.tasks.controls[:]:
            if task_view.is_done:
                self.task_delete(task_view)

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = TaskView.active
        for task_view in self.tasks.controls:
            task_view.visible = (
                    status == "all"
                    or (status == "active" and task_view.is_done is False)
                    or (status == "completed" and task_view.is_done)
            )

        self.items_left.value = f"{count} {_('wills') if count > 1 else _('will')} {_('to be done.')}"
        super().update()
