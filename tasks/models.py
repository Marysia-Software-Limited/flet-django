from django.db import models


class Epic(models.Model):
    name = models.TextField(max_length=1024)
    delete = models.BooleanField(default=False)
    date_add = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    name = models.TextField(max_length=1024)
    is_done = models.BooleanField(default=False)
    epic = models.ForeignKey(Epic, on_delete=models.SET_NULL, null=True)
    delete = models.BooleanField(default=False)
    date_add = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True)
