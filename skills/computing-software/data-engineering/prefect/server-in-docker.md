---
id: computing-software.data-engineering.prefect.server-in-docker
name: server-in-docker
category: computing-software
field: data-engineering
product: prefect
tags: [docker, server-start, api-url, self-hosted, container]
level: intro
status: docs-checked
description: "Run a self-hosted Prefect server in Docker with the prefecthq/prefect image, port 4200, host binding and PREFECT_API_URL checks."
sources:
  - https://docs.prefect.io/v3/how-to-guides/self-hosted/server-docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: start a Prefect server container.

```bash
docker run -p 4200:4200 -d --rm prefecthq/prefect:3-latest -- prefect server start --host 0.0.0.0
```

- Image: `prefecthq/prefect:3-latest`
- `-p 4200:4200` forwards the server port to localhost
- `-d` runs detached; `--rm` removes the container when it stops
- `--host 0.0.0.0` makes the server listen on all interfaces so the port mapping works

`PREFECT_API_URL` must be set so Prefect works from inside a container; the page gives no value, so point it at the server's API address for your network.

Verify the client configuration and open the UI:

```bash
prefect config view --show-secrets
prefect dashboard open
```

The default database is SQLite; for production use PostgreSQL via `server.database.connection_url` (see the server-database skill). The page does not cover Docker Compose or database environment variables.

## Checked
2026-11-08. Confirmed against the server-in-Docker how-to: the docker run command, port forwarding, --host 0.0.0.0, PREFECT_API_URL requirement, config view and dashboard open. SQLite default and PostgreSQL for production are confirmed on the Prefect server concept page, and server.database.connection_url on the settings and profiles page. Nothing removed.
Method: documentation only; no commands were run.
