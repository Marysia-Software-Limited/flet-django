import flet as ft
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from config import config
from tasks.main_app import main


class Command(BaseCommand):
    help = _('Run flutter app.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--view',
            type=str,
            default=ft.FLET_APP,
            required=False,
            help=_("Select view from web_browser, flet_app, flet_app_hidden. Default is flet_app")
        )

    def handle(self, *args, **options):
        # try:
        if True:
            if options["view"]:
                view = options["view"]
            else:
                view = ft.FLET_APP_HIDDEN
            self.stdout.write(self.style.MIGRATE_HEADING('Let run flutter app.'))
            ft.app(target=main, port=config.APP_PORT, view=view, host=config.APP_HOST)
        # except Exception as e:
        #     self.stderr.write(self.style.ERROR(f'Flutter app error: {e}'))
        self.stdout.write(self.style.SUCCESS('Finish running flutter app.'))
