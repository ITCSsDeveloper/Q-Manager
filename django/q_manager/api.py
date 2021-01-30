import json
import sys
import uuid 
import time
import datetime
from django.http.response import JsonResponse
import psycopg2
from psycopg2.extensions import TRANSACTION_STATUS_ACTIVE
import psycopg2.extras
import subprocess
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, resolve_url
from psycopg2.extras import RealDictCursor
from bson import json_util

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

# Start API
def api_show_all_task(request):
    sql = "SELECT * FROM q_manager.task_table"
    cursor.execute(sql)
    result = json.dumps(cursor.fetchall(), default=json_util.default)
    return HttpResponse(status=200, content=result, content_type="application/json" )

@csrf_exempt
def api_create_task(request):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        task_command = request.POST['task_command']
       
        # Check Task Duplicate
        sql = F"SELECT * FROM task_table T WHERE T.Task_name = '{task_name}' LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result != [] : 
            return HttpResponse(status=409, content="Duplicate Task Name")

        # Prepare Parameter
        pid = ''
        guid = str(uuid.uuid4().hex)
        status = "PENDING"
        create_by = "SYSTEM"
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        start_time =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        command = task_command
        
        # Insert new Task
        sql = """INSERT INTO q_manager.task_table( \
	            task_name, pid, status, create_by, create_time, start_time, end_time, guid, command) \
	            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        record_to_insert = (task_name, pid,status, create_by, create_time, start_time, end_time, guid, command)
        cursor.execute(sql, record_to_insert)
        
        return HttpResponse(status=200, content=F"Create Task Complete : {guid}")
    else:
        return HttpResponse(status=405, content="Method not allow")
    pass

@csrf_exempt
def api_delete_task(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        sql = F"SELECT * FROM task_table T WHERE T.guid = '{guid}' LIMIT 1"
        cursor.execute(sql)
        results = cursor.fetchall()

        if results == [] : 
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        sql = F"DELETE FROM task_table T WHERE T.guid = '{guid}' "
        cursor.execute(sql)

        return HttpResponse(status=200, content= F"Delete Task {guid} Complete")
    else :
        return HttpResponse(status=405, content="Method not allow")

@csrf_exempt
def api_start(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        # GET INFO TASK
        sql = F"SELECT * FROM task_table T WHERE T.guid = '{guid}' LIMIT 1"
        cursor.execute(sql)
        results = cursor.fetchall()
        if results == [] : 
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        # Validate Task Can Run ?
        row = results[0]
        if row.status == 'PENDING' :
            # SET UP Args
            args = F"-guid={guid}"
            custom1 = ''  # custom args ใช้ในบางกรณนีที่ ต้องการส่ง parameter เข้าไปใน task 
            custom2 = ''
            custom3 = ''

            if custom1 != '' : args += F' -custom1={custom1}'
            if custom2 != '' : args += F' -custom2={custom2}'
            if custom3 != '' : args += F' -custom3={custom3}'

            #TODO แก้ให้ระบบรองรับ dir file + ใส่ filename
            # RUN TASK.py
            try:
                po = subprocess.Popen(F'python3 {DIR_TASK}/task1.py {args}',shell=True)
                time.sleep(3)
                return HttpResponse(status=200, content= F"Task Runing ....")
            except:
                return HttpResponse(status=500, content=F"Error : "+ sys.exc_info()[0])
        else :
            return HttpResponse(status=403, content=F"Task {guid} Not Ready for Run")
    else :
        return HttpResponse(status=405, content="Method not allow")

def api_monitor(request):
    #TODO Get Last Status + Get Last Log
    return HttpResponse('monitor')

def api_stop(request):
    # TODO Send COmmadn to kill process by pid 
    # AND UPDATE status to database
    # https://stackoverflow.com/questions/17856928/how-to-terminate-process-from-python-using-pid
    # os.kill(99999, signal.SIGTERM) #or signal.SIGKILL 
    return HttpResponse('stop')

def api_logs(request):
    #TODO get all logs with pid or task_name
    return HttpResponse('logs')
