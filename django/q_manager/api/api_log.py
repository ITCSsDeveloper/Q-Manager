import json
import psycopg2
from psycopg2.extensions import TRANSACTION_STATUS_ACTIVE
import psycopg2.extras
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from psycopg2.extras import RealDictCursor
from bson import json_util
import os
import signal
from datetime import datetime

# ROOT DIR
DIR_TASK = '/Users/ratchanonc1/Documents/GitHub/Q-Manager/Disk0'

# Init Connection
connection = psycopg2.connect(host="127.0.0.1",
                              port="5432",
                              user="postgres", 
                              password="Password12345",
                              database="postgres", 
                              options="-c search_path=dbo,q_manager")
connection.set_session(autocommit=True)
cursor = connection.cursor(cursor_factory = RealDictCursor)

@csrf_exempt
def get_task_info(guid) :
    sql = F"SELECT * FROM task_table T WHERE T.guid = '{guid}' LIMIT 1"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

@csrf_exempt
def api_get_task(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        task_info = get_task_info(guid)
        if len(task_info) == 0:
            return HttpResponse(status=404)

        result = json.dumps(task_info[0], default=json_util.default)
        return HttpResponse(status=200, content=result, content_type="application/json")

@csrf_exempt
def api_insert_log(request):
    if  request.method == "POST" :
        guid = request.POST['guid']
        pid = request.POST['pid']
        message = request.POST['message']

        dt = datetime.now()
        task_info = get_task_info(guid)
        if len(task_info) == 0:
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        sql  = F""" INSERT INTO logs_table(
	                pid, task_id, message, date, time)
	                VALUES (%s, %s, %s, LOCALTIMESTAMP, LOCALTIMESTAMP); """
        record_to_insert = (pid, task_info[0]['id'], message)
        cursor.execute(sql, record_to_insert)

    return HttpResponse(status=200)

@csrf_exempt
def api_update_status(request):
    if  request.method == "POST" :
        guid = request.POST['guid']
        status = request.POST['status']

        task_info = get_task_info(guid)
        if len(task_info) == 0:
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        sql = """ UPDATE task_table
                  SET status=%s   
                  WHERE guid=%s;"""
        params = (status, guid)
        cursor.execute(sql, params)
        return HttpResponse(status=200)
    pass

@csrf_exempt
def api_get_logs(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        task_info = get_task_info(guid)
        if len(task_info) == 0:
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        sql = F"""
                select * 
                from (
                    select 
                        id, pid, task_id , message , to_char(time,'DD-MM-YYYY') as date , to_char(time,'HH:mm:ss') as time
                    from logs_table 
                    where task_id =  {task_info[0]['id']}
                    order by id 
                    limit 1000
                ) as A
                order by A.id DESC 
              """
        cursor.execute(sql)
        result = json.dumps(cursor.fetchall(), default=json_util.default)
        return HttpResponse(status=200, content=result, content_type="application/json" )
    pass

@csrf_exempt
def api_update_pid(request):
    if  request.method == "POST" :
        guid = request.POST['guid']
        pid = request.POST['pid']

        task_info = get_task_info(guid)
        if len(task_info) == 0:
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        sql = """ UPDATE task_table
                  SET pid=%s   
                  WHERE guid=%s;"""
        params = (pid, guid)
        cursor.execute(sql, params)
        return HttpResponse(status=200)
    pass

@csrf_exempt
def api_stop(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        task_info = get_task_info(guid)
        if len(task_info) == 0:
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        # Kill Process
        pid = int(task_info[0]['pid'])
        os.kill(pid, signal.SIGTERM)

        # Update Status To TERMINATE
        sql = """ UPDATE task_table
                  SET pid=%s, status=%s
                  WHERE guid=%s;"""
        params = ('', "TERMINATE" ,guid)
        cursor.execute(sql, params)

        # UPDATE LOGS
        sql  = F""" INSERT INTO logs_table(
	                pid, task_id, message, date, time)
	                VALUES (%s, %s, %s, LOCALTIMESTAMP, LOCALTIMESTAMP); """
        record_to_insert = (pid, task_info[0]['id'], 'TERMINATE by User')
        cursor.execute(sql, record_to_insert)

        return HttpResponse(status=200)

@csrf_exempt
def api_reset(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        task_info = get_task_info(guid)
        if len(task_info) == 0:
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        sql = """ UPDATE task_table SET pid=%s, status=%s WHERE id=%s """
        params = ('', "PENDING", task_info[0]['id'])
        cursor.execute(sql, params)
        return HttpResponse(status=200)

@csrf_exempt
def api_clear_logs(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        task_info = get_task_info(guid)
        if len(task_info) == 0:
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        sql = F""" DELETE FROM logs_table WHERE task_id = '{task_info[0]['id']}'"""
        cursor.execute(sql)
        return HttpResponse(status=200)