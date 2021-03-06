import pymongo
import logging
import os
import time
import sys
from client_api import clien_api_class


# Note 
# สิ่งแรกที่ task ควรจะได้มาพร้อม args คือ guid
# เพราะ ต้องใช้  guid ในการ (get task info, insert log)

# exit()

#############################################################

# Step1. Config MongoDB
mo_host = 'localhost'      # Host 
mo_user = 'mongodb'        # Password
mo_pass = 'Password12345'  # Password
mo_port = '27017'          # Port

mo_database = 'gcc'      # Database Name   ( Mongo จะสร้างให้อัตโนมัติถ้ายังไม่ถูกสร้าง )
mo_collection = 'gcc'    # Collection Name ( Mongo จะสร้างให้อัตโนมัติถ้ายังไม่ถูกสร้าง )

log_name = 'log_gcc.log' # Log file name
#############################################################

# Get Script path runing
script_path = os.path.dirname(os.path.abspath(__file__))
print('__name__', __name__)
print('script_path', script_path)

# Setup Logging
logFormatter = "%(asctime)s %(levelname)s: %(message)s"
logging.basicConfig( filename=F'{script_path}/logs/{log_name}',
                    encoding='utf-8',
                    level=logging.INFO,
                    format=logFormatter,
                    filemode='a'
                    )
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter(logFormatter))
logging.getLogger("").setLevel(logging.INFO)
logging.getLogger("").addHandler(console)
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("requests").addHandler(logging.NullHandler())
# Connection
conn_str = F'mongodb://{mo_user}:{mo_pass}@{mo_host}:{mo_port}'

#----------------------------------------------------------------------------#


