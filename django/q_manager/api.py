import json
import uuid 
import psycopg2
from psycopg2.extensions import TRANSACTION_STATUS_ACTIVE
import psycopg2.extras
import subprocess
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from psycopg2.extras import RealDictCursor
from bson import json_util
import sys
import time
import signal
import os

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
    sql = "SELECT * FROM q_manager.task_table ORDER BY id"
    cursor.execute(sql)
    result = json.dumps(cursor.fetchall(), default=json_util.default)
    return HttpResponse(status=200, content=result, content_type="application/json" )

@csrf_exempt
def api_create_task(request):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        file_name = request.POST['file_name']
        task_args = request.POST['task_args']
       
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
        # create_by = "SYSTEM"
        # create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # start_time =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        
        # Insert new Task
        sql = """INSERT INTO q_manager.task_table(
	            task_name, pid, status, guid, file_name, args)
	            VALUES (%s, %s, %s, %s, %s, %s);"""
        record_to_insert = (task_name, pid, status, guid, file_name, task_args)
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
        task_info = cursor.fetchall()
        if len(task_info) == 0 : 
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        # Validate Task Can Run ?
        row = task_info[0]
        if row['status'] == 'PENDING' :
            comm = F"python3 {DIR_TASK}/{row['file_name']} {row['args']}"
            
            comm = comm.replace("{DIR_TASK}", DIR_TASK)
            comm = comm.replace("{GUID}", guid)
            print('StartComm=', comm)
            # time.sleep(1)
            try:
                po = subprocess.Popen(comm, shell=True)
            except:
                print("Unexpected error:", sys.exc_info()[0])
            time.sleep(1)

            return HttpResponse(status=200)
        else :
            return HttpResponse(status=403, content=F"Task Unavailable")

def api_monitor(request):
    #TODO Get Last Status + Get Last Log
    return HttpResponse('monitor')


def api_logs(request):
    #TODO get all logs with pid or task_name
    return HttpResponse('logs')

def api_stop(request):
    #TODO get all logs with pid or task_name
    return HttpResponse('logs')