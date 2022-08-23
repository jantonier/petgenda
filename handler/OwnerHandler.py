from dao.OwnerDao import OwnerDao
from flask import jsonify
from Dictionary import *
import datetime
from handler.EmailHandler import EmailHandler

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

    def login(self, json):
        dao = OwnerDao()
        if json is None:
            return jsonify(Error="Malformed Request"), 400
        email = json.get('email')
        password = json.get('password')
        if email is None or password is None:
            return jsonify(Error="Malformed Request"), 400
        #verificamos si el admin existe
        result = dao.getOwnerNameAndIdByEmail(email)
        if len(result) == 0:
            return jsonify(Error="User not registered"), 404

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

    def forgotPassword(self, json):
        email = json.get('email')
        if email is None:
            return jsonify(Error="Malformed request"), 400
        dao = OwnerDao()
        # password = dao.getOwnerPasswordByEmail(email)
        ownerInfo = dao.getOwnerEmailInformation(email)
        if ownerInfo is None:
            return jsonify(Error="Email is not registered as an user"), 404
        expires = datetime.timedelta(minutes=10)
        access_token = create_access_token(identity=email, expires_delta=expires)
        mapped_ownerInfo = []
        mapped_ownerInfo.append(mapOwnerInfoToDict(ownerInfo))
        emailHandler = EmailHandler()
        subject = "Petgenda: Password Change Request"
        html = "Saludos, hemos recibido su solicitud para cambiar su contraseña. " \
               "<br>Si usted no hizo esta solicitud, haga caso omiso a este mensaje. " \
               "<br>Para cambiar su contraseña, favor de presionar el siguiente enlace:" \
               "<br>http://google.com/"+access_token
        result = emailHandler.sendEmail(subject, mapped_ownerInfo, html)
        return jsonify(result)

    def sharePet(self, json, owner_id):
        dao = OwnerDao()

        pet_id = json.get('pet_id')
        target_email = json.get('email')
        
        if pet_id is None or target_email is None:
            return jsonify(Error="Malformed Request"), 400

        target_id = dao.getOwnerIdByEmail(target_email)
        if target_email is None:
            return jsonify(Error="User not registered"), 400

        
        result = dao.createSharedOwner(name, lastname, email, password) #Terminar
        return jsonify(result)