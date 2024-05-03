import cv2
import subprocess
from inference_sdk import InferenceHTTPClient
import base64
import mimetypes
import os
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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

        def gmail_create_draft_with_attachment():
            """Create and insert a draft email with attachment.
            Print the returned draft's message and id.
            Returns: Draft object, including draft id and message meta data.

            Load pre-authorized user credentials from the environment.
            TODO(developer) - See https://developers.google.com/identity
            for guides on implementing OAuth2 for the application.
            """
            creds, _ = google.auth.default()

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

                create_draft_request_body = {"message": {"raw": encoded_message}}
                # pylint: disable=E1101
                draft = (
                    service.users()
                    .drafts()
                    .create(userId="me", body=create_draft_request_body)
                    .execute()
                )
                print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
            except HttpError as error:
                print(f"An error occurred: {error}")
                draft = None
            return draft


        def build_file_part(file):
            """Creates a MIME part for a file. Args: file: The path to the file to be attached. Returns:
                A MIME part that can be attached to a message."""
            content_type, encoding = mimetypes.guess_type(file)

            if content_type is None or encoding is not None:
                content_type = "application/octet-stream"
            main_type, sub_type = content_type.split("/", 1)
            if main_type == "text":
                with open(file, "rb"):
                    msg = MIMEText("r", _subtype=sub_type)
            elif main_type == "image":
                with open(file, "rb"):
                    msg = MIMEImage("r", _subtype=sub_type)
            elif main_type == "audio":
                with open(file, "rb"):
                    msg = MIMEAudio("r", _subtype=sub_type)
            else:
                with open(file, "rb"):
                    msg = MIMEBase(main_type, sub_type)
                msg.set_payload(file.read())
            filename = os.path.basename(file)
            msg.add_header("Content-Disposition", "attachment", filename=filename)
            return msg


        if __name__ == "__main__":
            gmail_create_draft_with_attachment()

        exit(0)