from flask_sqlalchemy import SQLAlchemy
import psycopg2
    
class Query():
    @staticmethod
    def select_all(table):
        return f"select * from {table}"

class Database():
    def __init__(self, user, password, host, db):
        self.user = user
        self.password = password
        self.host = host
        self.db = db
    
    def connect(func):
        def inner(self, *args, **kwargs):
            connection = psycopg2.connect(user=self.user,password=self.password,host=self.host,port=self.port, database=self.db)
            func(self, connection, *args, **kwargs)
            connection.close()
        return inner
    
    @connect 
    def get_table(self, connection, table):
        print(connection)
        print(Query.all(table))

    