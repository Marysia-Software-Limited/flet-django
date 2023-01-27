# Generated by Django 4.1.5 on 2023-01-27 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Epic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(max_length=1024)),
                ("delete", models.BooleanField(default=False)),
                ("date_add", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(max_length=1024)),
                ("is_done", models.BooleanField(default=False)),
                ("delete", models.BooleanField(default=False)),
                ("date_add", models.DateTimeField(auto_now_add=True)),
                ("date_change", models.DateTimeField(auto_now=True)),
                (
                    "epic",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="tasks.epic",
                    ),
                ),
            ],
        ),
    ]
