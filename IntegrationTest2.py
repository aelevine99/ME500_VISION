import os.path
import cv2
import subprocess
from inference_sdk import InferenceHTTPClient
import base64
import mimetypes
import os

from Google import Create_service
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

# Define global constant for SCOPES
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="wUU8rX5LcogWMC67u43g"
)

def send_message(to: str, subject: str, emailMsg: str, file_path: list):
    CLIENT_SECRETE_FILE = 'client_secret.json',
    API_NAME = 'gmail',
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_service(CLIENT_SECRETE_FILE, API_NAME,API_VERSION,SCOPES)

    file_attachments = [file_path]

    emailMsg = 'Print failed. See attached image.'

    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = to
    mimeMessage['subject'] = subject
    mimeMessage.attach(MIMEText(emailMsg,'plain'))

    #Attach files
    for attachment in file_attachments:
        content_type, encoding = mimetypes.guess_type(attachment)
        main_type, sub_type = content_type.split('/',1)
        file_name = os.path.basename(attachment)

        f = open(attachment,'rb')
        myFile = MIMEBase(main_type,sub_type)
        myFile.set_payload(f.read())
        myFile.add_header("Content Disposition","attachment",filename = file_name)

        f.close()

        mimeMessage.attach(myFile)

    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(
        userID='me',
        body={'raw': raw_string}).execute()
    print(message)
    return message 

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

        

    exit(0)
