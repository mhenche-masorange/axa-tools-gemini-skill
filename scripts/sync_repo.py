import os
import subprocess
from datetime import datetime

# Configuration
REPO_URL = "https://github.com/masorange/openapi-monorepo"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.join(SCRIPT_DIR, "..", "repo")
TIMESTAMP_FILE = os.path.join(SCRIPT_DIR, "..", ".last_sync")

def sync_repo():
    if os.path.exists(REPO_DIR):
        print("Updating repository...")
        subprocess.run(["git", "-C", REPO_DIR, "pull", "--quiet"], check=True)
    else:
        print("Cloning repository...")
        subprocess.run(["git", "clone", REPO_URL, REPO_DIR, "--quiet"], check=True)
    
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d"))

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "r") as f:
            last_sync = f.read().strip()
        
        if last_sync != today:
            sync_repo()
        else:
            print(f"Repository is up to date (last sync: {last_sync}).")
    else:
        sync_repo()

if __name__ == "__main__":
    main()
