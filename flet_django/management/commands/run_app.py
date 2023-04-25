import flet as ft
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from django.conf import settings

from main_app import main


class Command(BaseCommand):
    help = _('Run flutter app.')

    def add_arguments(self, parser):

        default_view = settings.FLET_VIEW if hasattr(settings, "FLET_VIEW") else ft.FLET_APP
        parser.add_argument(
            '--view',
            type=str,
            default=default_view,
            required=False,
            help=_(f"Chose view from web_browser, flet_app and flet_app_hidden. Default is {default_view}.")
        )

        default_port = int(settings.FLET_PORT) if hasattr(settings, "FLET_PORT") else 8085
        parser.add_argument(
            '--port',
            type=int,
            default=default_port,
            required=False,
            help=_(f"Chose port. Default is {default_port}.")
        )

        default_host = settings.FLET_HOST if hasattr(settings, "FLET_HOST") else "127.0.0.1",
        parser.add_argument(
            '--host',
            type=str,
            default=default_host,
            required=False,
            help=_(f"Chose host. Default is {default_host}.")
        )

        default_assets_dir = settings.FLET_ASSETS_DIR if hasattr(settings, "FLET_ASSETS_DIR") else settings.STATIC_ROOT or "assets"
        parser.add_argument(
            '--assets-dir',
            type=str,
            default=default_assets_dir,
            required=False,
            help=_(f"Chose directory for Flutter assets. Default is {default_assets_dir}.")
        )

        default_upload_dir = settings.FLET_UPLOAD_DIR if hasattr(settings, "FLET_UPLOAD_DIR") else settings.MEDIA_ROOT or "uploads"
        parser.add_argument(
            '--upload-dir',
            type=str,
            default=default_upload_dir,
            required=False,
            help=_(f"Chose directory for Flutter uploads. Default is {default_upload_dir}.")
        )

    def handle(self, *args, **options):

        view = options["view"]

        self.stdout.write(self.style.MIGRATE_HEADING('Let run flutter app.'))
        ft.app(
            target=main,
            port=options["port"],
            view=view,
            host=options["host"],
            assets_dir=options["assets_dir"],
            upload_dir=options["upload_dir"],
        )
        self.stdout.write(self.style.SUCCESS('Finish running flutter app.'))
