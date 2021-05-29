from flask import Flask
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from uc_auction.database import Database
from flask_json_schema import JsonSchema

app = Flask(__name__)
db = Database("user", "password", "host", "db")
auth = HTTPBasicAuth()
schema = JsonSchema(app)

from uc_auction import routes