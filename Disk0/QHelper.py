import psycopg2
import psycopg2.extras

class QHelper :
  # Init Connection
  connection = psycopg2.connect(host="127.0.0.1",
                                port="5432",
                                user="postgres", 
                                password="changeme",
                                database="postgres", 
                                options="-c search_path=dbo,q_manager")
  connection.set_session(autocommit=True)
  cursor = connection.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)

  def __init__(self):
    print('q helper init')
    pass
 
  def get_guid(self, *args):
    guid = ""
    for a in sys.argv:
      if "-guid=" in a: 
        guid = a.split('=')[1]
        break
    print('get_guid='+guid)
    return guid
  
  def task_start(self):
    # guid + pid -> Update Status To Start + Stampt TimeStart
    #TODO Get Task Infomation
    print('task_start')
    pass
  
  def task_stop(self):
    # guid + pid -> Update Status To Stop + Teminate Task + Stampt TimeStop 
    #TODO Get Task Infomation
    print('task_stop')
    pass

  def task_log(self, message): 
    #TODO Insert Logs -> Insert To Logs Table + Message
    print('task_log= '+  message)
    pass

  def task_error(self, error_title, error_message): 
    # guid + pid + error_title + error_message + Teminate Task + Stampt TimeStop + Change Status To Error
    print('task_error= '+ error_title, error_message)   
    pass
