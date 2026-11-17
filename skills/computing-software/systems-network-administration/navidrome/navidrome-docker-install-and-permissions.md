---
id: computing-software.systems-network-administration.navidrome.navidrome-docker-install-and-permissions
name: navidrome-docker-install-and-permissions
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, docker, docker-compose, permissions, uid-gid, data-folder, music-folder, puid]
level: practitioner
status: docs-checked
description: "Deploy Navidrome with Docker or Compose and fix the two permission failures: unwritable /data crashes at startup, unreadable /music gives an empty library. PUID/PGID do nothing."
sources: ["https://www.navidrome.org/docs/installation/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome in Docker: install and permissions

```yaml
services:
  navidrome:
    image: navidrome/navidrome:latest
    user: 1000:1000
    ports:
      - "4533:4533"
    restart: unless-stopped
    environment:
      ND_LOGLEVEL: info
    volumes:
      - "/path/to/data:/data"
      - "/path/to/your/music/folder:/music:ro"
```

Images exist for linux/amd64, arm/v6, arm/v7 and arm64. Navidrome needs read and write on `/data` (database and cache) and read on `/music`, both for the `UID:GID` in `user:`. Check yours with `id -u`, `id -g` and `ls -n /path/to/music`.

Failure 1, data folder not writable: the container exits at startup with `Error applying PRAGMA optimize ... unable to open database file` followed by a nil pointer panic. Fix: `mkdir -p /path/to/data && sudo chown -R $(id -u):$(id -g) /path/to/data`.

Failure 2, music folder not readable: the UI works but the library is empty, with `Error starting watcher ... open /music: permission denied` and `Scanner: Target folder does not exist.` (misleading: the folder exists, the user just cannot open it). Fix with `chown -R` to the container user, or `chmod -R a+rX` if other programs share the folder.

Do not rely on `PUID` and `PGID`: those are a linuxserver.io convention and Navidrome's image ignores them. Do not delete the `user:` line either; the container then runs as root and the error vanishes, which is unsafe in production.

Config: add `ND_` environment variables (for example `-e ND_SESSIONTIMEOUT=24h`) or put `navidrome.toml` in `/data` and set `ND_CONFIGFILE=/data/navidrome.toml`. Multi-library setups need extra volume mounts. The Jellyfin API auto-discovery feature needs host networking.

## Checked

2026-11-04. Confirmed against the Navidrome Installing with Docker page: platforms, compose example, permission needs, both failure modes with their log lines and fixes, PUID/PGID, the `user:` directive, config file setup, multi-library mounts and Jellyfin host networking. Removed the closing verify line (the scan and first-run page behaviour is not on the page).

Method: documentation only; no commands were run.
