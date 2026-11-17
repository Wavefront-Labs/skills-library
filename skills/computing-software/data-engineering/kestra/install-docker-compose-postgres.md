---
id: computing-software.data-engineering.kestra.install-docker-compose-postgres
name: install-docker-compose-postgres
category: computing-software
field: data-engineering
product: kestra
tags: [docker-compose, postgres, install, kestra-configuration, networking, port-8081]
level: practitioner
status: docs-checked
description: "Install Kestra with Docker Compose and PostgreSQL, set config via KESTRA_CONFIGURATION, reach host services, split components, and avoid known pitfalls."
sources:
  - https://kestra.io/docs/installation/docker-compose
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
curl -o docker-compose.yml https://raw.githubusercontent.com/kestra-io/kestra/develop/docker-compose.yml
docker compose up -d
```

Then open `http://localhost:8080`.

Configuration:

- Settings live in the `KESTRA_CONFIGURATION` environment variable of the Kestra container.
- Or mount an `application.yaml` at `/etc/config/application.yaml` and add `--config /etc/config/application.yaml` to the server command.

Networking: the default file sets none, so host `localhost` is not reachable from the container. Use `host.docker.internal` or `172.17.0.1`, a custom network with service names, or `network_mode: host` (a security risk).

Components can run as separate services with `kestra server <component>`: `executor`, `worker`, `indexer`, `scheduler`, `webserver`. They communicate through the database.

Pitfalls:

- A database initialised with PostgreSQL 16 fails on the newer default image; pin `image: postgres:16`.
- macOS M4 SIGILL: set `JAVA_OPTS` to `-XX:UseSVE=0` on the Kestra container.
- Examples run as root for development only.
- Port 8081 is unauthenticated; expose it only on trusted networks.

## Checked

2026-11-04. Confirmed against the Kestra Docker Compose page: the download command and docker compose up -d, UI at localhost:8080, KESTRA_CONFIGURATION, config file mounted at /etc/config/application.yaml with --config, networking options (host.docker.internal, 172.17.0.1, custom network, network_mode host), separate server components communicating through the database, postgres:16 pin, JAVA_OPTS -XX:UseSVE=0 for macOS M4, root user for development only, unauthenticated port 8081. Removed the advice to change placeholder credentials, which the page does not state.

Method: documentation only; no commands were run.
