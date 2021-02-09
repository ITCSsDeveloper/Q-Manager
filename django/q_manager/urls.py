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
    path('create',views.create_view),
    path('logs',views.log_view),
    path('/update',views.update_view),
    path('/delete',views.delete_view),
    path('/monitor',views.monitor),

    # WEB API
    path('api/start',  api_web.api_start),
    path('api/stop', api_web.api_stop),
    path('api/reset', api_web.api_reset),
    path('api/clear_logs', api_web.api_clear_logs),
    path('api/show', api_web.api_show_all_task),
    path('api/create',  api_web.api_create_task),
    path('api/delete',  api_web.api_delete_task),

    # JOB API
    path('api/helper/get_task', api_log.api_get_task),
    path('api/helper/insert_log', api_log.api_insert_log),
    path('api/helper/update_status', api_log.api_update_status),
    # path('api/helper/clear_logs', api_log.api_clear_logs),
    path('api/helper/get_logs', api_log.api_get_logs),
    path('api/helper/update_pid', api_log.api_update_pid),
]
