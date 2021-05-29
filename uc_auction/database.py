from datetime import datetime, timezone
import psycopg2
    
class Query():
    @staticmethod
    def select_all(table):
        return f"select * from {table}"

    @staticmethod
    def insert_user(username, password, first_name, last_name, phone, street, city, zipcode):
        return f"insert into person(username, password, first_name, last_name, phone, street, city, zipcode)\
            values({username}, {password}, {first_name}, {last_name}, {phone}, {street}, {city}, {zipcode})"

    @staticmethod
    def insert_auction(title, description, minimum_price, start_time, end_time, product_id, product_description, person_id):
        return f"insert into auction(title, description, minimum_price, start_time, end_time, product_id, product_description, person_id)\
            values({title}, {description}, {minimum_price}, {start_time}, {end_time}, {product_id}, {product_description}, {person_id})"

    @staticmethod
    def on_going_auctions():
        cur_date = datetime.now(timezone.utc)
        return f"select * from auction where end_time::date>{cur_date}"

class Database():
    def __init__(self, user, password, host, db, port):
        self.user = user
        self.password = password
        self.host = host
        self.db = db
        self.port = port 

    def connect(func):
        def inner(self, *args, **kwargs):
            connection = psycopg2.connect(user=self.user,password=self.password,host=self.host,port=self.port, database=self.db)
            result = func(self, connection, *args, **kwargs)
            connection.close()
            return result
        return inner

    @connect 
    def get_table(self, connection, table):
        with connection.cursor() as cursor:
            query = Query.select_all(table)
            cursor.execute(query)
            return [dict(zip([column[0] for column in cursor.description], row))
             for row in cursor.fetchall()]

    @connect 
    def get_on_going_auctions(self, connection):
        with connection.cursor() as cursor:
            query = Query.on_going_auctions()
            cursor.execute(query)
            return {"On Going Auctions": [dict(zip([column[0] for column in cursor.description], row))
             for row in cursor.fetchall()]}


    