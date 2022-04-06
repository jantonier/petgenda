from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from config import dbconfig
from handler.OwnerHandler import OwnerHandler
from handler.PetHandler import PetHandler
app = Flask(__name__)
CORS(app)

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app.secret_key = os.urandom(12)
app.config['JWT_SECRET_KEY'] = os.urandom(12)
jwt = JWTManager(app)

@app.route("/")
@jwt_required()
def hello_world():
    identity = get_jwt_identity()
    return jsonify("Welcome to Petgenda API "+ str(identity))

@app.route('/owner', methods=['GET', 'POST', 'DELETE'])
def owners():
    if request.method == 'GET':
        return OwnerHandler().getAllOwners()
    if request.method == 'POST':
        return OwnerHandler().createOwner(request.json)
    if request.method == 'DELETE':
    #else:
        return OwnerHandler().deleteOwner(request.json) #ToDo (pets, actions, logs, calendars)

@app.route('/mypets', methods=['GET', 'POST', 'DELETE', 'PUT'])
@jwt_required()
def myPets():
    identity = get_jwt_identity()
    if request.method == 'GET':
        return PetHandler().getMyPets(identity)
    if request.method == 'POST':
        return PetHandler().createPet(request.json, identity)
    if request.method == 'DELETE':
        return PetHandler().deletePet(request.json, identity) #falta probar cuando es un shared pet y borrar logs y actions
    if request.method == 'PUT':
        return PetHandler().updatePet(request.json)

@app.route('/action', methods=['GET', 'POST', 'DELETE', 'PUT']) #falta probar todos
@jwt_required()
def petActions():
    if request.method == 'GET':
        return PetHandler().getPetActions(request.json)
    if request.method == 'POST':
        return PetHandler().createPetAction(request.json)
    if request.method == 'DELETE':
        return PetHandler().deletePetAction(request.json) 
    if request.method == 'PUT':
        return PetHandler().updatePetAction(request.json)

@app.route('/log', methods=['GET', 'POST', 'DELETE', 'PUT']) #falta probar todos
@jwt_required()
def petActions():
    identity = get_jwt_identity()
    if request.method == 'GET':
        return PetHandler().getLog(request.json)
    # if request.method == 'POST':                               #hay que ver si esto se usará
    #     return PetHandler().createPetAction(request.json)
    # if request.method == 'DELETE':
    #     return PetHandler().deletePetAction(request.json) 
    # if request.method == 'PUT':
    #     return PetHandler().updatePetAction(request.json)

@app.route('/petlog', methods=['GET', 'POST', 'DELETE', 'PUT']) #falta probar todos
@jwt_required()
def petActions():
    identity = get_jwt_identity()
    if request.method == 'GET':
        return PetHandler().getPetLog(request.json)
    if request.method == 'POST':
        return PetHandler().createPetLog(request.json)
    if request.method == 'DELETE':
        return PetHandler().deletePetLog(request.json) 
    if request.method == 'PUT':
        return PetHandler().updatePetLog(request.json)

@app.route("/login")
def login():
    return OwnerHandler().login(request.json)

if __name__ == '__main__':
    app.run(debug=False)