import subprocess
import json
import urllib.request
import os
import argparse

def fetch_url(url, token):
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Fetch Apigee X organization and environment details")
    parser.add_argument("--org", default="osp-openapi-prod", help="Apigee organization/project name (default: osp-openapi-prod)")
    parser.add_argument("--env", default="apis-prod", help="Apigee environment name (default: apis-prod)")
    args = parser.parse_args()

    # Bypass corporate proxy if set in system
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    os.environ['no_proxy'] = '*'
    os.environ['NO_PROXY'] = '*'

    # Get token
    token_res = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True)
    token = token_res.stdout.strip()
    if not token:
        print("Error: Could not retrieve token.")
        return

    print(f"=== Organization Details ({args.org}) ===")
    org_data = fetch_url(f"https://apigee.googleapis.com/v1/organizations/{args.org}", token)
    print(json.dumps(org_data, indent=2))

    print(f"\n=== Environment Details ({args.env}) ===")
    env_data = fetch_url(f"https://apigee.googleapis.com/v1/organizations/{args.org}/environments/{args.env}", token)
    print(json.dumps(env_data, indent=2))

if __name__ == "__main__":
    main()
