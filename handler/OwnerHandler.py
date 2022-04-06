from dao.OwnerDao import OwnerDao
from flask import jsonify
from Dictionary import *
import datetime

from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)


class OwnerHandler:

    def getAllOwners(self):
        dao = OwnerDao()
        result = dao.getAllOwners()
        if not result:
            return jsonify("Nada")
        mapped_result = []
        for r in result:
            mapped_result.append(mapOwnerToDict(r))
        return jsonify(mapped_result)

    def createOwner(self, json):
        dao = OwnerDao()

        name = json.get('name')
        lastname = json.get('lastname')
        email = json.get('email')
        password = json.get('password')
        
        if name is None or lastname is None or email is None or password is None:
            return jsonify(Error="Malformed Request"), 400
        # getOwnerIdByEmail(email)
        result = dao.createOwner(name, lastname, email, password)
        return jsonify(result)

    # def getOwnerIdByEmail(self, email):
    #     dao = OwnerDao()
    #     return 

    def login(self, json):
        dao = OwnerDao()
        email = json.get('email')
        password = json.get('password')
        if email is None or password is None:
            return jsonify(Error="Malformed Request"), 400
        #verificamos si el admin existe
        result = dao.getOwnerNameAndIdByEmail(email)
        name = result[0][0]
        owner_id = result[0][1]

        if owner_id is None:
            return jsonify(Error="User not registered"), 404

        # role = dao.getAdminRoleByEmail(email)

        passConfirmed = dao.confirmPasswordByEmail(email, password)

        if passConfirmed:
            expires = datetime.timedelta(hours=3)
            access_token = create_access_token(identity=owner_id, expires_delta=expires)
        else:
            return jsonify(Error="Incorrect login information"), 401

        result = mapLoginToDict(name, access_token)

        return jsonify(result), 200