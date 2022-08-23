from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from config import dbconfig
from handler.OwnerHandler import OwnerHandler
from handler.PetHandler import PetHandler
from datetime import datetime
from pytz import timezone
app = Flask(__name__)
CORS(app)

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

dateFormat = "%m-%d-%Y %H:%M:%S"
timeFormat = "%H:%M"

app.secret_key = os.urandom(12)
app.config['JWT_SECRET_KEY'] = os.urandom(12)
jwt = JWTManager(app)

@app.route("/")
# @jwt_required()
def hello_world():
    now_PR = datetime.now(timezone('America/Puerto_Rico'))
    # identity = get_jwt_identity()
    return jsonify("Welcome to Petgenda API and date is: "+ now_PR.strftime(dateFormat))

@app.route("/checklogin")
@jwt_required()
def checklogin():
    now_PR = datetime.now(timezone('America/Puerto_Rico'))
    identity = get_jwt_identity()
    return jsonify("Welcome to Petgenda API. id is "+str(identity)+" and date is: "+ now_PR.strftime(dateFormat))

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
def logs():
    identity = get_jwt_identity()
    if request.method == 'GET':
        return PetHandler().getLog(identity)
    # if request.method == 'POST':                               #hay que ver si esto se usará
    #     return PetHandler().createPetAction(request.json)
    # if request.method == 'DELETE':
    #     return PetHandler().deletePetAction(request.json) 
    # if request.method == 'PUT':
    #     return PetHandler().updatePetAction(request.json)

@app.route('/petlog', methods=['GET', 'POST', 'DELETE', 'PUT']) #falta probar todos
@jwt_required()
def petLogs():
    if request.method == 'GET':
        return PetHandler().getPetLog(request.json)
    if request.method == 'POST':
        return PetHandler().createPetLog(request.json)
    if request.method == 'DELETE':
        return PetHandler().deletePetLog(request.json) 
    if request.method == 'PUT':
        return PetHandler().updatePetLog(request.json)

@app.route('/calendar', methods=['GET', 'POST', 'DELETE', 'PUT']) #Pere hacerlo relacionado a ambos (mascota o peronal) 
#se le hace el campo de pet_id y si tiene algo diferente a nulo, es de la mascota
@jwt_required()
def calendar():
    identity = get_jwt_identity()
    if request.method == 'GET':
        return PetHandler().getCalendar(request.json, identity)
    if request.method == 'POST':
        return PetHandler().createCalendar(request.json, identity)
    if request.method == 'DELETE':
        return PetHandler().deleteCalendar(request.json)
    if request.method == 'PUT':
        return PetHandler().updateCalendar(request.json)

@app.route("/sharepet")
@jwt_required()
def sharePet():
    identity = get_jwt_identity()
    return OwnerHandler().sharePet(request.json, identity)

@app.route("/login", methods=['GET', 'POST'])
def login():
    return OwnerHandler().login(request.json)

@app.route("/forgotpassword")
def forgotPassword():
    return OwnerHandler().forgotPassword(request.json)

if __name__ == '__main__':
    app.run(debug=False)