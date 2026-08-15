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


# Allowed extensions for blog
ALLOWED_EXTENSIONS = {
    ".md",
    ".markdown",
    ".canvas",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".svg",
    ".pdf",
}


def sanitize_markdown(file_path: str):
    """
    Fixes markdown files where horizontal rules (---) at the top of the file
    trick Quartz's YAML frontmatter parser into treating markdown body as YAML.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # If file starts with whitespace followed by ---
        stripped_leading = content.lstrip("\r\n \t")
        if stripped_leading.startswith("---"):
            lines = stripped_leading.splitlines()
            # Find closing ---
            closing_idx = -1
            for idx in range(1, min(len(lines), 100)):
                if lines[idx].strip() == "---":
                    closing_idx = idx
                    break

            if closing_idx > 0:
                header_block = "\n".join(lines[1:closing_idx])
                # If header block contains markdown elements (##, ###, list items) or fails YAML parsing
                is_markdown_pseudo_frontmatter = any(
                    line.strip().startswith(("#", "!", "[", "*", "<")) for line in lines[1:closing_idx]
                )
                if is_markdown_pseudo_frontmatter:
                    # Replace top --- with blank line so it's parsed as normal markdown, not frontmatter
                    lines[0] = ""
                    new_content = "\n".join(lines)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
    except Exception as e:
        print(f"[WARN] Failed to sanitize {file_path}: {e}")


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
                # Skip native Google Docs/Sheets/Slides
                print(f"[SKIP] Google Apps Doc: {name}")
            else:
                _, ext = os.path.splitext(name)
                if ext.lower() not in ALLOWED_EXTENSIONS:
                    print(f"[SKIP] Unallowed Extension: {name}")
                    continue

                print(f"[FILE] Downloading: {local_path}")
                request = service.files().get_media(fileId=item_id)
                with io.FileIO(local_path, "wb") as fh:
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()

                if ext.lower() in {".md", ".markdown"}:
                    sanitize_markdown(local_path)

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
