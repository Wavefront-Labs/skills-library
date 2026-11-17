---
id: computing-software.messaging-and-integration.ntfy.install-docker
name: install-docker
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, docker, docker-compose, kubernetes, container]
level: practitioner
status: docs-checked
description: "Run ntfy in Docker, Compose or Kubernetes: the image has no server.yml, persistence mounts, non-root ownership and the healthcheck."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/install.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ntfy in containers

Image `binwiederhier/ntfy`; the server listens on port 80; command `serve`. The image does **not** include `/etc/ntfy/server.yml`: create one and mount it.

## Docker

- Persistent cache: mount a host directory at `/var/cache/ntfy` and pass `--cache-file /var/cache/ntfy/cache.db` to `serve`.
- Config: mount `/etc/ntfy`; set `TZ`; optionally run as non-root with `-u UID:GID`.

## Compose essentials

- `image: binwiederhier/ntfy`, `command: serve`
- environment `TZ=UTC` (optional), `user: UID:GID` (optional)
- volumes for `/var/cache/ntfy` and `/etc/ntfy`
- port `80:80`, `restart: unless-stopped`
- healthcheck against `/v1/health`, which requires `init: true` to avoid zombie processes

## Gotchas

- Non-root user: `chown` `server.yml`, `user.db`, `cache.db` and the attachments directory to the same UID/GID.
- Custom image: base on `binwiederhier/ntfy`, copy `server.yml` to `/etc/ntfy/server.yml`, `ENTRYPOINT ["ntfy", "serve"]`.

## Kubernetes

Run the image with `args: ["serve"]`, mount config from a ConfigMap at `/etc/ntfy` (`kubectl create configmap ntfy --from-file=server.yml`). For persistence the page's example passes `serve --cache-file /var/cache/ntfy/cache.db` and mounts a volume at `/var/cache/ntfy`.

## Checked

2026-11-04. Confirmed against the ntfy install page (Docker, Docker Compose, Kubernetes): image name, port 80, no bundled `server.yml`, mount points, `--cache-file`, `TZ`, `-u UID:GID`, Compose healthcheck on `/v1/health` with `init: true`, `restart: unless-stopped`, chown note, custom image lines, ConfigMap command, `args: ["serve"]`. Removed: a SQLite single-writer claim, a PVC and attachment-directory claim, and the Verify step.
Method: documentation only; no commands were run.
