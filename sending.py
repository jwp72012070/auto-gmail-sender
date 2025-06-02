import os
import base64
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API 접근 권한
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message_with_attachment(to, subject, body_text, file_paths):
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject

    # 메일 본문 추가
    message.attach(MIMEText(body_text, 'plain'))

    for path in file_paths:
        path = path.strip()    
        # 첨부파일 추가
        if path and os.path.exists(path):
            with open(path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(path)
                attachment = MIMEApplication(file_data)
                attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
                message.attach(attachment)
        else:
            print(f"[경고] 첨부파일이 존재하지 않음: {path}")

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(service, user_id, message):
    return service.users().messages().send(userId=user_id, body=message).execute()

def main():
    service = gmail_authenticate()
    with open('recipients.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            email = row['email']
            file_paths_raw = row.get('files','')  # None일 수 있음
            file_paths = file_paths_raw.split(';') if file_paths_raw else []

            subject = f"{name}님, 초대의 말씀드립니다"
            body = f"""{name}님 안녕하세요,\n\n귀하를 초대하고자 이 메일을 드립니다.\n많은 관심 부탁드립니다.\n\n감사합니다."""

            message = create_message_with_attachment(email, subject, body, file_paths)
            send_email(service, 'me', message)
            print(f"📧 Sent to {name} <{email}> (첨부: {file_paths if file_paths else '없음'})")

if __name__ == '__main__':
    main()