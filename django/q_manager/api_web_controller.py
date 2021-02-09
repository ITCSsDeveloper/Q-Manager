import os, signal, json, uuid, sys, subprocess
from bson import json_util
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .Repository.db_file import db_class

# ROOT DIR
DIR_TASK = '/Users/ratchanonc1/Documents/GitHub/Q-Manager/Disk0'

class db_task_repo:
    cursor : any

    def __init__(self) -> None:
        self.cursor = db_class().cursor
        pass

    def get_all_task(self):
        sql = "SELECT * FROM task_table ORDER BY id"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def check_duplicate_task_name(self, task_name):
        sql = F"SELECT COUNT(1) FROM task_table T WHERE T.Task_name = '{task_name}'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]['count'] != 0

    def create_task(self, task_name, pid, status, guid, file_name, task_args):

        if self.check_duplicate_task_name(task_name=task_name) == True:
            return False

        sql = """INSERT INTO q_manager.task_table(
	            task_name, pid, status, guid, file_name, args)
	            VALUES (%s, %s, %s, %s, %s, %s);"""

        record_to_insert = (task_name, pid, status, guid, file_name, task_args)
        self.cursor.execute(sql, record_to_insert)
        return True

    def get_one_task(self, guid):
        sql = F"SELECT * FROM task_table T WHERE T.guid = '{guid}' LIMIT 1"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if results != [] : return results[0]
        return []
    
    def delete_task(self,guid):
        sql = F"DELETE FROM task_table T WHERE T.guid = '{guid}' "
        self.cursor.execute(sql)
        return True

    def task_update_status(self, guid, status):
        sql = "UPDATE task_table SET pid=%s, status=%s WHERE guid=%s;"
        params = ('', status ,guid)
        self.cursor.execute(sql, params)
        return True

    #TODO แยกออกไปเป็น TaskLogRepo
    def task_log(self, pid, task_id, message) :
        sql  = """ INSERT INTO logs_table(
	                pid, task_id, message, date, time)
	                VALUES (%s, %s, %s, LOCALTIMESTAMP, LOCALTIMESTAMP); """
        record_to_insert = (pid, task_id, message)
        self.cursor.execute(sql, record_to_insert)
        return True
        
    #TODO แยกออกไปเป็น TaskLogRepo
    def clear_log(self, task_id):
        sql = F""" DELETE FROM logs_table WHERE task_id = '{task_id}'"""
        self.cursor.execute(sql)
        return True


db_task = db_task_repo()
# db_task.check_duplicate_task_name('Task1')
# db_task.create_task('test1', '10001', 'PENDING', 'GUID', 'pyname.py', 'task_args')
# xx = db_task.get_one_task('GUID')



# Start API
@csrf_exempt
def api_show_all_task(request):
    result = json.dumps(db_task.get_all_task(), default=json_util.default)
    return HttpResponse(status=200, content=result, content_type="application/json" )

@csrf_exempt
def api_create_task(request):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        file_name = request.POST['file_name']
        task_args = request.POST['task_args']
       
        if db_task.check_duplicate_task_name(task_name) : 
            return HttpResponse(status=409, content="Duplicate Task Name")

        db_task.create_task(task_name=task_name,
                            pid='', status= "PENDING",guid=str(uuid.uuid4().hex),
                            file_name=file_name, task_args=task_args)
        
        return HttpResponse(status=200, content=F"Create Task Complete")
    else:
        return HttpResponse(status=405, content="Method not allow")
    pass

@csrf_exempt
def api_delete_task(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        if db_task.get_one_task(guid=guid) == [] : 
            return HttpResponse(status=404, content= F"Task {guid} Not Found")
        
        db_task.delete_task(guid=guid)

        return HttpResponse(status=200, content= F"Delete Task {guid} Complete")
    else :
        return HttpResponse(status=405, content="Method not allow")

@csrf_exempt
def api_start(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        # GET INFO TASK
        task_info = db_task.get_one_task(guid=guid)
        if len(task_info) == 0 : 
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        # Validate Task Can Run ?
        row = task_info[0]
        if row['status'] == 'PENDING' :

            comm = F"python3 {DIR_TASK}/{row['file_name']} {row['args']}"
            comm = comm.replace("{DIR_TASK}", DIR_TASK)
            comm = comm.replace("{GUID}", guid)
        
            try:
                po = subprocess.Popen(comm, shell=True)
            except:
                print("Unexpected error:", sys.exc_info()[0])

            return HttpResponse(status=200)
        else :
            return HttpResponse(status=403, content=F"Task Unavailable")

@csrf_exempt
def api_stop(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        task_info = db_task.get_one_task(guid=guid)
        if len(task_info) == 0:
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        # Kill Process
        pid = int(task_info[0]['pid'])
        os.kill(pid, signal.SIGTERM)

        db_task.task_update_status(guid=guid, status="TERMINATE")
        db_task.task_log(pid=pid, task_id=task_info[0]['id'], message='TERMINATE by User')

        return HttpResponse(status=200)

@csrf_exempt
def api_reset(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        task_info = db_task.get_one_task(guid=guid)
        if len(task_info) == 0:
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        db_task.task_update_status(guid=guid, status="PENDING")
        db_task.task_log(pid='', task_id=task_info[0]['id'], message='Reset to PENDING by User')

        return HttpResponse(status=200)

@csrf_exempt
def api_clear_logs(request):
    if  request.method == "POST" :
        guid = request.POST['guid']

        task_info = db_task.get_one_task(guid=guid)
        if len(task_info) == 0:
            return HttpResponse(status=404, content= F"Task {guid} Not Found")

        db_task.clear_log(task_id=task_info[0]['id'])
        return HttpResponse(status=200)