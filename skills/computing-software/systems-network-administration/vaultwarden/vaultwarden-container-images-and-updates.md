---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-container-images-and-updates
name: vaultwarden-container-images-and-updates
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, docker, container-image, latest-alpine, testing-tag, update, watchtower, ghcr]
level: intro
status: docs-checked
description: "Pick the right Vaultwarden container image and tag (latest, alpine, testing, pinned versions, registries) and update it with docker or compose without losing data."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Which-container-image-to-use", "https://github.com/dani-garcia/vaultwarden/wiki/Updating-the-vaultwarden-image"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden images and updates

Registries: `ghcr.io/dani-garcia/vaultwarden`, `docker.io/vaultwarden/server`, `quay.io/vaultwarden/server`.

Tags: `latest` (latest release, recommended), `testing` (latest commits, early access, occasional issues), `x.y.z` (pinned release), `latest-alpine` and `x.y.z-alpine` (same as latest but Alpine instead of Debian; mostly preference). The image is multi-arch since 1.16.0; since 1.17.0 one image supports SQLite, MySQL and PostgreSQL, with SQLite the most tested. The old `bitwardenrs/server-mysql` and `-postgresql` images should be replaced. ARMv6 boards need Docker 20.10.0+, and a Pi Zero may need `--platform=linux/arm/v6`. The bundled web vault always matches the server version; keep the server current because newer Bitwarden clients can break against old servers.

Update standalone Docker with a bind-mounted data directory:

```
docker pull vaultwarden/server:latest
docker stop vaultwarden && docker rm vaultwarden
docker run -d --name vaultwarden -v /vw-data/:/data/ -p 80:80 vaultwarden/server:latest
```

Compose: `docker compose pull`, then `docker compose up -d`. If data is not bind-mounted, carry it across with `--volumes-from` and an intermediate busybox container before removing the old one. Watchtower can automate pull-and-recreate. Back up before updating (see the backup skill). Be careful with `docker system prune -f` after updates: it can remove unrelated stopped containers and unused images.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Which-container-image-to-use (tags, registries, 1.16.0/1.17.0, ARMv6, client compatibility) and Updating-the-vaultwarden-image (pull/stop/rm, volumes-from, Watchtower, prune warning).
Removed or reworded: the `&&` chaining of the compose commands (the page lists them as two commands).
Method: documentation only; no commands were run.
