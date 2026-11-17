---
id: computing-software.data-science-and-analytics.apache-superset.docker-compose-quickstart
name: docker-compose-quickstart
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [docker-compose, quickstart, env-local, compose-variants, evaluation]
level: intro
status: docs-checked
description: "Start Superset with Docker Compose: the four compose file variants, docker/.env-local overrides, default port and login, and why it is not production."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/installation/docker-compose.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run a local Superset for evaluation or development (Linux or macOS; Windows has no official support).

Clone with `git clone --depth=1 https://github.com/apache/superset.git`, then pick a compose file:
- `docker-compose.yml`: interactive development; mounts your local frontend and backend folders. Run `docker compose up --build`.
- `docker-compose-light.yml`: minimal services (database, app, frontend dev server), in-memory caching instead of Redis, built to run several instances (default port 9001; `NODE_PORT=9002 docker compose -p superset-2 -f docker-compose-light.yml up`).
- `docker-compose-non-dev.yml`: builds a more immutable image from the local branch.
- `docker-compose-image-tag.yml`: pulls a pre-built image from Docker Hub. Use a `-dev` suffixed `TAG` (for example `5.0.0-dev`, default `latest-dev`) so the image has the `psycopg2-binary` driver for the bundled Postgres.

Example for an official release:

```bash
export TAG=5.0.0
git fetch --depth=1 origin tag $TAG
git checkout $TAG
docker compose -f docker-compose-image-tag.yml up
```

Check out the matching release tag so the compose files and mounted `docker/` scripts agree with the image.

Settings: `docker/.env` holds defaults for all images; override in `docker/.env-local`, which is in `.gitignore`. `SUPERSET_LOAD_EXAMPLES` controls loading example data (set `SUPERSET_FORCE_LOAD_EXAMPLES=yes` to reload). Extra Python config goes in `docker/pythonpath_dev/superset_config_docker.py`, ignored by git.

Access: browse to http://localhost:8088 (use http, not https) and log in as `admin` / `admin`.

Telemetry: Superset uses Scarf Gateway. Set `SCARF_ANALYTICS` to `false` in `docker/.env` to disable the telemetry pixel; to stop pulling through the gateway, change the `x-superset-image:` line to `apache/superset`.

Warning: the docs say Docker Compose is not production-ready (the metadata database lives in an un-backed-up Docker volume) and they neither support nor recommend it for production. From inside a container, `localhost` is the container: to reach a database on the host use `host.docker.internal` or the docker0 gateway address.

## Checked

2026-11-08. Confirmed against the Docker Compose page (read in full). Removed: the unsupported `git checkout 4.1.0` example and "hardened deployment" advice (page recommends minikube with the Kubernetes docs for single-host use); corrected the compose variant descriptions.
Method: documentation only; no commands were run.
