from dao.OwnerDao import OwnerDao
from dao.PetDao import PetDao
from flask import jsonify
from Dictionary import *
import datetime

from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)


class PetHandler:

    def createPet(self, json, owner_id):
        dao = PetDao()
        pet_name = json.get("pet_name")
        pet_birthdate = json.get("pet_birthdate")
        pet_type = json.get("pet_type")

        if pet_name is None or pet_birthdate is None or pet_type is None:
            return jsonify(Error="Malformed Request"), 400
        
        result = dao.createPet(owner_id, pet_name, pet_birthdate, pet_type)
        return jsonify(str(result))

    def getMyPets(self, owner_id):
        dao = PetDao()
        result = dao.getMyPets(owner_id)
        if not result:
            return jsonify("You have no pets registered"), 204
        mapped_result = []
        for r in result:
            mapped_result.append(mapPetToDict(r))
        return jsonify(mapped_result), 200

    def deletePet(self, json, owner_id):
        dao = PetDao()
        pet_id = json.get("pet_id")
        if pet_id is None:
            return jsonify(Error="Malformed Request"), 400
        result = dao.deletePet(owner_id, pet_id)
        return jsonify(str(result))

    def updatePet(self, json):
        dao = PetDao()
        pet_id = json.get("pet_id")
        pet_name = json.get("pet_name")
        pet_birthdate = json.get("pet_birthdate")
        pet_type = json.get("pet_type")

        if pet_name is None or pet_birthdate is None or pet_type is None or pet_id is None:
            return jsonify(Error="Malformed Request"), 400
        
        result = dao.updatePet(pet_id, pet_name, pet_birthdate, pet_type)
        return jsonify(str(result))

    def getPetActions(self, json):
        dao = PetDao()
        pet_id = json.get("pet_id")
        if pet_id is None:
            return jsonify(Error="Malformed Request"), 400
        result = dao.getPetActions(pet_id)
        if not result:
            return jsonify("Your pet has no actions associated with"), 204
        mapped_result = []
        for r in result:
            mapped_result.append(mapActionToDict(r)) 
        return jsonify(mapped_result), 200

    def createPetAction(self, json):
        dao = PetDao()
        action_name = json.get("action_name")
        pet_id = json.get("pet_id")

        if pet_id is None or action_name is None:
            return jsonify(Error="Malformed Request"), 400
        
        result = dao.createPetAction(action_name, pet_id)
        return jsonify(str(result))

    def deletePetAction(self, json):
        dao = PetDao()
        action_id = json.get("action_id")

        if action_id is None:
            return jsonify(Error="Malformed Request"), 400
        
        result = dao.deletePetAction(action_id)
        return jsonify(str(result))

    def updatePetAction(self, json):
        dao = PetDao()
        action_name = json.get("action_name")
        action_id = json.get("action_id")

        if action_id is None or action_name is None:
            return jsonify(Error="Malformed Request"), 400
        
        result = dao.updatePetAction(action_name, action_id)
        return jsonify(str(result))