#This is the script we used to create and send an email object to the user's email address. This still needs to create an attachment and pull an image from 
#the directory for this to be applicable. This will only be used in the final application to notify the user.

from mailjet_rest import Client
import os
from dotenv import load_dotenv
from pathlib import Path

# Get the directory containing your script
script_dir = Path(__file__).parent.absolute()
# Look for the .env file in the same directory
env_path = script_dir / 'keys.py'

# Load the .env file with debug output
if env_path.exists():
    print(f"Loading environment variables from: {env_path}")
    load_dotenv(env_path)
else:
    print(f"Error: Cannot find {env_path}")

# Debug: Print environment variables (careful not to share these values!)
print(f"Public key found: {'Yes' if os.environ.get('MJ_APIKEY_PUBLIC') else 'No'}")
print(f"Private key found: {'Yes' if os.environ.get('MJ_APIKEY_PRIVATE') else 'No'}")

# Get API keys from environment variables
api_key = os.environ.get('MJ_APIKEY_PUBLIC')
api_secret = os.environ.get('MJ_APIKEY_PRIVATE')

# Verify keys are present
if not api_key or not api_secret:
    raise ValueError("Mailjet API keys not found in environment variables")

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
try:
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
except Exception as e:
    print(f"Error sending email: {e}")
