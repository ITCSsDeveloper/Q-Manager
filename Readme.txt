ใน mac os  ใช้ keyword
python3, pip3


install python3 (mac os) 
- brew install python3

upgrade pip 
- python3 -m pip install --upgrade pip

install  virtual enviroment (pipenv)
- pip3 install pipenv

create folder django
- mkdir django
- cd django/

install django
- pipenv install django==3.1.5

activate virtual enviroment (เข้าสู่โหมดการทำงานของ virtual environment)
- pipenv shell
- เมื่อเข้าสำเร็จ ข้างหน้าจะมี (ชื่อโปรเจค)
- เราจะสั่ง pip install หรือ รันคำสั่งติดตั้งทุกอย่างไว้ในโหมดนี้
- ถ้าต้องการออก พิมพ์ exit


create project django   ( . คือ ระบุให้สร้างที่ pwd  )
- djando-admin startproject {project_name} . 


คำสั่ง ตรวจสอบโครงสร้างโปรเจค
- tree
- brew install tree ( mac os )
.
├── Pipfile
├── Pipfile.lock
├── manage.py
└── q_manager
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
1 directory, 8 files


Warning เตือน ว่ายังไม่ได้ทำการสร้าง migration จะทำให้ ฟีเจอร์ทั้งบางตัวไม่สามารถใช้งานได้
You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.


Select python interprinter 
VS Code -> some.py -> View -> Command Palett -> python interprinter (Select)

Install Extension On VS Code
- https://marketplace.visualstudio.com/items?itemName=ms-python.python
- เพื่อช่วยแสดง intelliSense หรือ Code Formatting



ถ้าจะเชื่อมต่อ database  ให้ใช้ 
- pipenv install psycopg2
- pipenv install psycopg2-binary (mac, windows)

connection string เชื่อมต่อ  mongoDb
- mongodb://{username}:{password}@{host}:{port}



python3 main.py -file_name={DIR_TASK}/data/LA00000.GCC -map_file_name={DIR_TASK}/data/LA00000.MAP -limit=100 -header=HT -body=DT -footer=FT -guid={GUID}
python3 /Users/ratchanonc1/Documents/GitHub/Q-Manager/Disk0/Task1.py -file_name=/Users/ratchanonc1/Documents/GitHub/Q-Manager/Disk0/data/LA00000.GCC -map_file_name=/Users/ratchanonc1/Documents/GitHub/Q-Manager/Disk0/data/LA00000.MAP -limit=100 -header=HT -body=DT -footer=FT -guid=9adb73ebabfa49fe9dd49f4d8f930675