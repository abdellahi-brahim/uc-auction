from uc_auction import app, schema
from uc_auction import schemas
from flask import request, jsonify
from flask_json_schema import JsonValidationError
from datetime import datetime

import re

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
    return jsonify(data)

#To-Do Registar Utilizador
@app.route("/user", methods=['POST'])
@schema.validate(schemas.userSchema)
def register():
    data = request.get_json()
    return jsonify(data)

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

#To-Do Pesquisar uma eleição dado um id
@app.route("/auction/<id>", methods=['GET'])
def get_auction(id):
    return jsonify({"auction_id": id})

#To-Do Retornar todas as eleições
@app.route("/auctions", methods=['GET'])
def get_all_auctions():
    return jsonify({'auctions':['All Auctions']})

#To-Do Retornar uma eleição com base numa keyword
@app.route("/auctions/<keyword>", methods=['GET'])
def get_auctions(keyword):
    return jsonify({'keyword':keyword})
