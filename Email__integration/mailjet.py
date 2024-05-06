#This is the script we used to create and send an email object to the user's email address. This still needs to create an attachment and pull an image from 
#the directory for this to be applicable. This will only be used in the final application to notify the user.

from mailjet_rest import Client
import os

#Get api keys from file which creates environmental vars
execfile("keys.py")

#Grab key values from env vars
api_key = os.environ['MJ_APIKEY_PUBLIC']
api_secret = os.environ['MJ_APIKEY_PRIVATE']

#Create email object
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

#Send email, print debug stuff
result = mailjet.send.create(data=data)
print(result.status_code)
print(result.json())
