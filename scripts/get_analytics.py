import subprocess
import argparse
import json
from datetime import datetime, timedelta

def get_stats(api_name, environment, project):
    print(f"Fetching stats for {api_name} in {environment}...")
    
    # Calculate yesterday and today
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).strftime("%m/%d/%Y 00:00")
    today = now.strftime("%m/%d/%Y 00:00")
    
    command = [
        "gcloud", "apigee", "stats", "list",
        f"--project={project}",
        f"--environment={environment}",
        f"--api={api_name}",
        "--select=sum(message_count)",
        f"--start={yesterday}",
        f"--end={today}",
        "--format=json"
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Error fetching stats: {result.stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Apigee stats.")
    parser.add_argument("--api", required=True, help="API proxy name")
    parser.add_argument("--env", default="prod", help="Environment (default: prod)")
    parser.add_argument("--project", default="osp-openapi-prod", help="GCP Project")
    
    args = parser.parse_args()
    get_stats(args.api, args.env, args.project)
