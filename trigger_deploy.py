"""
One-click blog sync trigger script.
Triggers GitHub Actions to fetch Google Drive notes and rebuild the Quartz blog.
"""

import os
import sys
import urllib.request
import json

REPO_OWNER = "jshoon1106"
REPO_NAME = "my-obsidian-blog"
EVENT_TYPE = "sync-blog"


def trigger_sync():
    # You can set GITHUB_PAT as an environment variable or enter it
    token = os.environ.get("GITHUB_PAT")
    if not token:
        token = input("Enter your GitHub Personal Access Token (PAT): ").strip()
        if not token:
            print("[ERROR] GitHub PAT is required to trigger deployment.")
            sys.exit(1)

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "Quartz-Sync-Trigger"
    }
    payload = json.dumps({"event_type": EVENT_TYPE}).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in (200, 204):
                print(">> [SUCCESS] GitHub Actions deployment triggered successfully!")
                print(f">> Check progress at: https://github.com/{REPO_OWNER}/{REPO_NAME}/actions")
                print(">> The site will be updated in ~1 minute: https://jshoon1106.github.io/my-obsidian-blog/")
            else:
                print(f"[STATUS] Received response status: {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP Error {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] Failed to trigger deployment: {e}")


if __name__ == "__main__":
    trigger_sync()
