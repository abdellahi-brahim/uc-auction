from functools import wraps
from flask.helpers import make_response
from uc_auction import app, schema, db
from uc_auction import schemas
from flask import request, jsonify
from flask_json_schema import JsonValidationError
from datetime import datetime, timedelta

import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return make_response(jsonify({'message' : 'Token is missing!'}), 401)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            username = data['id']
            
        except Exception:
            return make_response(jsonify({'message': 'Token is invalid'}), 401)
        return f(username, *args, **kwargs)

    return decorated

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]})

#Home page
@app.route("/")
def home():
    return "Welcome to uc-auction api"

#To-Do Login
@app.route("/user", methods=['PUT'])
@schema.validate(schemas.loginSchema)
def login():
    data = request.get_json()
    result = db.login(data)
    if result == False:
        return make_response(jsonify({"message":'Could not verify'}), 401, {'WWW-Authenticate' : 'Basic realm="Login Required!"'})

    print(result)

    expire = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode({'id':result, 'exp': expire}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

@app.route("/user", methods=['POST'])
@schema.validate(schemas.userSchema)
def register():
    "Receives a JSON object and creates user in database"
    data = request.get_json()
    result = db.register_user(data) 
    if result == True:
        return make_response(jsonify({"message":"User Created!"}), 200)
    return make_response(jsonify(result), 400)

#Debug Method
@app.route("/users", methods=['GET'])
def get_users():
    """Return JSON object with array with all users detailed information"""
    users = db.get_table("person")
    return jsonify({"users": users})

#To-Do Criar Eleição
@app.route("/auction", methods=['POST'])
@schema.validate(schemas.auctionSchema)
def create_auction():
    data = request.get_json()
    try:
        start = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S.%f')
        print(f"start_time: {start}")
        end = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S.%f')
        print(f"end_time: {end}")
    except ValueError as e:
        print(e)

    return jsonify(data)

#To-Do Pesquisar um leilão dado um id
@app.route("/auction/<auction_id>", methods=['GET'])
def get_auction(auction_id):
    return jsonify({"auction_id": auction_id})

#To-Do Editar propriedades dum leilão
@app.route("/auction/<auction_id>", methods = ['POST'])
def edit_auction(auction_id):
    return jsonify({"auction_id": auction_id})

#To-Do Mural Comments
@app.route("/auction/comment", methods=['PUT'])
def comment():
    data = request.get_json()
    return jsonify(data)

#To-Do Retornar todas as eleições
@app.route("/auctions", methods=['GET'])
def get_all_auctions():
    return jsonify({'auctions':['All Auctions']})

#To-Do Retornar uma eleição com base numa keyword
@app.route("/auctions/<keyword>", methods=['GET'])
def get_auctions(keyword):
    return jsonify({'keyword':keyword})

#To-Do Criar uma licitação num leilão
@app.route("/bid/<auction_id>/<bid>", methods=['PUT'])
def bid(auction_id, bid):
    return jsonify({'auction_id': auction_id, 'bid': bid})

#To-Do Endpoint with all notifications
@app.route("/user/notifications", methods=['GET'])
def notifications():
    return jsonify({"Notifications" :['All notifications']})


