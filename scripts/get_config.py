import os
import json
import xml.etree.ElementTree as ET
import argparse
from glob import glob

def find_proxy_dir(repo_path, api_name):
    """Fuzzy search for the proxy directory."""
    patterns = [
        f"apiproxy{api_name.lower()}*",
        f"*{api_name.lower()}*"
    ]
    for pattern in patterns:
        matches = glob(os.path.join(repo_path, pattern))
        if matches:
            # Filter for directories
            dirs = [m for m in matches if os.path.isdir(m)]
            if dirs:
                return dirs[0]
    return None

def get_xml_value(file_path, xpath):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        # Simple XPath-like search (limited support in ET)
        # Note: This is a simplified parser for the common Apigee structure
        parts = xpath.strip("/").split("/")
        current = root
        
        # ET search is relative to root, but root IS the first tag
        if current.tag != parts[0]:
            return None
            
        for part in parts[1:]:
            # Handle potential property attributes [ @name='...']
            if "[" in part:
                tag = part.split("[")[0]
                attr_name = part.split("@")[1].split("=")[0]
                attr_value = part.split("'")[1]
                found = False
                for child in current.findall(tag):
                    if child.get(attr_name) == attr_value:
                        current = child
                        found = True
                        break
                if not found: return None
            else:
                current = current.find(part)
                if current is None: return None
        return current.text
    except Exception as e:
        return f"Error: {str(e)}"

def resolve_config_json(proxy_dir, env_name, target_xml, xpath):
    config_path = os.path.join(proxy_dir, "config.json")
    if not os.path.exists(config_path):
        return None
        
    try:
        with open(config_path, "r") as f:
            data = json.load(f)
            
        for config in data.get("configurations", []):
            if config.get("name") == env_name:
                for target in config.get("targets", []):
                    if target.get("name") == target_xml:
                        for token in target.get("tokens", []):
                            # Normalize XPaths for comparison (simple check)
                            if token.get("xpath").replace("//", "/") == xpath.replace("//", "/"):
                                return token.get("value")
    except Exception:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description="Extract Apigee Proxy config.")
    parser.add_argument("--api", required=True, help="API name")
    parser.add_argument("--env", default="apis-prod", help="Environment name in config.json")
    parser.add_argument("--repo", default="axa/repo", help="Path to repo")
    
    args = parser.parse_args()
    
    proxy_dir = find_proxy_dir(args.repo, args.api)
    if not proxy_dir:
        print(f"Error: Could not find directory for API '{args.api}'")
        return

    print(f"Proxy Directory: {os.path.basename(proxy_dir)}")
    
    # 1. Base Path
    proxy_xmls = glob(os.path.join(proxy_dir, "apiproxy", "proxies", "*.xml"))
    if proxy_xmls:
        base_path = get_xml_value(proxy_xmls[0], "ProxyEndpoint/HTTPProxyConnection/BasePath")
        print(f"Base Path: {base_path}")

    # 2. Timeouts
    target_xmls = glob(os.path.join(proxy_dir, "apiproxy", "targets", "*.xml"))
    for t_xml in target_xmls:
        t_name = os.path.basename(t_xml)
        xpath = "TargetEndpoint/HTTPTargetConnection/Properties/Property[@name='io.timeout.millis']"
        val = get_xml_value(t_xml, xpath)
        
        if val == "CONFIG.JSON":
            val = resolve_config_json(proxy_dir, args.env, t_name, "/TargetEndpoint/HTTPTargetConnection/Properties/Property[@name='io.timeout.millis']")
        
        print(f"Target: {t_name} | Timeout: {val} ms")

if __name__ == "__main__":
    main()
