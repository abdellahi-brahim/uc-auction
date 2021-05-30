from flask import Flask
from flask_bcrypt import Bcrypt
from uc_auction.database import Database
from flask_json_schema import JsonSchema

#To-Do set env variables
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"

user = "fxizouxlthwjpl"
password = "fb9f0750ac21dcae788d6ed36f9125b37cb4aa0ebbe6d07b47f1009af9d1c2d3"
host = "ec2-34-254-69-72.eu-west-1.compute.amazonaws.com"
db = "d3uhmt1e2qo9g3"
port = "5432"

db = Database(user, password, host, db, port)
schema = JsonSchema(app)

from uc_auction import routes