from mailjet_rest import Client
import os

os.environ['MJ_APIKEY_PUBLIC'] = '7f4057a65d47712d6b513b7a15c17789'
os.environ['MJ_APIKEY_PRIVATE'] = '63548e7a89bff43c762146098dd12b87'
api_key = os.environ['MJ_APIKEY_PUBLIC']
api_secret = os.environ['MJ_APIKEY_PRIVATE']

mailjet = Client(auth=(api_key, api_secret), version='v3.1')

data = {
  'Messages': [
    {
      "From": {
        "Email": "aelevine@bu.edu",
        "Name": "Me"
      },
      "To": [
        {
          "Email": "alexlevine3120@gmail.com",
          "Name": "You"
        }
      ],
      "Subject": "My first Mailjet Email!",
      "TextPart": "Greetings from Mailjet!",
      "HTMLPart": "<h3>Dear passenger 1, welcome to <a href=\"https://www.mailjet.com/\">Mailjet</a>!</h3><br />May the delivery force be with you!"
    }
  ]
}
result = mailjet.send.create(data=data)
print(result.status_code)
print(result.json())