from Google import Create_Service
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import mimetypes


def send_message(to: str, subject: str, emailMsg: str, file_path: list):
    CLIENT_SECRETE_FILE = 'client_secret.json',
    API_NAME = 'gmail',
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRETE_FILE, API_NAME,API_VERSION,SCOPES)

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

send_message("mcowley@bu.edu","Print Failed","See attached images",'annotated_image.jpg')