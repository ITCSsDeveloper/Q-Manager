import os
import sys
import time
import psycopg2
import psycopg2.extras

class Task :
  q = QHelper
  pid = ""
  guid = ""

  def __init__(self):
    self.q = QHelper()
    self.pid = os.getpid()
    self.guid = self.q.get_guid(sys.argv)

  def start(self):
      try:
          self.q.task_start()
          for x in range(0, 10):
            print("We're on time %d" % (x))
            time.sleep(1)
      except:
        selg.q.task_error('title error', 'error_message')
        print("Unexpected error:", sys.exc_info()[0])
        raise
      finally:
        self.q.task_stop()
        print('finaly')


# Init And Start Task 
task1 = Task()
task1.start()
del task1







