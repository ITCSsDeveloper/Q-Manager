from django.contrib import admin
from django.urls import path
from . import views
from . import api
from . import api_log

# WebManageAPI
# ClientApi

urlpatterns = [
    path('',views.index),
    path('create',views.create_view),
    path('logs',views.log_view),

    path('/update',views.update_view),
    path('/delete',views.delete_view),
    path('/monitor',views.monitor),

    path('api/helper/insert_log', api_log.api_insert_log),
    path('api/helper/get_task', api_log.api_get_task),
    path('api/helper/update_status', api_log.api_update_status),
    path('api/helper/clear_logs', api_log.api_clear_logs),
    path('api/helper/get_logs', api_log.api_get_logs),
    path('api/helper/update_pid', api_log.api_update_pid),
    
    path('api/helper/stop', api_log.api_stop),
    path('api/helper/delete', api.api_delete_task),

    path('api/helper/reset', api_log.api_reset),
    path('api/helper/clear_logs', api_log.api_clear_logs),

    path('api/show', api.api_show_all_task),
    path('api/create',  api.api_create_task),
    path('api/delete',  api.api_delete_task),
    path('api/start',  api.api_start)
]
