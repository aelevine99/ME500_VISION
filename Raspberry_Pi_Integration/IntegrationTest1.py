import cv2
import subprocess
from inference_sdk import InferenceHTTPClient
import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage

# Initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com", api_key="wUU8rX5LcogWMC67u43g"
)

# Main loop; infers sequentially until you press "q"
while True:
    # On "q" keypress, exit
    def signal_handler(sig, frame):
        print("Ctrl+C detected. Exiting...")
        exit(0)

    # Get the current image from the webcam
    subprocess.run(
        [
            "fswebcam",
            "-r",
            "1280x720",
            "--jpeg",
            "100",
            "--save",
            "/home/me500/fdmVision/image.jpg",
        ]
    )
    img = cv2.imread("/home/me500/fdmVision/image.jpg")

    # Perform inference using the Roboflow Infer API
    result = CLIENT.infer(img, model_id="fdm-failures-spaghetti/1")

    # Parse the inference results
    predictions = result["predictions"]

    for prediction in predictions:
        # Extract prediction information
        print(prediction)
        class_name = prediction["class"]
        x, y = int(prediction["x"]), int(prediction["y"])
        print(x, y)
        width, height = int(prediction["width"]), int(prediction["height"])
        print(width, height)
        confidence = int(prediction["confidence"])
        print(confidence)

        # Draw bounding box on the image
        topLeft = (int(x - width / 2), int(y + height / 2))
        print(topLeft)
        bottomRight = (int(x + width / 2), int(y - height / 2))
        print(bottomRight)
        cv2.rectangle(img, topLeft, bottomRight, (0, 255, 0), 2)
        cv2.putText(
            img, class_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
        )

        annotatedImagePath = "/home/me500/fdmVision/annotated_image.jpg"
        cv2.imwrite(annotatedImagePath, img)

        SCOPES = ["https://www.mail.google.com"]

        def send_message(
            messageBody: str, subject: str, to_email: str, key_path: str, attachments: list = None
        ):
            """Create and send an email message
            Print the returned  message id
            Returns: Message object, including message id"""

            creds = Credentials.from_authorized_user_file(key_path, SCOPES)
            
            try:
                service = build("gmail", "v1", credentials=creds)

                print(attachments)
                message = EmailMessage()
                message["To"] = to_email
                message["From"] = "spaghettimonitor@gmail.com"
                message["Subject"] = subject
                message.set_content(messageBody)
                print("To:", message["To"])
                print("From:", message["From"])
                print("Subject:", message["Subject"])
                print("Content-Type:", message["Content-Type"])
                # Print the message body
                print("Body:", message.get_payload(decode=True))
                if attachments:
                    for attachment in attachments:
                        print(attachment)
                        with open(attachment, "rb") as content_file:
                            content = content_file.read()
                            message.add_attachment(
                                content,
                                maintype="image",
                                subtype=(attachment.split(".")[1]),
                                filename=attachment,
                            )

                encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

                create_message = {"raw": encoded_message}
                # pylint: disable=E1101
                send_message = (
                    service.users()
                    .messages()
                    .send(userId="spaghettimonitor@gmail.com", body=create_message)
                    .execute()
                )
                print(f'Message Id: {send_message["id"]}')
            except HttpError as error:
                print("An error occurred:")
                print(f"HTTP status code: {error.resp.status}")
                print(f"Error content: {error.content.decode('utf-8')}")
                send_message = None
            return send_message

        # Example usage:
        credentials = "/home/me500/fdmVision/client_secret.json"
        sender_email = "spaghettimonitor@gmail.com"
        recipient_email = "mpbcowley@gmail.com"
        subject = "Test email with attachment"
        body = "This is a test email with attachment."
        attachment_path = "annotated_image.jpg"

        send_message(body, subject, recipient_email, credentials, [attachment_path])

        exit(0)
