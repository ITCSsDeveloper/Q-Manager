from django.contrib import admin
from django.urls import path
from . import views
from . import api_web_controller as api_web
from . import api_log

# WebManageAPI
# ClientApi

urlpatterns = [
    # ROOT RENDER VIEWS
    path('',views.index),
    path('task/create',views.create_view),
    path('task/logs',views.log_view),
    path('task/update',views.update_view),
    path('task/delete',views.delete_view),
    path('task/monitor',views.monitor),

    # WEB API
    path('api/task/start',  api_web.api_start),
    path('api/task/stop', api_web.api_stop),
    path('api/task/reset', api_web.api_reset),
    path('api/task/show', api_web.api_show_all_task),
    path('api/task/create',  api_web.api_create_task),
    path('api/task/delete',  api_web.api_delete_task),
    path('api/task/log/show', api_web.api_get_logs),
    path('api/task/log/clear', api_web.api_clear_logs),

    # JOB API
    path('api/helper/get_task', api_log.api_get_task),
    path('api/helper/insert_log', api_log.api_insert_log),
    path('api/helper/update_status', api_log.api_update_status),
    path('api/helper/update_pid', api_log.api_update_pid),
]
