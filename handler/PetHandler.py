from dao.OwnerDao import OwnerDao
from dao.PetDao import PetDao
from flask import jsonify
from Dictionary import *
import datetime
from pytz import timezone

# from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)

dateFormat = "%m-%d-%Y %H:%M:%S"
timeFormat = "%H:%M"

class PetHandler:
#-------------------------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------------------------
    def getLog(self, owner_id):
        dao = PetDao()
        if owner_id is None:
            return jsonify(Error="Malformed Request"), 400
        result = dao.getLog(owner_id)
        if not result:
            return jsonify("Your pets has no logs yet"), 204
        mapped_result = []
        for r in result:
            mapped_result.append(mapLogToDict(r)) 
        return jsonify(mapped_result), 200

    def getPetLog(self, json):
        dao = PetDao()
        pet_id = json.get("pet_id")
        if pet_id is None:
            return jsonify(Error="Malformed Request"), 400
        result = dao.getPetLog(pet_id)
        if not result:
            return jsonify("Your pet has no logs yet"), 204
        mapped_result = []
        for r in result:
            mapped_result.append(mapLogToDict(r)) 
        return jsonify(mapped_result), 200

    def createPetLog(self, json):
        dao = PetDao()
        action_id = json.get("action_id")
        now_PR = datetime.now(timezone('America/Puerto_Rico'))
        date = now_PR.strftime(dateFormat)

        if action_id is None or date is None:
            return jsonify(Error="Malformed Request"), 400
        
        result = dao.createPetLog(action_id, date)
        return jsonify(str(result))

    def deletePetLog(self, json):
        dao = PetDao()
        log_id = json.get("log_id")

        if log_id is None:
            return jsonify(Error="Malformed Request"), 400
        
        result = dao.deletePetLog(log_id)
        return jsonify(str(result))

    def updatePetLog(self, json):
        dao = PetDao()
        log_id = json.get("log_id")
        action_id = json.get("action_id")
        date = json.get("date")

        if log_id is None or action_id is None or date is None:
            return jsonify(Error="Malformed Request"), 400
        
        result = dao.updatePetLog(log_id, action_id, date)
        return jsonify(str(result))


    def createCalendar(self, json, owner_id): #Averiguar si el json viene con "null" en pet_id o si viene vacío
        dao = PetDao()
        date = json.get("date")
        pet_id = json.get("pet_id")
        event_name = json.get("event_name")

        if event_name is None or date is None or owner_id is None:  #Terminar!
            return jsonify(Error="Malformed Request"), 400
        if pet_id is None:
            result = dao.createCalendar(event_name, date, owner_id)
            return jsonify(str(result))
        else:
            result = dao.createPetCalendar(event_name, date, owner_id, pet_id)
            return jsonify(str(result))

    def getCalendar(self, owner_id): # verificar si funciona bien. Los que tienen pet y los que no
        dao = PetDao()
        if owner_id is None:
            return jsonify(Error="Malformed Request"), 400
        result = dao.getCalendar(owner_id)
        if not result:
            return jsonify("Your calendar has no events"), 204
        mapped_result = []
        for r in result:
            mapped_result.append(mapCalendarToDict(r)) 
        return jsonify(mapped_result), 200

    def deleteCalendar(self, json):
        dao = PetDao()
        calendar_id = json.get("calendar_id")

        if calendar_id is None:
            return jsonify(Error="Malformed Request"), 400
        
        result = dao.deleteCalendar(calendar_id)
        return jsonify(str(result))
    
    def updateCalendar(self, json):
        dao = PetDao()
        calendar_id = json.get("calendar_id")
        event_name = json.get("event_name")
        date = json.get("date")
        pet_id = json.get("pet_id")


        if calendar_id is None or event_name is None or date is None:
            return jsonify(Error="Malformed Request"), 400
        
        result = dao.updateCalendar(calendar_id, event_name, date, pet_id)
        return jsonify(str(result))