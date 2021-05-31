from uc_auction.queries import Query

import psycopg2

class Database():
    def __init__(self, user, password, host, db, port):
        self.user = user
        self.password = password
        self.host = host
        self.db = db
        self.port = port 

    def connect(func):
        def inner(self, *args, **kwargs):
            with psycopg2.connect(user=self.user,password=self.password,host=self.host,port=self.port, database=self.db) as connection:
                try:
                    result = func(self, connection, *args, **kwargs)
                except Exception as e:
                    result = {"error": str(e)}
                    connection.rollback()
                return result
        return inner

    @connect 
    def login(self, connection, data):
        query = Query.hashed_password(data['username'])
        with connection.cursor() as cursor:
            cursor.execute(query)
            #No username found or wrong password
            if cursor.rowcount < 1:
                return "Username Not Found"

            user_id, hashed_password = cursor.fetchone()
            
            if hashed_password != data['password']:
                print(f"{hashed_password} == {data['password']}")
                return "Wrong Password"

            return int(user_id)

    @connect
    def register_user(self, connection, data):
        query = Query.insert_user(data['username'],data['password'],data['first_name'],data['last_name'],data['phone'],data['street'],data['city'],data['zipcode'])  
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            return True

    @connect
    def create_election(self, connection, data):
        query = Query.insert_auction(data['title'], data['description'], data['minimum_price'], data['start_time'], data['end_time'], data['product_id'], data['product_description'], data['person_id'])
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            return True

    @connect 
    def get_table(self, connection, table):
        query = Query.select_all(table)
        with connection.cursor() as cursor:
            cursor.execute(query)
            return [dict(zip([column[0] for column in cursor.description], row))
             for row in cursor.fetchall()]

    @connect 
    def get_on_going_auctions(self, connection):
        query = Query.on_going_auctions()
        with connection.cursor() as cursor:
            cursor.execute(query)
            
            if cursor.rowcount < 1:
                return {"message": "No on going auction found!"}

            return {"On Going Auctions": [dict(zip([column[0] for column in cursor.description], row))
             for row in cursor.fetchall()]}

    @connect
    def get_auction_by_id(self, connection, auction_id):
        query = Query.auction(auction_id)
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.rowcount < 1:
                return {"message": "No auction found!"}
            return dict(zip([column[0] for column in cursor.description], cursor.fetchone()))
    
    @connect 
    def edit_auction(self, connection, user_id, auction_id, data):
        #Verify if auction's author is user_id
        query = Query.get_user_auction(user_id, auction_id)
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.rowcount < 1:
                return {"message": "access forbiden"}
        
        #Insert Previous Info in Version Table
        version_query = Query.update_version(auction_id)
        #Update Table values query
        auction_query = Query.update_auction(user_id, auction_id, data)
        with connection.cursor() as cursor:
            cursor.execute(version_query)
            cursor.execute(auction_query)
            #Commit transation
            connection.commit()

        return {"message": "auction updated successfully"}

    @connect 
    def post_comment(self, connection, user_id, data):
        query = Query.insert_comment(data['auction_id'], user_id, data['content'])
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

        return{"message": "comment posted successfully"}

    @connect 
    def get_auction_by_keyword(self, connection, keyword):
        query = Query.auction_keyword(keyword)
        with connection.cursor() as cursor:
            cursor.execute(query)
            
            if cursor.rowcount < 1:
                return {"message": "No auction found!"}
            
            return {"Auctions": [dict(zip([column[0] for column in cursor.description], row))
            for row in cursor.fetchall()]}

    @connect
    def add_bid(self, connection, user_id, auction_id, increase):
        query = Query.add_bid(user_id, auction_id, increase)
        with connection.cursor() as cursor:
            cursor.execute(query)

        return {"message": "bid commited successfully"}

    @connect
    def get_notifications(self, connection, user_id):
        notif_query = Query.notifications(user_id)
        update_query = Query.read_notifications(user_id)

        with connection.cursor() as cursor:
            cursor.execute(notif_query)

            notif = {"Notifications": [dict(zip([column[0] for column in cursor.description], row))
                for row in cursor.fetchall()]}

            cursor.execute(update_query)
            connection.commit()
        
        return notif

    @connect 
    def get_next_auction(self, connection):
        query = Query.next_auction()
        with connection.cursor() as cursor:
            cursor.execute(query)

            if cursor.rowcount < 1:
                return {"message": "no auction selected"}

            return {"next": cursor.fetchone()[0]}

    @connect 
    def end_auctions(self, connection):
        query = Query.end_auctions()
        with connection.cursor() as cursor:
            cursor.execute(query)
        
        return {"success": "auctions ended"} 