"""
Google Drive to Quartz content/ Incremental Synchronizer.
Downloads notes and attachments from a Google Drive folder using Google Drive API (Service Account).
Supports Incremental Sync (only downloads new/modified files) and markdown auto-sanitization.
"""

import os
import json
import io
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Target output directory and manifest file
CONTENT_DIR = "content"
MANIFEST_FILE = ".sync_manifest.json"

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

# Stats
stats = {"downloaded": 0, "skipped": 0, "deleted": 0}
visited_local_paths = set()


def sanitize_markdown(file_path: str):
    """
    Auto-corrects Obsidian-specific / loose markdown syntax to prevent Quartz build errors:
    1. Fixes isolated '---' at top of file that tricks YAML parser into treating body as frontmatter.
    2. Fixes callout headers with markdown heading tags: '> [!note]+ ### Title' -> '> [!note]+ Title'
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        modified = False

        # 1. Fix leading whitespace followed by isolated ---
        stripped_leading = content.lstrip("\r\n \t")
        if stripped_leading.startswith("---"):
            lines = stripped_leading.splitlines()
            closing_idx = -1
            for idx in range(1, min(len(lines), 100)):
                if lines[idx].strip() == "---":
                    closing_idx = idx
                    break

            if closing_idx > 0:
                is_markdown_pseudo_frontmatter = any(
                    line.strip().startswith(("#", "!", "[", "*", "<", ">", "-"))
                    for line in lines[1:closing_idx]
                )
                if is_markdown_pseudo_frontmatter:
                    lines[0] = ""
                    content = "\n".join(lines)
                    modified = True

        # 2. Fix callout heading syntax: '> [!type]+ ### Title' -> '> [!type]+ Title'
        callout_regex = re.compile(r'^(>\s*\[![a-zA-Z0-9_-]+\][+-]?\s*)#{1,6}\s*(.*)$', re.MULTILINE)
        if callout_regex.search(content):
            content = callout_regex.sub(r'\1\2', content)
            modified = True

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[SANITIZE] Auto-corrected markdown syntax in {file_path}")
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


def load_manifest():
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_manifest(manifest):
    try:
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[WARN] Failed to save manifest: {e}")


def sync_folder(service, folder_id, local_dir, manifest):
    os.makedirs(local_dir, exist_ok=True)
    
    page_token = None
    while True:
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, md5Checksum)",
            pageToken=page_token,
            pageSize=100
        ).execute()

        items = results.get("files", [])
        for item in items:
            name = item["name"]
            item_id = item["id"]
            mime_type = item["mimeType"]
            modified_time = item.get("modifiedTime", "")
            md5_checksum = item.get("md5Checksum", "")

            if name in IGNORE_NAMES:
                continue

            local_path = os.path.join(local_dir, name)
            rel_path = os.path.relpath(local_path, CONTENT_DIR).replace("\\", "/")

            if mime_type == "application/vnd.google-apps.folder":
                sync_folder(service, item_id, local_path, manifest)
            elif mime_type.startswith("application/vnd.google-apps."):
                continue
            else:
                _, ext = os.path.splitext(name)
                if ext.lower() not in ALLOWED_EXTENSIONS:
                    continue

                visited_local_paths.add(os.path.abspath(local_path))

                # Check if file is already up to date
                prev_info = manifest.get(rel_path)
                file_exists = os.path.exists(local_path)

                if (
                    file_exists
                    and prev_info
                    and prev_info.get("id") == item_id
                    and prev_info.get("modifiedTime") == modified_time
                ):
                    stats["skipped"] += 1
                    continue

                # Download file
                print(f"[SYNC] Downloading: {rel_path}")
                request = service.files().get_media(fileId=item_id)
                with io.FileIO(local_path, "wb") as fh:
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()

                if ext.lower() in {".md", ".markdown"}:
                    sanitize_markdown(local_path)

                manifest[rel_path] = {
                    "id": item_id,
                    "modifiedTime": modified_time,
                    "md5": md5_checksum
                }
                stats["downloaded"] += 1

        page_token = results.get("nextPageToken")
        if not page_token:
            break


def clean_deleted_files(manifest):
    """Removes local files that no longer exist in Google Drive."""
    content_abs = os.path.abspath(CONTENT_DIR)
    for root, _, files in os.walk(content_abs):
        for file in files:
            full_path = os.path.abspath(os.path.join(root, file))
            if full_path not in visited_local_paths:
                rel_path = os.path.relpath(full_path, CONTENT_DIR).replace("\\", "/")
                try:
                    os.remove(full_path)
                    manifest.pop(rel_path, None)
                    print(f"[DELETE] Removed local file (deleted on Drive): {rel_path}")
                    stats["deleted"] += 1
                except Exception as e:
                    print(f"[WARN] Failed to delete {rel_path}: {e}")


def main():
    folder_id = os.environ.get("GDRIVE_FOLDER_ID")
    if not folder_id:
        raise ValueError("GDRIVE_FOLDER_ID environment variable is not set.")

    print(f"Starting Incremental Sync for Google Drive folder: {folder_id}")
    os.makedirs(CONTENT_DIR, exist_ok=True)

    manifest = load_manifest()
    service = get_drive_service()
    sync_folder(service, folder_id, CONTENT_DIR, manifest)
    clean_deleted_files(manifest)

    # Convert Obsidian Dataview blocks into static GFM markdown tables/lists
    try:
        from dataview_converter import convert_dataview_queries_in_vault
        print("\n>> Evaluating Dataview queries...")
        convert_dataview_queries_in_vault(CONTENT_DIR)
    except Exception as e:
        print(f"[WARN] Dataview conversion warning: {e}")

    save_manifest(manifest)

    print(
        f"\n>> [INCREMENTAL SYNC COMPLETED] "
        f"Downloaded: {stats['downloaded']}, "
        f"Skipped (Up-to-date): {stats['skipped']}, "
        f"Deleted: {stats['deleted']}"
    )


if __name__ == "__main__":
    main()
