import flet as ft
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from main_app import main


class Command(BaseCommand):
    help = _('Run flutter app.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--view',
            type=str,
            default=ft.FLET_APP,
            required=False,
            help=_("Chose view from web_browser, flet_app and flet_app_hidden. Default is flet_app.")
        )
        parser.add_argument(
            '--port',
            type=str,
            default=8085,
            required=False,
            help=_("Chose port. Default is 8085.")
        )
        parser.add_argument(
            '--host',
            type=str,
            default="127.0.0.1",
            required=False,
            help=_("Chose host. Default is 127.0.0.1.")
        )

    def handle(self, *args, **options):

        view = options["view"]

        self.stdout.write(self.style.MIGRATE_HEADING('Let run flutter app.'))
        ft.app(target=main, port=options["port"], view=view, host=options["host"])
        self.stdout.write(self.style.SUCCESS('Finish running flutter app.'))
