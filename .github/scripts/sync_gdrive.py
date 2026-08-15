"""
Google Drive to Quartz content/ synchronizer.
Downloads notes and attachments from a Google Drive folder using Google Drive API (Service Account).
"""

import os
import json
import io
import shutil
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Target output directory
CONTENT_DIR = "content"

# Folders and files to ignore
IGNORE_NAMES = {
    ".obsidian",
    ".agents",
    ".trash",
    "private",
    "templates",
    "desktop.ini",
    "structure_summary.json",
    ".git",
    ".DS_Store",
}


def get_drive_service():
    creds_json = os.environ.get("GDRIVE_CREDENTIALS")
    if not creds_json:
        raise ValueError("GDRIVE_CREDENTIALS environment variable is not set.")

    try:
        creds_info = json.loads(creds_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse GDRIVE_CREDENTIALS as JSON: {e}")

    creds = service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    return build("drive", "v3", credentials=creds)


def sync_folder(service, folder_id, local_dir):
    os.makedirs(local_dir, exist_ok=True)
    
    page_token = None
    while True:
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token,
            pageSize=100
        ).execute()

        items = results.get("files", [])
        for item in items:
            name = item["name"]
            item_id = item["id"]
            mime_type = item["mimeType"]

            if name in IGNORE_NAMES:
                print(f"[SKIP] Ignored: {name}")
                continue

            local_path = os.path.join(local_dir, name)

            if mime_type == "application/vnd.google-apps.folder":
                print(f"[DIR] Entering: {local_path}")
                sync_folder(service, item_id, local_path)
            elif mime_type.startswith("application/vnd.google-apps."):
                # Skip native Google Docs/Sheets/Slides unless needed
                print(f"[SKIP] Google Apps Doc: {name}")
            else:
                print(f"[FILE] Downloading: {local_path}")
                request = service.files().get_media(fileId=item_id)
                with io.FileIO(local_path, "wb") as fh:
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()

        page_token = results.get("nextPageToken")
        if not page_token:
            break


def main():
    folder_id = os.environ.get("GDRIVE_FOLDER_ID")
    if not folder_id:
        raise ValueError("GDRIVE_FOLDER_ID environment variable is not set.")

    print(f"Starting sync for Google Drive folder: {folder_id}")
    
    # Clean previous content
    if os.path.exists(CONTENT_DIR):
        print(f"Cleaning existing {CONTENT_DIR}/ directory...")
        shutil.rmtree(CONTENT_DIR)
    os.makedirs(CONTENT_DIR, exist_ok=True)

    service = get_drive_service()
    sync_folder(service, folder_id, CONTENT_DIR)
    print("Google Drive sync completed successfully.")


if __name__ == "__main__":
    main()
