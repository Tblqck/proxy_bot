# ------------------ GOOGLE DRIVE API INTERACT (RAM-ONLY VERSION) ------------------
import io
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

SERVICE_ACCOUNT_FILE = 'proxydatacollector-a0c74abdcd83.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = '1oAElT3urppWuayzOmV0GlYebtAvjyyDa'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)


def get_file_id(filename):
    query = f"name='{filename}' and '{FOLDER_ID}' in parents and trashed=false"
    response = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = response.get('files', [])
    return files[0]['id'] if files else None


def download_csv(filename):
    file_id = get_file_id(filename)
    if not file_id:
        print(f"⚠️ '{filename}' not found in Drive.")
        return None

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)
    df = pd.read_csv(fh)
    print(f"⬇️ Downloaded '{filename}' ({len(df)} rows)")
    return df


def upload_csv(df, filename):
    if df is None or df.empty:
        print(f"⚠️ Skipped upload for empty '{filename}'")
        return

    csv_bytes = io.BytesIO()
    df.to_csv(csv_bytes, index=False)
    csv_bytes.seek(0)
    media = MediaIoBaseUpload(csv_bytes, mimetype='text/csv')

    file_id = get_file_id(filename)
    if file_id:
        drive_service.files().update(fileId=file_id, media_body=media).execute()
        print(f"🔄 Updated '{filename}' ({len(df)} rows)")
    else:
        file_metadata = {'name': filename, 'parents': [FOLDER_ID]}
        drive_service.files().create(body=file_metadata, media_body=media).execute()
        print(f"✅ Uploaded new '{filename}' ({len(df)} rows)")
