class Query():
    @staticmethod
    def select_all(table):
        return f"select * from {table}"

    @staticmethod
    def hashed_password(username):
        return f"select id, password from person where username = '{username}'"

    @staticmethod
    def insert_user(username, password, first_name, last_name, phone, street, city, zipcode):
        return f"insert into person(username, password, first_name, last_name, phone, street, city, zipcode)\
            values('{username}', '{password}', '{first_name}', '{last_name}', {phone}, '{street}', '{city}', '{zipcode}')"

    @staticmethod
    def insert_auction(title, description, minimum_price, end_time, product_id, product_description, person_id):
        return f"insert into auction(title, description, minimum_price, start_time, end_time, product_isbn, product_description, person_id)\
            values('{title}', '{description}', {minimum_price}, current_timestamp, '{end_time}', {product_id}, '{product_description}', '{person_id}')"

    @staticmethod
    def on_going_auctions():
        return f"select id, title, description from auction where end_time>current_timestamp"

    @staticmethod
    def get_user_auction(user_id, auction_id):
        return f"select * from auction where id = {auction_id} and person_id = {user_id}"

    @staticmethod
    def update_version(auction_id):
        return f"insert into version(title, description, edited, auction_id)\
            select a.title, a.description, current_timestamp, a.id\
            from auction a where a.id = {auction_id}"

    @staticmethod
    def update_auction(user_id, auction_id, data):
        query = "update auction set "
        
        for key in data:
            if isinstance(data[key], str):
                query += f"{key} = '{data[key]}',"
            else:
                query += f"{key} = {data[key]},"

        return f"{query[:-1]} where id = {auction_id} and person_id = {user_id}"

    @staticmethod
    def auction(auction_id):
        return f"select * from auction where id = {auction_id}"

    @staticmethod
    def insert_comment(auction_id, user_id, content):
        return f"insert into comment(person_id, auction_id, content, comment_date)\
            values({user_id}, {auction_id}, '{content}', current_timestamp)"

    @staticmethod
    def auction_keyword(keyword):
        return f"select a.id, a.description from auction a where a.product_description like '%{keyword}%' or a.product_isbn = '{keyword}'"

    @staticmethod
    def bid(auction_id):
        return f"select p.username, b.increase from bid b, person p where b.person_id = p.id and b.auction_id = {auction_id}"

    
    @staticmethod
    def person_auction(person_id):
        return f"select distinct concat(b.auction_id, a.id) from bid b, auction a where b.person_id = {person_id} and a.person_id = {person_id}"

    @staticmethod
    def comment(auction_id):
        return f"select p.username, c.content from comment c, person p where c.person_id = p.id and c.auction_id = {auction_id}"

    @staticmethod
    def add_bid(person_id, auction_id, increase):
        return f"begin; lock table bid in access exclusive mode;\
            insert into bid(auction_id, person_id, increase, bid_date)\
            select {auction_id}, {person_id}, {increase}, current_timestamp\
            where not exists\
            (select * from bid where auction_id = {auction_id} and increase >= {increase});\
            end;"

    @staticmethod
    def read_notifications(person_id):
        return f"update notification set seen = TRUE where person_id = {person_id} and seen = FALSE"

    @staticmethod
    def notifications(person_id):
        return f"select * from notification where person_id = {person_id}"

    @staticmethod
    def next_auction():
        return f"select min(end_time) from auction where winner_id is null"

    @staticmethod
    def end_auctions():
        return f"update auction a\
                set winner_id = coalesce((select a.id\
                from bid b\
                where a.id = b.auction_id and b.increase =\
                (select max(b2.increase) from bid b2 where a.id = b2.auction_id)\
                group by a.id), 0)\
                where winner_id is null and end_time < current_timestamp"
                