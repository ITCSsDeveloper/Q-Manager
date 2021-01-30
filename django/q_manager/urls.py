from django.contrib import admin
from django.urls import path
from . import views
from . import api


urlpatterns = [
    path('',views.index),
    path('create',views.create_view),
    path('/update',views.update_view),
    path('/delete',views.delete_view),
    path('/monitor',views.monitor),

    path('api/show', api.api_show_all_task),
    path('api/create',  api.api_create_task),
    path('api/delete',  api.api_delete_task),
    path('api/start',  api.api_start),
    path('api/monitor',  api.api_monitor),
    path('api/stop',  api.api_stop),
    path('api/logs', api.api_logs)
]
