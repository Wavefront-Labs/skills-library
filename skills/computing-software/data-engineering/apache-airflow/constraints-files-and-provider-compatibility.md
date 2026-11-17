---
id: computing-software.data-engineering.apache-airflow.constraints-files-and-provider-compatibility
name: constraints-files-and-provider-compatibility
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, constraints-file, airflow-providers, dependency-resolution, pip, provider-versions, reproducible-builds]
level: practitioner
status: docs-checked
description: "Install Airflow and providers reproducibly with the official constraints files, upgrade providers independently, and resolve conflicts with your own dependencies."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html
  - https://airflow.apache.org/docs/apache-airflow-providers/installing-from-pypi.html
  - https://github.com/apache/airflow/tree/constraints-main
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constraints files and provider compatibility

**Goal:** an Airflow environment whose hundreds of transitive dependencies are the combination the Airflow project tested, upgradeable without surprise breakage.

## Why constraints
The Airflow project keeps a constraints file per released version and per supported Python version, so you can reproduce the exact Airflow + providers + dependencies set that was known to work at release. Constraints live on orphan branches (`constraints-main`, `constraints-2-0`, ...) with a tag per release, e.g. `constraints-3.3.2`.

## Install Airflow with constraints
```bash
AIRFLOW_VERSION=3.3.2
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINTS="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow[postgres,celery]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINTS}"
```
Variant: `constraints-no-providers-<py>.txt` for Airflow core without providers.

## Upgrading a provider independently
To upgrade or downgrade providers and other dependencies away from the constraints, install them as a separate command after the reproducible install, without `--constraint`:
```bash
pip install "apache-airflow==${AIRFLOW_VERSION}" apache-airflow-providers-google==10.1.1
```
Pin `apache-airflow` in the same command so pip does not change it. Then freeze the result into your own constraints file (`pip freeze > my-constraints.txt`) and install later with `--constraint my-constraints.txt`. Poetry and pip-tools installs are not supported; `uv pip` follows the pip workflow.

## Resolving conflicts with your libraries
1. Try the constraints; if pip errors on your library, see which package conflicts.
2. If your library needs a different version of something Airflow uses (pandas, protobuf, SQLAlchemy), do not force it into the Airflow env. Run that code isolated (a separate virtualenv, container or service).
3. Your own constraints file can replace the community one; you own the risk, so run full DAG tests.

## Gotchas
- Use the constraints tag for your exact released Airflow version, not a different version's file.
- Python minor version must match the constraints file name (there is one file per supported Python version).

## Verify
- [ ] Image build uses a pinned constraints URL or a committed constraints file; two builds produce identical `pip freeze`.

## Checked

2026-10-31. Confirmed against the Airflow stable "Installation from PyPI" page: constraints branches and per-release tags, one file per Python version, the `--constraint` install command, `constraints-no-providers-<py>.txt`, installing providers in a separate unconstrained command with airflow pinned, `pip freeze` into your own constraints file, Poetry/pip-tools unsupported and `uv pip` pip-like. Removed: `constraints-source-providers`, managed-service (MWAA, Composer, Astronomer) claims, virtualenv decorator names, `airflow providers list` and `pip check` checks, `main` constraints gotcha.

Method: documentation only; no commands were run.
