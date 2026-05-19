import os
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from app.core.config import settings

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_google_credentials():
    if not hasattr(settings, 'GOOGLE_SERVICE_ACCOUNT_FILE') or not settings.GOOGLE_SERVICE_ACCOUNT_FILE:
        return None
    if not os.path.exists(settings.GOOGLE_SERVICE_ACCOUNT_FILE):
        return None
    return Credentials.from_service_account_file(settings.GOOGLE_SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def log_lead_to_sheet(prospect_name: str, email: str, company_name: str, status: str):
    """
    Appends the lead's information to a Google Sheet.
    """
    creds = get_google_credentials()
    if not creds or settings.GOOGLE_SHEET_ID == "your_google_sheet_id_here":
        print("[Google Sheets] Integration skipped. Missing Credentials or Sheet ID.")
        return

    try:
        print(f"[Google Sheets] Logging lead {prospect_name} ({company_name}) as {status}...")
        service = build('sheets', 'v4', credentials=creds)
        
        values = [
            [datetime.utcnow().isoformat(), prospect_name, email, company_name, status]
        ]
        body = {'values': values}
        
        # We target Sheet1!A:E
        result = service.spreadsheets().values().append(
            spreadsheetId=settings.GOOGLE_SHEET_ID,
            range="Sheet1!A:E",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        
        print(f"[Google Sheets] Successfully logged {result.get('updates').get('updatedCells')} cells.")
        
    except Exception as e:
        print(f"[Google Sheets Error] Failed to log lead: {e}")

def upload_pdf_to_drive(pdf_path: str, company_name: str):
    """
    Uploads the generated PDF to a specific Google Drive folder.
    """
    creds = get_google_credentials()
    if not creds or settings.GOOGLE_DRIVE_FOLDER_ID == "your_google_drive_folder_id_here":
        print("[Google Drive] Integration skipped. Missing Credentials or Folder ID.")
        return

    try:
        print(f"[Google Drive] Archiving {company_name} audit to Drive...")
        service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {
            'name': f"{company_name}_Audit.pdf",
            'parents': [settings.GOOGLE_DRIVE_FOLDER_ID]
        }
        
        media = MediaFileUpload(pdf_path, mimetype='application/pdf', resumable=True)
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        print(f"[Google Drive] Successfully archived PDF with ID: {file.get('id')}")
        
    except Exception as e:
        print(f"[Google Drive Error] Failed to archive PDF: {e}")
