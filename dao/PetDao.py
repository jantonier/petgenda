import psycopg2
from passlib.hash import pbkdf2_sha256
from config import dbconfig2

class PetDao:

    conn = psycopg2.connect(
        host=dbconfig2.host,
        port=dbconfig2.port,
        user=dbconfig2.user,
        password=dbconfig2.password,
        database=dbconfig2.database
    )

    def createPet(self, owner_id, pet_name, pet_birthdate, pet_type):
        cursor = self.conn.cursor()
        query = "insert into pet (pet_name, pet_birthdate, pet_type, pet_is_deleted) values (%s, %s, %s, false) returning pet_id"
        try:
            cursor.execute(query, (pet_name, pet_birthdate, pet_type,))
        except psycopg2.Error as e:
            # self.conn.commit()
            return e
        result = cursor.fetchone()
        if result is None:
            self.conn.rollback()
            return "There was a problem creating pet"
        pet_id = result[0]
        query = "insert into owns (owner_id, pet_id, creator, confirmed, owns_is_deleted) values (%s, %s, true, true, false)"
        try:
            cursor.execute(query, (owner_id, pet_id,))
        except psycopg2.Error as e:
            self.conn.rollback()
            return e
        self.conn.commit()
        return "Done"

    def getMyPets(self, owner_id):
        cursor = self.conn.cursor()
        query = "select pet_id, pet_name, pet_type, pet_photo, creator from pet natural inner join owns where owner_id = %s and pet_is_deleted = false and confirmed = true"
        try:
            cursor.execute(query, (owner_id,))
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def deletePet(self, owner_id, pet_id):
        cursor = self.conn.cursor()
        query = "select creator from owns where pet_id = %s and owner_id = %s"
        try:
            cursor.execute(query, (pet_id, owner_id,))
        except psycopg2.Error as e:
            return e
        result = cursor.fetchone()
        if result[0] is True:
            query = "update pet set pet_is_deleted = true where pet_id = %s"
            try:
                cursor.execute(query, (pet_id,))
            except psycopg2.Error as e:
                self.conn.rollback()
                return e
            query = "update owns set owns_is_deleted = true where pet_id = %s"
            try:
                cursor.execute(query, (pet_id,))
            except psycopg2.Error as e:
                self.conn.rollback()
                return e
            self.conn.commit()
            return "Done"
        else:
            query = "update owns set owns_is_deleted = true where pet_id = %s and owner_id = %s"
            try:
                cursor.execute(query, (pet_id, owner_id,))
            except psycopg2.Error as e:
                self.conn.rollback()
                return e
            self.conn.commit()
            return "Done"

    def updatePet(self, pet_id, pet_name, pet_birthdate, pet_type):
        cursor = self.conn.cursor()
        query = "update pet set pet_name = %s, pet_birthdate = %s, pet_type = %s where pet_id = %s"
        try:
            cursor.execute(query, (pet_name, pet_birthdate, pet_type, pet_id,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"

    def getPetActions(self, pet_id):
        cursor = self.conn.cursor()
        query = "select action_id, action_name from action where pet_id = %s and action_is_deleted = false"
        try:
            cursor.execute(query, (pet_id,))
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def createPetAction(self, action_name, pet_id):
        cursor = self.conn.cursor()
        query = "insert into action (pet_id, action_name, action_is_deleted) values (%s, %s, false)"
        try:
            cursor.execute(query, (pet_id, action_name,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"

    def deletePetAction(self, action_id):
        cursor = self.conn.cursor()
        query = "update action set action_is_deleted = true where action_id = %s"
        try:
            cursor.execute(query, (action_id,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"

    def updatePetAction(self, action_name, action_id):
        cursor = self.conn.cursor()
        query = "update action set action_name = %s where action_id = %s"
        try:
            cursor.execute(query, (action_name, action_id,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"

    def getLog(self, owner_id):
        cursor = self.conn.cursor()
        query = "select log_id, pet_name, action_name, date from log natural inner join action natural inner join owns where owner_id = %s and log_is_deleted = false and confirmed = true"
        try:
            cursor.execute(query, (owner_id,))
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPetLog(self, pet_id):
        cursor = self.conn.cursor()
        query = "select log_id, pet_name, action_name, date from log natural inner join action natural inner join owns where pet_id = %s and log_is_deleted = false and confirmed = true"
        try:
            cursor.execute(query, (pet_id,))
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def createPetLog(self, action_id, date):
        cursor = self.conn.cursor()
        query = "insert into log (action_id, date, log_is_deleted) values (%s, %s, false)"
        try:
            cursor.execute(query, (action_id, date,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"

    def deletePetLog(self, log_id):
        cursor = self.conn.cursor()
        query = "update log set log_is_deleted = true where log_id = %s"
        try:
            cursor.execute(query, (log_id,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"

    def updatePetLog(self, log_id, action_id, date):
        cursor = self.conn.cursor()
        query = "update log set action_id = %s, date = %s where log_id = %s"
        try:
            cursor.execute(query, (action_id, date, log_id,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"

    def createCalendar(self, event_name, date, owner_id):
        cursor = self.conn.cursor()
        query = "insert into calendar (event_name, date, owner_id, calendar_is_deleted) values (%s, %s, %s, false)"
        try:
            cursor.execute(query, (event_name, date, owner_id,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"

    def createPetCalendar(self, event_name, date, owner_id, pet_id):
        cursor = self.conn.cursor()
        query = "insert into calendar (event_name, date, owner_id, pet_id, calendar_is_deleted) values (%s, %s, %s, %s, false)"
        try:
            cursor.execute(query, (event_name, date, owner_id, pet_id,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"

    def getCalendar(self, owner_id):
        cursor = self.conn.cursor()
        query = "select calendar_id, event_name, date, owner_id, pet_id from calendar natural inner join owns natural inner join pet where owner_id = %s and calendar_is_deleted = false and confirmed = true and owns_is_deleted = false"
        try:
            cursor.execute(query, (owner_id,))
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def deleteCalendar(self, calendar_id):
        cursor = self.conn.cursor()
        query = "update calendar set calendar_is_deleted = true where calendar_id = %s"
        try:
            cursor.execute(query, (calendar_id,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"

    def updateCalendar(self, calendar_id, event_name, date, pet_id):
        cursor = self.conn.cursor()
        query = "update calendar set event_name = %s, date = %s, pet_id = %s where calendar_id = %s"
        try:
            cursor.execute(query, (event_name, date, pet_id, calendar_id,))
        except psycopg2.Error as e:
            return e
        self.conn.commit()
        return "Done"