import pymongo
import logging
import os
import time
import sys
import requests

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

mo_database = 'acc'      # Database Name   ( Mongo จะสร้างให้อัตโนมัติถ้ายังไม่ถูกสร้าง )
mo_collection = 'acc'    # Collection Name ( Mongo จะสร้างให้อัตโนมัติถ้ายังไม่ถูกสร้าง )

log_name = 'log_acc.log' # Log file name
#############################################################

"""
    
    อธิบาย Mapfile  ( ./data/LA00000.MAP )

    ทุกครั้งที่จะเอาข้อมูลเข้า Database เราต้องทำการระบุชื่อฟิลด์ให้กับข้อมูลก่อน
    โดย ให้เข้าไประบุไว้ในไฟล์ .MAP

    ใน mapfile จะมีส่วนที่กำหนดค่าอยู่ 3 ส่วน คือ HEADER, BODY, FOOTER
    
    ยกตัวอย่าง (HEADER, BODY, FOOTER ใช้หลักการกำหนดแบบเดียวกัน) :
    #HEADER     ( คือ ระบุว่าข้อมูลต่อจากนี้จะเป็นส่วนของ Column Header )
    #ENDHEADER  ( คือ ระบุว่าให้หยุดอ่านข้อมูลของ  Header )

"""

""" 

* วิธีเรียกใช้งาน
 - python3 main.py -file_name=./data/LA00000.GCC -map_file_name=./data/LA00000.MAP -limit=100 -header=HT -body=DT -footer=FT
 
* อธิบาย Parameter :
 -file_name={value}        ( ให้ใส่ Part ไฟล์ Source )
 -map_file_name={value}    ( ให้ใส่ Part ไฟล์ Mapping  )
 -limit={value}            ( จำนวนข้อมูลต่อรอบการ Insert เช่น ใส่ 100 จะหมายถึง ให้อ่านข้อมูลครบ 100 rows ก่อนถึงค่อยทำการ Insert ลง Database  )
 -header={value}           ( ระบุชุดข้อมูลแบบ Header เช่น ใส่ HT เมื่อโปรแกรมอ่านเจอขึ้นต้นว่า HT โปรแกรมจะเข้าใจว่าบรรทัดนั้นคือข้อมูล Header  )
 -body={value}             ( ระบุชุดข้อมูลแบบ Body   เช่น ใส่ DT เมื่อโปรแกรมอ่านเจอขึ้นต้นว่า DT โปรแกรมจะเข้าใจว่าบรรทัดนั้นคือข้อมูล Body  )
 -footer={value}           ( ระบุชุดข้อมูลแบบ Footer เช่น ใส่ FT เมื่อโปรแกรมอ่านเจอขึ้นต้นว่า FT โปรแกรมจะเข้าใจว่าบรรทัดนั้นคือข้อมูล Footer  )

* หมายเหตุ -header, -body, -footer ไม่ใส่ก็ได้ โปรแกรมจะ Default ค่าไว้ให้ HT, DT, FT ตามลำดับ

"""

"""
 ไฟล์ Log จะเก็บอยู่ที่ Folder logs
"""

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

# HELPER CLASS  (ค่อยย้ายออกไปข้างนอก ตอนนี้ติดบัคอยู่ไม่รู้ว่าทำไม)
class MyHelper:
    __api_url = 'http://localhost:8000'
    __guid = ""
    __pid = ""

    def __init__(self, guid, pid):
        self.__guid = guid
        self.__pid = pid
        pass

    # ตรวจสอบว่ามี guid นี้อยู่ใน database ไหม
    def api_get_task(self) :
        url = F"{self.__api_url}/api/helper/get_task"
        payload={'guid': self.__guid}
        response = requests.request("POST", url, headers={}, data=payload, files=[])
        if response.status_code == 200:
            return 1
        elif response.status_code == 404:
            return None
        pass

    # Insert log ลง db
    def api_log_insert(self, message): 
        try :
            url = F"{self.__api_url}/api/helper/insert_log"
            payload={'guid': self.__guid,'pid': self.__pid, 'message': message}
            requests.request("POST", url, headers={}, data=payload, files=[])
        except:
            print("Unexpected error:", sys.exc_info()[0])
            pass
        pass

    def api_update_status(self, status):
        try :
            url = F"{self.__api_url}/api/helper/update_status"
            payload={   
                'guid': self.__guid,
                'status': status
            }
            requests.request("POST", url, headers={}, data=payload, files=[])
        except:
            print("Unexpected error:", sys.exc_info()[0])
            pass
        pass

    def api_update_pid(self):
       try :
           url = F"{self.__api_url}/api/helper/update_pid"
           payload={   
               'guid': self.__guid,
               'pid': self.__pid
           }
           requests.request("POST", url, headers={}, data=payload, files=[])
       except:
           print("Unexpected error:", sys.exc_info()[0])
           pass
       pass
#END OF HELPER CLASS

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

    # __api_helpter = None
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
        self.__api_helpter = MyHelper(self.__guid, self.__pid)
        self.change_status(self.RUNNING)  # UPDATE STATUS TO RUNNING
        self.update_pid()
        self.log(F'PID = {self.__pid}')

        time.sleep(15)
        
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