from django.urls import path

from tasks.ft_views import tasks_2003, year_archive, month_archive, tasks

urlpatterns = [
    path('/2023', tasks_2003),
    path('/<int:year>', year_archive),
    path('/<int:year>/<int:month>', month_archive),
    path('', tasks, name="tasks"),
]
