import subprocess
import json
import urllib.request
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Fetch Apigee X instances for an organization")
    parser.add_argument("--org", default="osp-openapi-prod", help="Apigee organization/project name (default: osp-openapi-prod)")
    args = parser.parse_args()

    # Bypass corporate proxy if set in system
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    os.environ['no_proxy'] = '*'
    os.environ['NO_PROXY'] = '*'

    # Get token
    token_res = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, shell=True)
    token = token_res.stdout.strip()
    if not token:
        print("Error: Could not retrieve token from gcloud.")
        return

    url = f"https://apigee.googleapis.com/v1/organizations/{args.org}/instances"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error fetching instances for {args.org}: {e}")

if __name__ == "__main__":
    main()
