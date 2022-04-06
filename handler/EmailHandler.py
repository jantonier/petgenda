from mailjet_rest import Client
from config import emailconfig

class EmailHandler():

    def sendEmail(self, subject, emailsList, html):
        api_key = emailconfig.api_key
        api_secret = emailconfig.api_secret
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": emailconfig.sender_email,
                        "Name": emailconfig.sender_name
                    },
                    "To": emailsList,
                    "Subject": subject,
                    "TextPart": "",
                    "HTMLPart": html,
                    "CustomID": "AppGettingStartedTest"
                }
            ]
        }
        result = mailjet.send.create(data=data)
        return "result"

