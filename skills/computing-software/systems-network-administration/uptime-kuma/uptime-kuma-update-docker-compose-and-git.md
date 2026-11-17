---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-update-docker-compose-and-git
name: uptime-kuma-update-docker-compose-and-git
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [uptime-kuma-update, docker-pull, force-recreate, git-checkout, download-dist, pm2-restart]
level: practitioner
status: docs-checked
description: "Update Uptime Kuma safely for docker run, Compose and Git installs, with data volume preserved."
sources: ["https://github.com/louislam/uptime-kuma/wiki/%F0%9F%86%99-How-to-Update"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Updating Uptime Kuma

The data directory is the state; updating means replacing the code or image and keeping the volume.

Docker (run):
```bash
docker pull louislam/uptime-kuma:2
docker stop uptime-kuma
docker rm uptime-kuma
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:2
```
Use your own port and volume if you changed them. New releases take time to build the image, so a missing tag shortly after a release is normal.

Docker Compose:
```bash
cd /path/to/compose-dir
docker compose pull
docker compose up -d --force-recreate
```

Non-Docker:
```bash
cd /path/to/uptime-kuma
git fetch --all --tags
git checkout 2.5.9 --force      # the release tag you want
npm install --omit dev --no-audit
npm run download-dist
pm2 restart uptime-kuma
```

Crossing major versions is different: v1 to v2 migrates the database and must not be interrupted (see uptime-kuma-v1-to-v2-migration).

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: How to Update page (Docker, Compose and non-Docker commands, image build delay) and Migration From v1 To v2 page. Removed: The instruction to back up before every update (the page only says this for the v1 to v2 migration) and the generic verify line.

Method: documentation only; no commands were run.
