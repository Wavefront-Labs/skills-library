---
id: computing-software.data-engineering.apache-airflow.customising-the-docker-image
name: customising-the-docker-image
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow-docker-image, dockerfile, constraints-file, providers, extend-image, airflow-deployment, pip-install]
level: practitioner
status: docs-checked
description: "Extend the official apache/airflow Docker image with providers, Python packages and OS deps using constraints, and bake DAGs or shared code for reproducible deploys."
sources:
  - https://airflow.apache.org/docs/docker-stack/build.html
  - https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customising the Airflow Docker image

**Goal:** one immutable image per release containing Airflow, providers and libraries, used by every component.

## Extend (the normal path)
```dockerfile
FROM apache/airflow:<AIRFLOW_VERSION>

USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends libpq-dev git \
 && apt-get clean && rm -rf /var/lib/apt/lists/*
USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

COPY --chown=airflow:root include/ /opt/airflow/include/
# optional: bake DAGs (vs git-sync / bundles)
COPY --chown=airflow:root dags/ /opt/airflow/dags/
```
Rules:
- Install with `apache-airflow==${AIRFLOW_VERSION}` on the same pip command so pip cannot upgrade/downgrade Airflow while resolving your packages. `AIRFLOW_VERSION` is set in the base image.
- Run `pip` as the `airflow` user. Root only for apt.
- Pin provider versions in requirements.txt (for example `apache-airflow-providers-snowflake==<VERSION>`).

## Constraints
For reproducible resolution, use Airflow's constraints file for your exact version and Python:
```bash
pip install "apache-airflow-providers-amazon" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-<AIRFLOW_VERSION>/constraints-<PYTHON_VERSION>.txt"
```
Constraints pin transitive deps that were tested together. If your library needs a conflicting version, isolate that task (virtualenv/KPO) rather than overriding constraints.

## Customise (build from source)
Use only when you need a different base OS/Python or to minimise size: build from the Airflow repo's Dockerfile with build args (for example `ADDITIONAL_AIRFLOW_EXTRAS`, `ADDITIONAL_PYTHON_DEPS`). Most teams should extend.

## Verify in the build
```dockerfile
RUN python -c "import airflow, sys; print(airflow.__version__)" \
 && airflow providers list | grep -E "snowflake|amazon" \
 && python -m pip check
```
Add a DagBag import test in CI against the built image.

## Gotchas
- Different images for scheduler and workers (e.g. worker has extra libs) -> DAGs parse on one but not the other. Use one image.
- `latest` tags: pin the full version and Python tag.
- Image size: providers like Google/Amazon pull many deps; install only what you use.
- Baked DAGs require a rebuild per DAG change; fine for strict change control, slow for iteration (consider bundles/git-sync).

## Verify
- [ ] `pip check` clean, `airflow version` matches expectation in every running pod.
- [ ] Image digest pinned in Helm values; rollback = previous digest.

## Checked

2026-10-28. Confirmed in the Airflow Docker stack build page and installation page: extending the image with `FROM apache/airflow:<version>`, apt installs as root then back to the airflow user, the constraints URL pattern `constraints-<airflow version>/constraints-<python version>.txt`, and the `ADDITIONAL_PYTHON_DEPS` / `ADDITIONAL_AIRFLOW_EXTRAS` build args. Fixed: the build arg was named `AIRFLOW_EXTRAS`. Removed: a concrete image tag, constraint version and provider pin, and the venv claim.
Method: documentation only; no commands were run.
