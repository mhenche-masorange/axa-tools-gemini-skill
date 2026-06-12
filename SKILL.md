---
name: axa-tools
description: Tools for Apigee X Agent (AxA) for managing and querying Apigee X proxies. Use this skill to find configuration details (base paths, timeouts, policies) from the openapi-monorepo and to fetch traffic metrics from the osp-openapi-prod GCP project.
---

# AxA (Apigee X Agent)

## Overview
AxA is a specialized agent for Apigee X. It uses a local synchronization of the `openapi-monorepo` to provide instant access to proxy configurations and integrates with GCP to fetch real-time or historical analytics.

### Known GCP Projects & Apigee Organizations
The following organizations are managed under the `osp-openapi*` footprint:
*   **`osp-openapi-int`** (Project Number: `294953947316`) - Integración / Integration (Int)
*   **`osp-openapi-aseg`** (Project Number: `1091106836606`) - Aseguramiento / QA & Testing (Aseg)
*   **`osp-openapi-ent1`** (Project Number: `719950874577`) - Entrenamiento / Training & Sandbox 1 (Ent1)
*   **`osp-openapi-ent2`** (Project Number: `482363356162`) - Entrenamiento / Training & Sandbox 2 (Ent2)
*   **`osp-openapi-prod`** (Project Number: `208787813038`) - Producción / Production (Prod)

## Core Workflows

### 1. Repository Synchronization
Before searching for proxy configurations, ensure the local repository is synced.
- **Tool**: `run_shell_command`
- **Command**: `python axa/scripts/sync_repo.py`
- **Repo Location**: `axa/repo`

### 2. Querying Configuration (Static Info)
To answer questions about Base Path, Timeouts, or Policies:
- **Tool**: `run_shell_command`
- **Command**: `python axa/scripts/get_config.py --api "API_NAME" --env "apis-prod"`
- **Description**: This script automatically finds the proxy directory, parses the XML, and resolves tokenized values from `config.json`.
- **Reference**: See `axa/references/apigee_mapping.md` for manual mapping if needed.

### 3. Querying Analytics (Dynamic Info)
To answer questions about request counts or performance:
- **Tool**: `run_shell_command`
- **Command**: `python axa/scripts/get_analytics.py --api "API_NAME" --env "prod"`
- **Project**: Defaults to `osp-openapi-prod`.
 
 ### 4. Generating Global CSV Reports
   2 To extract configuration details for all APIs (Name, Base Path, Timeout, and Backend) and generate a summary document:
   3 - **Tool**: `run_shell_command`
   4 - **Command**: `python3 scripts/generate_api_csv.py`
   5 - **Description**: This parses all local proxies in the `repo/` directory, extracts their configurations, resolves the real timeouts from `config.json`, and outputs a semicolon-separated `apis_config.csv`
     in the current working directory.

### 5. Querying Apigee Instance & Organization Info (Infrastructure)
To fetch runtime configuration, regions, state, IP ranges, or organization-level properties (including maintenance update policy and scheduled maintenance windows):
- **Tool**: `run_shell_command`
- **Commands**:
  - `python3 scripts/get_apigee_instances.py --org "ORGANIZATION_NAME"`
  - `python3 scripts/get_apigee_org.py --org "ORGANIZATION_NAME" --env "ENVIRONMENT_NAME"`
- **Description**: These scripts fetch real-time instance details (such as maintenanceUpdatePolicy start times and scheduled platform upgrades) and organization/environment details directly from the Apigee management API using active gcloud authentication. They automatically bypass any system-configured corporate proxies to avoid connection timeouts.
- **Defaults**: If `--org` is omitted, they default to `osp-openapi-prod`. If `--env` is omitted, it defaults to `apis-prod`.

## Key Files to Watch
- **Base Paths**: `/ProxyEndpoint/HTTPProxyConnection/BasePath`
- **Timeouts**: `/TargetEndpoint/HTTPTargetConnection/Properties/Property` (e.g., `io.timeout.millis`)
- **Quotas**: Found in `apiproxy/policies/` files.

## Examples
- "What is the timeout for ocsg_micTerminalRepair?" -> Sync repo, find `axa/repo/ocsg_micTerminalRepair/apiproxy/targets/default.xml`, read property.
- "How many requests did ocsg_micTerminalRepair get yesterday?" -> Run `get_analytics.ps1`.
- "Genera un CSV con todas las APIs, sus timeouts, backends y base paths" -> Run `python C:\Users\miguelangel.henche\.gemini\skills\axa\scripts\generate_api_csv.py`.