import requests

class clien_api_class:
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