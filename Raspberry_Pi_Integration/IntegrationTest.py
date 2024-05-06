#This code is an extension of rasPiTest.py
#It unsuccessfully calls the GMail API to send an email to notify the user of failed prints.

import os.path
import cv2
import subprocess
from inference_sdk import InferenceHTTPClient
import base64
import mimetypes
import os
from email.message import EmailMessage
from google.oauth2.credentials import Credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="wUU8rX5LcogWMC67u43g"
)

# Main loop; infers sequentially until you press "q"
while True:
    # On "q" keypress, exit
    def signal_handler(sig, frame):
        print("Ctrl+C detected. Exiting...")
        exit(0)

    # Get the current image from the webcam
    subprocess.run(["fswebcam", "-r", "1280x720", "--jpeg", "100", "--save", "/home/me500/fdmVision/image.jpg"])
    img = cv2.imread("/home/me500/fdmVision/image.jpg")

    # Perform inference using the Roboflow Infer API
    result = CLIENT.infer(img, model_id="fdm-failures-spaghetti/1")

    # Parse the inference results
    predictions = result['predictions']

    for prediction in predictions:
        # Extract prediction information
        print(prediction)
        class_name = prediction['class']
        x, y = int(prediction['x']), int(prediction['y'])
        print(x,y)
        width, height = int(prediction['width']), int(prediction['height'])
        print(width,height)
        confidence = int(prediction['confidence'])
        print(confidence)

        # Draw bounding box on the image
        topLeft = (int(x-width/2),int(y+height/2))
        print(topLeft)
        bottomRight = (int(x+width/2),int(y-height/2))
        print(bottomRight)
        cv2.rectangle(img, topLeft, bottomRight, (0, 255, 0), 2)
        cv2.putText(img, class_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        annotatedImagePath = "/home/me500/fdmVision/annotated_image.jpg"
        cv2.imwrite(annotatedImagePath,img)

        def gmail_send_message_with_attachment():

            SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

            """Create and insert a draft email with attachment.
            Print the returned draft's message and id.
            Returns: Draft object, including draft id and message meta data.

            Load pre-authorized user credentials from the environment.
            TODO(developer) - See https://developers.google.com/identity
            for guides on implementing OAuth2 for the application.
            """

            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

            try:
                # create gmail api client
                service = build("gmail", "v1", credentials=creds)
                mime_message = EmailMessage()

                # headers
                mime_message["To"] = "mcowley@bu.edu"
                mime_message["From"] = "spaghettimonitor@gmail.com"
                mime_message["Subject"] = "sample with attachment"

                # text
                mime_message.set_content(
                    "Hi, this is automated mail with attachment.Please do not reply."
                )

                # attachment
                attachment_filename = annotatedImagePath
                # guessing the MIME type
                type_subtype, _ = mimetypes.guess_type(attachment_filename)
                maintype, subtype = type_subtype.split("/")

                with open(attachment_filename, "rb") as fp:
                    attachment_data = fp.read()
                mime_message.add_attachment(attachment_data, maintype, subtype)

                encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

                create_message = {"raw": encoded_message}
                # pylint: disable=E1101
                send_message = (
                    service.users()
                    .messages()
                    .send(userId="me", body=create_message)
                    .execute()
                )
                print(f'Message Id: {send_message["id"]}')
            except HttpError as error:
                print(f"An error occurred: {error}")
                send_message = None
            return send_message

        if __name__ == "__main__":
            gmail_send_message_with_attachment

        exit(0)
