---
id: computing-software.systems-network-administration.jellyfin.migrate-linux-install-to-docker
name: migrate-linux-install-to-docker
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, migration, docker, bind-mount, uid-gid, docker-compose]
level: advanced
status: docs-checked
description: "Move a native Linux Jellyfin install into the official Docker image by reusing its directories, matching media paths and the jellyfin user's uid and gid."
sources: ["https://jellyfin.org/docs/general/administration/migrate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating a Linux install to Docker

The data of a local install can be used by the official image if you map the same files and folders into the container. Two rules from the docs:

- Media paths inside the container must match exactly. If media lives at `/media/raid/`, it must be reachable at `/media/raid/` in the container.
- Permissions must line up, so run the container as the local Jellyfin user. Find the ids with `id jellyfin` and substitute them for `<uid>:<gid>`.

Use `Dashboard > Paths` to see which folders to map.

```sh
docker run -d \
    --user <uid>:<gid> \
    -e JELLYFIN_CACHE_DIR=/var/cache/jellyfin \
    -e JELLYFIN_CONFIG_DIR=/etc/jellyfin \
    -e JELLYFIN_DATA_DIR=/var/lib/jellyfin \
    -e JELLYFIN_LOG_DIR=/var/log/jellyfin \
    --mount type=bind,source=/etc/jellyfin,target=/etc/jellyfin \
    --mount type=bind,source=/var/cache/jellyfin,target=/var/cache/jellyfin \
    --mount type=bind,source=/var/lib/jellyfin,target=/var/lib/jellyfin \
    --mount type=bind,source=/var/log/jellyfin,target=/var/log/jellyfin \
    --mount type=bind,source=</path/to/media>,target=</path/to/media> \
    --net=host --restart=unless-stopped \
    jellyfin/jellyfin
```

The compose equivalent sets `user`, `network_mode: 'host'`, the same four `JELLYFIN_*_DIR` variables and the same volumes.

## Checked

2026-11-03. Confirmed against the Jellyfin Migrating page: exact matching media paths, id jellyfin for uid and gid, Dashboard > Paths, docker run and compose settings. Removed: unsupported stop-the-service and backup advice.

Method: documentation only; no commands were run.
