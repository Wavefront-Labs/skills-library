---
id: computing-software.systems-network-administration.rclone.rclone-docker-volume-plugin
name: rclone-docker-volume-plugin
category: computing-software
field: systems-network-administration
product: rclone
tags: [docker, volume-plugin, managed-plugin, compose, swarm, fuse]
level: advanced
status: docs-checked
description: "Run rclone as a Docker managed volume plugin and create volumes with remote, type and mount options."
sources: ["https://rclone.org/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rclone can serve Docker named volumes backed by any remote. It must run on the same host as the Docker daemon (or on every Swarm node) and needs the FUSE driver on the host (for example the `fuse3` package).

## Install the managed plugin

```console
mkdir -p /var/lib/docker-plugins/rclone/config
mkdir -p /var/lib/docker-plugins/rclone/cache
docker plugin install rclone/docker-volume-rclone:amd64 args="-v" --alias rclone --grant-all-permissions
docker plugin list
```

The config directory must exist even if you use no config file, because options can be passed statically.

## Create volumes

```console
docker volume create vol1 -d rclone -o remote=storj: -o vfs-cache-mode=full
docker volume create vol2 -d rclone -o remote=:storj,access_grant=xxx:heimdall
docker volume create vol3 -d rclone -o type=storj -o path=heimdall -o storj-access-grant=xxx -o poll-interval=0
```

`-d rclone` selects the driver (the `--alias rclone` makes that work for the full plugin name). Options are set with `-o` and cover backend parameters plus mount and VFS options; special ones are `remote`, `fs`, `type`, `path`, `mount-type` and `persist`. Connection strings work in `remote`. Inspect with `docker volume list` and `docker volume inspect`.

## Caveat when changing settings

Docker has no volume update command. Re-running `docker volume create` with new options on an existing volume silently does nothing. Remove the volume first (`docker volume remove my_vol`), stopping any container or Swarm service using it, then recreate it and confirm with `docker volume inspect`. The same page covers Compose and Swarm usage, systemd operation of a standalone plugin, healthchecks and troubleshooting.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
