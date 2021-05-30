from functools import wraps
from flask.helpers import make_response
from uc_auction import app, schema, db
from uc_auction import schemas
from flask import request, jsonify
from flask_json_schema import JsonValidationError
from datetime import datetime, timedelta

import jwt

def token_required(f):
    """Wrapper that ensures that request has a valid token in header. Returns user_id"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return make_response(jsonify({'message' : 'Token is missing!'}), 401)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['id']
            
        except Exception:
            return make_response(jsonify({'message': 'Token is invalid'}), 401)
        return f(user_id, *args, **kwargs)

    return decorated

@app.errorhandler(JsonValidationError)
def validation_error(e):
    """Validates JSON data, check if all required fields are present and if they are in correct format"""
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]})

#Home page
@app.route("/")
def home():
    return "Welcome to uc-auction api"

@app.route("/user", methods=['PUT'])
@schema.validate(schemas.loginSchema)
def login():
    """Returns jwt token with 30 minutes validity if credentials are correct"""
    data = request.get_json()
    result = db.login(data)
    if isinstance(result, str):
        return make_response(jsonify({"message":result}), 401, {'WWW-Authenticate' : 'Basic realm="Login Required!"'})

    expire = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode({'id':result, 'exp': expire}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

@app.route("/user", methods=['POST'])
@schema.validate(schemas.userSchema)
def register():
    """Receives a JSON object with user data and creates user in database"""
    data = request.get_json()
    result = db.register_user(data) 
    if result == True:
        return make_response(jsonify({"message":"User Created!"}), 200)
    return make_response(jsonify(result), 401)


@app.route("/users", methods=['GET'])
def get_users():
    """Return JSON object with array with all users detailed information"""
    users = db.get_table("person")
    return jsonify({"users": users})

@app.route("/auction", methods=['POST'])
@schema.validate(schemas.auctionSchema)
@token_required
def create_auction(user_id):
    """Receives a JSON object with auction data and creates auction in database"""
    data = request.get_json()
    try:
        data['start_time'] = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S.%f')
        data['end_time'] = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S.%f')
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), 401)
    
    data['person_id'] = user_id
    result = db.create_election(data)

    if result == True:
        return make_response(jsonify({"message":"Auction Created!"}), 200)

    return make_response(jsonify(result), 401)

@app.route("/auction/<auction_id>", methods=['GET'])
@token_required
def get_auction(_, auction_id):
    """Returns the auction details which id corresponds to auction_id"""
    result = db.get_auction_by_id(auction_id)
    return jsonify(result)

#To-Do Verify json input
@app.route("/auction/<auction_id>", methods = ['POST'])
@token_required
def edit_auction(user_id, auction_id):
    data = request.get_json()
    result = db.edit_auction(user_id, auction_id, data)
    return jsonify(result)

#To-Do Notify all users about auction
@app.route("/auction/comment", methods=['PUT'])
@token_required
def comment(user_id):
    data = request.get_json()
    result = db.post_comment(user_id, data)
    return jsonify(result)

@app.route("/auctions", methods=['GET'])
@token_required
def get_all_auctions(user_id):
    """Return JSON object with array with all auctions detailed information"""
    auctions = db.get_table("auction")
    return jsonify({"auctions": auctions})

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


