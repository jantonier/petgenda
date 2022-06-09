

def mapOwnerToDict(row):
    result = {}
    result['owner_id'] = str(row[0])
    result['name'] = row[1]
    result['lastname'] = row[2]
    result['email'] = row[3]
    return result

def mapLoginToDict(name, access_token):
    result = {}
    result['name'] = name
    result['access_token'] = access_token
    return result

def mapPetToDict(row):
    result = {}
    result['pet_id'] = str(row[0])
    result['pet_name'] = row[1]
    result['pet_type'] = row[2]
    result['pet_photo'] = row[3]
    result['creator'] = row[4]
    return result

def mapActionToDict(row):
    result = {}
    result['action_id'] = str(row[0])
    result['action_name'] = row[1]
    return result

def mapLogToDict(row):
    result = {}
    result['log_id'] = str(row[0])
    result['pet_name'] = row[1]
    result['action_name'] = row[2]
    result['date'] = row[3]
    return result
#calendar_id, event_name, date, owner_id, pet_id
def mapCalendarToDict(row):
    result = {}
    result['calendar_id'] = str(row[0])
    result['event_name'] = row[1]
    result['date'] = row[2]
    result['action_name'] = row[3]
    result['owner_id'] = str(row[4])
    result['pet_id'] = str(row[5])
    return result

def mapOwnerInfoToDict(row):
    result = {}
    result['Name'] = row[0] + " " + row[1]
    result['Email'] = row[2]
    return result