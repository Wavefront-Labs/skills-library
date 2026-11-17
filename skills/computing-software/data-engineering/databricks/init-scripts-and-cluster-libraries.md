---
id: computing-software.data-engineering.databricks.init-scripts-and-cluster-libraries
name: init-scripts-and-cluster-libraries
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, init-scripts, cluster-libraries, compute-configuration, unity-catalog-volumes]
level: advanced
status: docs-checked
description: "Install system packages and libraries on Databricks classic compute: init scripts in volumes or workspace files, allowlists, library sources, logs, and serverless alternatives."
sources:
  - https://docs.databricks.com/aws/en/init-scripts/
  - https://docs.databricks.com/aws/en/libraries/
  - https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/allowlist
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Init scripts and cluster libraries

**Goal:** reproducible compute setup without manual installs, compatible with Unity Catalog access modes.

## Libraries first
Prefer libraries over init scripts:
- Cluster, notebook-scoped and job-task libraries are covered on the Databricks libraries page.
- Serverless compute does not support init scripts; use the serverless environment configuration instead.

## Init scripts (when you need OS packages, certs, agents)
```bash
#!/bin/bash
set -euo pipefail
apt-get update -y && apt-get install -y libpq-dev
cp /Volumes/main/infra/certs/corp-ca.pem /usr/local/share/ca-certificates/corp-ca.crt && update-ca-certificates
```
Add the script path in the compute configuration's init script settings.
- Store in **UC volumes** (Databricks Runtime 13.3 LTS and above with Unity Catalog), **workspace files**, or cloud object storage. Init scripts on DBFS have reached end-of-life and can no longer be used.
- Standard (shared) access mode requires the script path / Maven coordinates / JAR paths to be on the metastore **allowlist**.
- Only workspace admins can create global init scripts, which can cause library conflicts: prefer compute policies or cluster-scoped init scripts. Restart affected clusters after changing any init script.

## Logs
Enable compute log delivery to keep init script output; see the Databricks compute log delivery documentation.

## Gotchas
- Init scripts run on every node at every start: slow scripts slow every job. Keep scripts light.
- `pip install` in init scripts can break runtime-provided packages; pin versions compatible with the DBR.
- Serverless does not support init scripts.

## Verify
The compute starts without init script errors; `%sh dpkg -l libpq-dev` in a notebook confirms the package.

## Checked

- 2026-10-28: confirmed on the init scripts page (classic compute only, serverless unsupported, volumes on Runtime 13.3 LTS and above, workspace files, DBFS end-of-life, standard access mode allowlist, admin-only global init scripts, restart after changes).
- Removed: pinned PyPI and `%pip` examples, the `init_scripts` JSON snippet, `cluster_log_conf` details, event log names and the container services advice (not in the fetched pages).

Method: documentation only; no commands were run.
