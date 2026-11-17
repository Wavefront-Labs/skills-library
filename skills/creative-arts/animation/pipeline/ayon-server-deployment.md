---
id: creative-arts.animation.pipeline.ayon-server-deployment
name: ayon-server-deployment
category: creative-arts
field: animation
product: pipeline
tags: [ayon-server, ayon, openpype, docker-compose, ynput, postgres, redis, addons, bundles, studio-pipeline]
level: advanced
status: draft
description: "Deploy an Ayon server for a small studio with Docker Compose: services, first admin setup, addon bundles, backups, and upgrading without breaking productions."
sources:
  - https://github.com/ynput/ayon-docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ayon server deployment

**Goal:** a running Ayon server (Ynput's successor to OpenPype) that artists' launchers connect to, with a
pinned set of addons per production and a restore path.

## Install (Docker Compose, from ynput/ayon-docker)

```bash
git clone https://github.com/ynput/ayon-docker.git && cd ayon-docker
docker compose up -d          # services: postgres, redis, ayon server (and optional workers)
```
Open `http://<SERVER>:5000`, create the first admin user. Put it behind a reverse proxy with TLS for
anything beyond a closed LAN.

## Concepts to set up next

- **Addons**: features (Maya, Blender, Nuke, Houdini integrations, ftrack/ShotGrid/Kitsu sync, deadline)
  are addons uploaded to the server (Market or zip upload).
- **Bundles**: a named, versioned set of addon versions plus the launcher/dependency package. Mark one bundle
  as **production**, another as **staging** for testing upgrades. Productions keep working while staging
  is tested.
- **Project anatomy and settings** per project (`creative-arts.animation.pipeline.ayon-project-anatomy`).
- **Launcher** distribution to workstations (`creative-arts.animation.pipeline.ayon-launcher-environments`).

## Storage and paths

Ayon stores metadata in Postgres; files live on your storage. Configure root paths (Windows, Linux, macOS)
per project so every OS resolves the same files.

## Backups

- Postgres dump on a schedule (`docker compose exec postgres pg_dump -U ayon ayon > ayon_$(date +%F).sql`)
  plus the server's addon/storage volumes.
- Test a restore on a separate machine before relying on it.

## Upgrades

1. Read release notes; upgrade the server container (`docker compose pull && docker compose up -d`).
2. Create a new staging bundle with updated addons; test with a pilot user on a copy project.
3. Promote to production bundle; launchers update on next start.

## Gotchas

- Mixed addon versions between server bundle and what artists' launchers cache cause "addon not
  compatible" errors; always change versions through bundles.
- Exposed port 5000 without TLS sends credentials in clear text.

## Verify

A workstation launcher logs in, shows the production bundle, launches a DCC with the Ayon menu, and a
test publish appears in the web UI.
