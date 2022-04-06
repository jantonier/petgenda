import os

class dbconfig:
    database=os.environ.get("DBNAME")
    host=os.environ.get("URL")
    port=os.environ.get("PORTDB")
    user=os.environ.get("DBUSER")
    password=os.environ.get("DBPASSWORD")
  

class dbconfig2:
    database=os.environ.get("DBNAME2")
    host=os.environ.get("URL2")
    port=os.environ.get("PORTDB2")
    user=os.environ.get("DBUSER2")
    password=os.environ.get("DBPASSWORD2")


class emailconfig:
    api_key =os.environ.get("EMAILAPIKEY")
    api_secret=os.environ.get("EMAILAPISECRET")
    sender_email=os.environ.get("EMAILSENDEREMAIL")
    sender_name=os.environ.get("EMAILSENDERNAME")
