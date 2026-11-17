---
id: computing-software.cybersecurity-defensive.authelia.docker-compose-deployment-and-secrets
name: docker-compose-deployment-and-secrets
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, docker, docker-compose, puid, pgid, umask, docker-secrets, container]
level: practitioner
status: docs-checked
description: "Deploy Authelia in Docker Compose with Docker secrets or a secrets volume, and set PUID, PGID and UMASK to control container permissions."
sources:
  - https://www.authelia.com/integration/deployment/docker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The official image is `docker.io/authelia/authelia`. The standalone example expects a `data/authelia/config/configuration.yml`, a `data/authelia/secrets/` directory holding `JWT_SECRET`, `SESSION_SECRET`, `STORAGE_PASSWORD` and `STORAGE_ENCRYPTION_KEY`, PostgreSQL as storage and an external bridge network.

```yaml
services:
  authelia:
    image: 'docker.io/authelia/authelia:latest'
    restart: 'unless-stopped'
    secrets: ['JWT_SECRET', 'SESSION_SECRET', 'STORAGE_PASSWORD', 'STORAGE_ENCRYPTION_KEY']
    environment:
      AUTHELIA_IDENTITY_VALIDATION_RESET_PASSWORD_JWT_SECRET_FILE: '/run/secrets/JWT_SECRET'
      AUTHELIA_SESSION_SECRET_FILE: '/run/secrets/SESSION_SECRET'
      AUTHELIA_STORAGE_POSTGRES_PASSWORD_FILE: '/run/secrets/STORAGE_PASSWORD'
      AUTHELIA_STORAGE_ENCRYPTION_KEY_FILE: '/run/secrets/STORAGE_ENCRYPTION_KEY'
    volumes:
      - '${PWD}/data/authelia/config:/config'
```

An alternative mounts the secrets directory as a volume and points the `_FILE` variables at `/secrets/...`.

Permission models, in the documented order of preference:

1. Tell Docker to run the container as another user (`user:` in Compose). The process never has privileged access, but you must set filesystem permissions yourself.
2. Set `PUID`, `PGID` (default 0) so the entrypoint, which then runs as root, chowns paths and drops privileges. `UMASK`, if set, runs `umask ${UMASK}`.
3. User namespaces, beyond the documentation and support.

These variables only affect the container entrypoint, not the daemon.

Images are published as `authelia/authelia`, `docker.io/authelia/authelia` and `ghcr.io/authelia/authelia`. The examples use `latest`; pinning a version tag instead is general practice, not from the page.

If logs do not explain a startup failure, the page's debug recipe overlays a `compose.debug.yml` that disables the healthcheck, sets `AUTHELIA_LOG_LEVEL: 'trace'` and runs `sleep 3300`, then `docker exec -it authelia sh` and run `authelia` interactively. To reach Authelia from a proxy on the host, publish `127.0.0.1:9091:9091`.

Check: `docker compose logs authelia` shows the listening line and no missing-secret errors.

## Checked

2026-11-08. Read in full: integration/deployment/docker. Added image registries and the debug recipe; version pinning labelled as practice.

Method: documentation only; no commands were run.
