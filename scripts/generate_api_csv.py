import os
import glob
import xml.etree.ElementTree as ET
import json
import csv
import sys

def main():
    # El script está en skills/axa/scripts/, el repo en skills/axa/repo/
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.join(base_dir, "..", "repo")

    # El CSV se guardará en la carpeta desde la que se ejecute el comando
    output_dir = os.getcwd()
    output_file = os.path.join(output_dir, "apis_config.csv")

    data = []

    if not os.path.exists(repo_path):
        print(f"Error: No se encuentra el repositorio en {repo_path}")
        sys.exit(1)

    # Buscar carpetas de apiproxies
    api_folders = [f.path for f in os.scandir(repo_path) if f.is_dir() and f.name.startswith("apiproxy")]

    for api_folder in api_folders:
        api_name = os.path.basename(api_folder).replace("apiproxy", "").replace("-apiresource-apigeex", "")
        base_path = "N/A"

        # Extraer BasePath
        proxies_path = os.path.join(api_folder, "apiproxy", "proxies", "default.xml")
        if not os.path.exists(proxies_path):
            proxy_files = glob.glob(os.path.join(api_folder, "apiproxy", "proxies", "*.xml"))
            if proxy_files: proxies_path = proxy_files[0]

        if os.path.exists(proxies_path):
            try:
                tree = ET.parse(proxies_path)
                bp_elem = tree.getroot().find(".//BasePath")
                if bp_elem is not None and bp_elem.text:
                    base_path = bp_elem.text
            except Exception: pass

        # Extraer Timeout y Backend
        targets_dir = os.path.join(api_folder, "apiproxy", "targets")
        target_files = glob.glob(os.path.join(targets_dir, "*.xml"))
        timeout = "N/A"
        backend = "N/A"
        target_file_used = None

        if target_files:
            target_file_used = target_files[0]
            for tf in target_files:
                if "default.xml" in tf.lower() or "public.xml" in tf.lower():
                    target_file_used = tf
                    break

            try:
                tree = ET.parse(target_file_used)
                root = tree.getroot()

                url_elem = root.find(".//URL")
                if url_elem is not None and url_elem.text:
                    backend = url_elem.text
                else:
                    server_elem = root.find(".//Server")
                    if server_elem is not None:
                        backend = server_elem.attrib.get('name', 'N/A')

                for prop in root.findall(".//Property"):
                    if prop.attrib.get("name") == "io.timeout.millis":
                        timeout = prop.text
                        break
            except Exception: pass

        # Resolver variables de CONFIG.JSON
        if timeout and ("CONFIG.JSON" in timeout.upper() or "@" in timeout):
            config_path = os.path.join(api_folder, "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        config_data = json.load(f)
                    prod_env = None
                    for env in config_data.get("configurations", []):
                        if env.get("name") in ["apis-prod", "prod"]:
                            prod_env = env
                            break
                    if not prod_env and config_data.get("configurations"):
                        prod_env = config_data["configurations"][0]

                    if prod_env:
                        tf_name = os.path.basename(target_file_used) if target_file_used else "default.xml"
                        for t in prod_env.get("targets", []):
                            if t.get("name") == tf_name:
                                for token in t.get("tokens", []):
                                    if "io.timeout.millis" in token.get("xpath", ""):
                                        timeout = token.get("value")
                                        break
                except Exception: pass

        data.append({"API Name": api_name, "Timeout (TO)": timeout, "Base Path": base_path, "Backend": backend})

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["API Name", "Timeout (TO)", "Base Path", "Backend"], delimiter=";")
        writer.writeheader()
        writer.writerows(data)

    print(f"Documento CSV generado correctamente en: {output_file}")

if __name__ == "__main__":
    main()