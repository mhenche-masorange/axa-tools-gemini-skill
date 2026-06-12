import subprocess
import json
import urllib.request
import urllib.parse
import os
import argparse
from datetime import datetime, timedelta

def main():
    # Setup arguments
    parser = argparse.ArgumentParser(description="Query Apigee X analytics for a specific API proxy.")
    parser.add_argument("--api", required=True, help="Name of the API proxy (e.g., NumberVerification)")
    parser.add_argument("--env", default="apis-prod", help="Apigee environment name (default: apis-prod)")
    parser.add_argument("--project", default="osp-openapi-prod", help="GCP project / Apigee organization name (default: osp-openapi-prod)")
    parser.add_argument("--timerange", help="Optional time range in format 'MM/DD/YYYY HH:MM~MM/DD/YYYY HH:MM' (default: last 24 hours)")
    args = parser.parse_args()

    # Bypass corporate proxy if set
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''
    os.environ['http_proxy'] = ''
    os.environ['https_proxy'] = ''
    os.environ['no_proxy'] = '*'
    os.environ['NO_PROXY'] = '*'

    # Determine time range
    if args.timerange:
        time_range = args.timerange
    else:
        now = datetime.now()
        start = now - timedelta(hours=24)
        time_range = f"{start.strftime('%m/%d/%Y %H:%M')}~{now.strftime('%m/%d/%Y %H:%M')}"

    # Get token
    token_res = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, shell=True)
    token = token_res.stdout.strip()
    if not token:
        print("Error: Could not retrieve token.")
        return

    # Endpoint URL
    base_url = f"https://apigee.googleapis.com/v1/organizations/{args.project}/environments/{args.env}/stats/apiproxy"
    params = {
        "select": "sum(message_count),avg(total_response_time),avg(target_response_time)",
        "timeRange": time_range,
        "filter": f"(apiproxy eq '{args.api}')"
    }
    url = base_url + "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error calling Apigee Analytics API for {args.api} in {args.env}: {e}")

if __name__ == "__main__":
    main()
