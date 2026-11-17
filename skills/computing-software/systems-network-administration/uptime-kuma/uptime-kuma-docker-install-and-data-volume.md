---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-docker-install-and-data-volume
name: uptime-kuma-docker-install-and-data-volume
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [uptime-kuma-install, docker-run, data-volume, sqlite-file-locking, docker-compose, port-3001]
level: intro
status: docs-checked
description: "Run Uptime Kuma 2 in Docker with a persistent data volume, change the port, and avoid SQLite corruption on NFS."
sources: ["https://github.com/louislam/uptime-kuma/wiki/%F0%9F%94%A7-How-to-Install"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing Uptime Kuma with Docker

```bash
docker run -d --restart=unless-stopped -p 3001:3001 \
  -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:2
```

Browse to `http://localhost:3001`. To change the port or storage use `-p <YOUR_PORT>:3001 -v <YOUR_DIR OR VOLUME>:/app/data`. For Compose the project publishes an example `compose.yaml`; start with `docker compose up -d`.

Persistent data is stored under `/app/data`. The install page warns that SQLite needs POSIX file locking: do not put the data directory on a filesystem with unreliable locks, such as commonly encountered NFS setups, or the database can corrupt. Map a local volume or directory instead.

Tag choice matters: `louislam/uptime-kuma:2` follows the latest v2; the `latest` tag is deprecated and still points to v1 (see uptime-kuma-docker-tags-slim-and-rootless). Reverse proxying needs WebSocket headers (see uptime-kuma-reverse-proxy-websocket-headers).

Non-Docker alternative needs Node.js 20.4 or newer, Git and pm2 (see uptime-kuma-non-docker-install-pm2-systemd).

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: How to Install page (docker run command, port and volume options, POSIX file lock warning, Compose example link, non-Docker requirements) and Migration From v1 To v2 / Docker Tags pages (tag and latest deprecation). Removed: The invented minimal Compose service, the claim that /app/data is the only thing to back up, and the generic verify line.

Method: documentation only; no commands were run.
