import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import TRANSACTION_STATUS_ACTIVE

class db_class:
    connection = None
    cursor = None

    def __init__(self):
        if self.cursor == None:
            self.connection = psycopg2.connect(host="127.0.0.1",
                                    port="5432",
                                    user="postgres", 
                                    password="Password12345",
                                    database="postgres", 
                                    options="-c search_path=dbo,q_manager")
            self.connection.set_session(autocommit=True)
            self.cursor = self.connection.cursor(cursor_factory = RealDictCursor)
        pass