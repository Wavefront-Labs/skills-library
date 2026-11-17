---
id: computing-software.cybersecurity-defensive.authentik.install-docker-compose
name: install-docker-compose
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, docker-compose, install, secret-key, postgres, ports]
level: practitioner
status: docs-checked
description: "Install authentik with Docker Compose: fetch compose.yml, generate PG_PASS and AUTHENTIK_SECRET_KEY, set ports, mind the Docker socket and UTC, then run initial setup."
sources:
  - https://docs.goauthentik.io/install-config/install/docker-compose/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: a test or small production authentik on Docker Compose. Needs a host with at least 2 CPU cores, 2 GB RAM, and Podman or Docker Compose v2.

1. Download the file: `wget https://docs.goauthentik.io/compose.yml` (Linux) or `curl -O https://docs.goauthentik.io/compose.yml` (macOS).
2. Generate secrets into `.env`:
```shell
echo "PG_PASS=$(openssl rand -base64 36 | tr -d '\n')" >> .env
echo "AUTHENTIK_SECRET_KEY=$(openssl rand -base64 60 | tr -d '\n')" >> .env
```
PostgreSQL does not support passwords longer than 99 characters. Optional error reporting: `echo "AUTHENTIK_ERROR_REPORTING__ENABLED=true" >> .env`.
3. Optional custom exposed ports in `.env`: `COMPOSE_PORT_HTTP=80` and `COMPOSE_PORT_HTTPS=443` (authentik listens on 9000 HTTP and 9443 HTTPS by default; internal ports are changed via the configuration reference). Re-run `docker compose up -d` after changing.
4. Start: `docker compose pull` then `docker compose up -d`.
5. Open `http://<server IP or hostname>:9000` and set a password for the default `akadmin` user.

## Gotchas
- All internal operations use UTC. Do not update or mount `/etc/timezone` or `/etc/localtime` in the containers; it breaks OAuth and SAML authentication.
- The compose file mounts `/var/run/docker.sock` into the worker for automatic outpost deployment. That is a security risk; use a Docker Socket Proxy, or remove the mount and deploy outposts manually.
- `compose.yml` pins the version current at download time. To upgrade, download a new `compose.yml` (see the upgrade skill).
- Configure global email afterwards for admin alerts and Email stages.

## Checked

Method: docs-checked 2026-11-09 against https://docs.goauthentik.io/install-config/install/docker-compose/ (read in full).