class ImportToMongo :
    __guid = ""
    __pid = ""
    __myclient = None
    __mydb = None
    __mycol = None

    __start_time = None
    __stop_time = None

    __limit = 0
    __header = "HT"
    __body = "DT"
    __footer = "FT"

    __file_name = ""
    __map_file_name = ""

    __task_info = None

    #TODO Move Constatn to New Class
    PENDING = 'PENDING'     #เพิ่งสร้าง
    RUNNING = 'RUNNING'     #กำลังทำงาน
    FINISH ='FINISH'        #ทำงานเสร็จสิ้น
    TERMINATE = 'TERMINATE' #ถูกสั่งให้หยุด
    ERROR  ='ERROR'         #เกิด Error
 
    def log(self, message):
        logging.info(message)
        self.__api_helpter.api_log_insert(message=message)
        pass
    
    def change_status(self, stauts):
        self.log(F'Change Status To -> {stauts}')
        self.__api_helpter.api_update_status(status=stauts)
        pass

    def update_pid(self):
        self.log(F'Update PID -> {self.__pid}')
        self.__api_helpter.api_update_pid()
        pass

    def __init__(self):
        # Get args
        self.get_args()

        # Set PID
        self.__pid = os.getpid()

         # Init MyHelper สำหรับ Insert Logs
        self.__api_helpter = clien_api_class(self.__guid, self.__pid)
        self.change_status(self.RUNNING)  # UPDATE STATUS TO RUNNING
        self.update_pid()
        self.log(F'PID = {self.__pid}')

        time.sleep(5)
        
        # Check args
        if self.__guid == '':
            self.log(F'-guid is required')
            sys.exit()
        if self.__file_name == '':
            self.log(F'-file_name is required')
            sys.exit()
        if self.__map_file_name == '':
            self.log(F'-map_file_name is required')
            sys.exit()
        if self.__limit == 0:
            self.log(F'-limit is required')
            sys.exit()

        # REAL Start
        self.__start_time = time.time()

        # GET Task Info
        task_info = self.__api_helpter.api_get_task()
        if(task_info != None):
            self.__task_info = task_info
        else:
            self.log(F'The registration information was not found.')
            sys.exit()

        # Setup Pymongo Connection String
        self.__myclient = pymongo.MongoClient(conn_str)
        self.__mydb = self.__myclient[mo_database] # Create Database
        self.__mycol = self.__mydb[mo_collection]    # Create Collection
        self.__mycol.delete_many({})         # Clear Collection
        self.log(F'DB Connected host={self.__myclient.HOST}:{self.__myclient.PORT}')
        self.log(F'args limit={self.__limit}')
        pass
    
    def time_convert(self, sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        return ("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

    def get_args(self):
        for a in sys.argv:
            if "-guid=" in a: 
                self.__guid = str(a.split('=')[1])
            if "-limit=" in a: 
                self.__limit = int(a.split('=')[1])
            if "-header=" in a: 
                self.__header = str(a.split('=')[1])
            if "-body=" in a: 
                self.__body = str(a.split('=')[1])
            if "-footer=" in a: 
                self.__footer = str(a.split('=')[1])
            if "-file_name=" in a: 
                self.__file_name = str(a.split('=')[1])
            if "-map_file_name=" in a: 
                self.__map_file_name = str(a.split('=')[1])

    def get_mapping_template(self) :
       isHeader= False,
       isBody = False,
       isFooter = False
       template = {
           "header" : [],
           "body" : [],
           "footer" : []
       }
       with open(self.__map_file_name, mode="r") as f:
           for line in f:
               line = line.strip()

               if(line == "#HEADER") : isHeader = True; continue
               elif(line=="#ENDHEADER"): isHeader = False; continue
               elif(line == "#BODY") : isBody = True; continue
               elif(line=="#ENDBODY"): isBody = False; continue
               elif(line == "#FOOTER") : isFooter = True; continue
               elif(line=="#ENDFOOTER"):isFooter = False; continue

               if isHeader == True :
                   template["header"].append(line)
                   continue
               elif isBody == True :
                   template["body"].append(line)
                   continue
               elif isFooter == True :
                   template["footer"].append(line)
                   continue
       return template

    def start(self): 
        file_name = self.__file_name
        map_file_name = self.__map_file_name

        row = 0                 # Current Row Insert Per Cycle
        limit = self.__limit    # Limit Row Insert Per Cycle (Recommend 10000 rows per cpu core)
        la_list_temp = []       # Temporary files
        row_inserted = 0        # Total Row Inserted 
        header = None           # var for keep header file
        footer = None           # var for keep footer file

        num_lines = sum(1 for line in open(file_name))  # Check Total Lines
        map_template = self.get_mapping_template()    

        self.log(F'-------------------------------------------')
        self.log(F'Total Lines {str(num_lines)}')
        self.log(F'File Name : {file_name}')
        self.log(F'Map File Name : {map_file_name}')
        self.log(F'Start Import')

        # Start Process
        with open(file_name , mode="r") as f:
            for line in f:
                data = line.split('|')          # Split With

                # Check Header and Keep
                if data[0] == self.__header:             
                    data[2] = data[2].replace('\n','')
                    header = data
                    continue
                # Check Footer and Keep
                elif data[0] == self.__footer:          
                    data[1] = data[1].replace('\n','')
                    footer = data
                    pass
                # Check Data and Keep
                elif data[0] == self.__body:
                    model_temp = {}
                    for i in range(len(data)):
                        model_temp[map_template['body'][i]] = data[i].strip().replace('\n','')
                    la_list_temp.append(model_temp)

                row += 1

                # Insert To MongoDB
                if (row >= limit) or (data[0] == self.__footer and row != 0) :
                    if  len(la_list_temp) > 0:
                        self.__mycol.insert_many(la_list_temp)     
                        row_inserted += len(la_list_temp)
                        
                        self.log(F'Inserted = {str(row)} {str(row_inserted)}/{str(num_lines)}')
                        la_list_temp = []
                        row = 0

        self.__stop_time = time.time()
        time_lapsed = self.time_convert((self.__stop_time - self.__start_time) )

        self.log(F'-------------------------------------------')
        self.log(F'Complete')
        self.log(F'Time lapsed : {time_lapsed}')
        self.log(F'File Name : {file_name}')
        self.log(F'Map File Name : {map_file_name}')

        self.log(F'Insert Limit : {limit}')
        self.log(F'Total Lines : {num_lines}')
        self.log(F'Total Inserted : {row_inserted}')
        self.log(F'Header : {header}')
        self.log(F'Footer : {footer}')
        self.log(F'-------------------------------------------')
        self.change_status(self.FINISH) # UPDATE STATUS TO FINISH
        pass # End of Start

# Init App And Start Process
app = ImportToMongo()
app.start()
del(app)