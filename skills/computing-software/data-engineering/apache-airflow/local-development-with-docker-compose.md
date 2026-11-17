---
id: computing-software.data-engineering.apache-airflow.local-development-with-docker-compose
name: local-development-with-docker-compose
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow-docker-compose, local-development, docker-compose]
level: intro
status: docs-checked
description: "Run Airflow locally with the official docker-compose.yaml: init, user id, adding requirements, CLI access, resetting state, and what not to carry into production."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local Airflow with docker compose

**Goal:** a full local stack (scheduler, API server, triggerer, worker and supporting services) in minutes.

## Start
```bash
mkdir airflow-local && cd airflow-local
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/<version>/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env          # Linux; on other OSes ignore the warning or set AIRFLOW_UID=50000
docker compose up airflow-init                  # initialization service
docker compose up -d
```
The API server is at http://localhost:8080; the default login and password are `airflow`. Configure Docker with at least 4 GB of memory.

## Add Python packages
- Quick test: `_PIP_ADDITIONAL_REQUIREMENTS="<package>==<version>"` in `.env` (containers install the requirements at start; testing only, never production).
- Proper: build an image:
```dockerfile
FROM apache/airflow:<version>
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```
and in compose set `build: .` instead of `image:`.

## Everyday commands
```bash
docker compose run airflow-cli airflow config list
docker compose logs -f airflow-scheduler
docker compose down --volumes --remove-orphans     # wipe DB and start fresh
```

## Gotchas
- The compose file is a quick-start for learning and exploration. It gives none of the security guarantees a production system needs; the docs recommend Kubernetes with the Official Airflow Community Helm Chart for production.
- The best way to recover from most problems is to clean up and restart from scratch (`down --volumes`).

## Verify
`docker compose ps` shows the services as healthy.

## Checked

2026-10-31. Confirmed against the Airflow stable Docker Compose how-to: directory setup, `AIRFLOW_UID` handling, `airflow-init`, port 8080 and default login, 4 GB memory guidance, `_PIP_ADDITIONAL_REQUIREMENTS` is not for production, `airflow-cli` service, `down --volumes --remove-orphans`, production warning and Helm chart recommendation. Removed: DAG processor/Postgres/Redis list, refresh-interval and logs permission gotchas, `dags test` example, tag-pinning note.

Method: documentation only; no commands were run.
