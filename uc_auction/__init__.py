from flask import Flask
from flask_bcrypt import Bcrypt
from uc_auction.database import Database
from flask_json_schema import JsonSchema

#To-Do set env variables
app = Flask(__name__)

app.config['SECRET_KEY'] = "secret_key"
app.config['USER'] = "fxizouxlthwjpl"
app.config['PASSWORD'] = "fb9f0750ac21dcae788d6ed36f9125b37cb4aa0ebbe6d07b47f1009af9d1c2d3"
app.config['HOST'] = "ec2-34-254-69-72.eu-west-1.compute.amazonaws.com"
app.config['DB'] = "d3uhmt1e2qo9g3"
app.config['PORT'] = "5432"

db = Database(app.config['USER'], app.config['PASSWORD'], app.config['HOST'], app.config['DB'], app.config['PORT'])
schema = JsonSchema(app)

from uc_auction import routes