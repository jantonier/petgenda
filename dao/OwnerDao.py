import psycopg2
from passlib.hash import pbkdf2_sha256
from config import dbconfig2

class OwnerDao:

    conn = psycopg2.connect(
        host=dbconfig2.host,
        port=dbconfig2.port,
        user=dbconfig2.user,
        password=dbconfig2.password,
        database=dbconfig2.database
    )

    def getAllOwners(self):
        cursor = self.conn.cursor()
        query = "select owner_id, name, lastname, email " \
                "from owner where is_deleted = false"
        try:
            cursor.execute(query,)
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def createOwner(self, name, lastname, email, password):
        cursor = self.conn.cursor()
        query = "select owner_id from owner where email = %s and is_deleted = false"
        try:
            cursor.execute(query, (email,))
        except psycopg2.Error as e:
            # self.conn.commit()
            return e
        result = cursor.fetchone()
        if result is not None:
            return "User already registered"
        hashedPassword = pbkdf2_sha256.hash(password)
        query = "insert into owner (name, lastname, email, password, is_deleted) values (%s, %s, %s, %s, false)"
        try:
            cursor.execute(query, (name, lastname, email, hashedPassword,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"

    def confirmPasswordByEmail(self, email, password):
        cursor = self.conn.cursor()
        query = "select password from owner where email = %s and is_deleted = false"
        try:
            cursor.execute(query, (email,))
        except psycopg2.Error as e:
            return
        result = cursor.fetchone()
        hashedPassword = result[0]
        response = pbkdf2_sha256.verify(password, hashedPassword)
        self.conn.commit()
        return response


    def getOwnerNameAndIdByEmail(self, email):
        cursor = self.conn.cursor()
        query = "select name, owner_id from owner where email = %s and is_deleted = false"
        try:
            cursor.execute(query, (email,))
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        # name = result[0]
        # owner_id = result[1]
        self.conn.commit()
        return result

    def getOwnerIdByEmail(self, email):
        cursor = self.conn.cursor()
        query = "select owner_id from owner where email = %s"
        try:
            cursor.execute(query, (email,))
        except psycopg2.Error as e:
            return
        result = cursor.fetchone()
        hashedPassword = result[0]
        self.conn.commit()
        return hashedPassword

    def getOwnerEmailInformation(self, email):
        cursor = self.conn.cursor()
        query = "select name, lastname, email from owner where email = %s"
        try:
            cursor.execute(query, (email,))
        except psycopg2.Error as e:
            return
        result = cursor.fetchone()
        #info = result[0]
        self.conn.commit()
        return result