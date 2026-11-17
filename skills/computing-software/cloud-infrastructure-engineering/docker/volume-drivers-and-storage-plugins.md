---
id: computing-software.cloud-infrastructure-engineering.docker.volume-drivers-and-storage-plugins
name: volume-drivers-and-storage-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volume-driver, local-driver, nfs-volume, docker-plugin, rexray, local-persist, volume-plugin-api, bind-mount, tmpfs, overlay2, storage-driver, volume-prune, plugin-install, docker-plugin-create]
level: advanced
status: docs-checked
description: "Docker storage past the default local volume driver: NFS/cloud-backed volume drivers, the plugin API, when a bind mount beats a named volume, and volume lifecycle pitfalls."
sources: ["https://docs.docker.com/engine/storage/volumes/", "https://docs.docker.com/reference/cli/docker/plugin/install/", "https://docs.docker.com/reference/cli/docker/volume/prune/", "https://docs.docker.com/reference/cli/docker/compose/down/", "https://docs.docker.com/engine/storage/drivers/select-storage-driver/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume drivers and storage plugins

**Goal:** pick the right persistence mechanism (bind mount, named volume, driver-backed
volume) for the actual failure mode you're protecting against, and know how to plug in
network/cloud storage when a single host's disk isn't enough.

## The three built-in mechanisms, and when each is right
- **Bind mount** (`-v /host/path:/container/path`) — direct host path, no Docker-managed
  lifecycle; it obscures any files already at the container path. Right for: config files you edit on the host, dev-loop source code, anything
  where the host path is the source of truth. Wrong for: anything that needs to survive a
  host rebuild or move with the container to another host — it's tied to that exact path on
  that exact host.
- **Named volume** (`-v myvol:/data`, stored under `/var/lib/docker/volumes/` on Linux) —
  Docker owns the lifecycle (`docker volume create/rm/prune`), shareable across containers on
  the same host, and it persists after the container is removed (`docker compose down -v`
  deletes the named volumes declared in the Compose file, so run it only when you mean to
  delete data). Right default for databases and any stateful service's data directory.
- **tmpfs mount** (`--tmpfs /tmp` or `--mount type=tmpfs,dst=/tmp`) — held in host memory,
  removed when the container stops, not shareable between containers. Right for scratch space
  you do not want persisted.

## Volume drivers (the plugin API)
The `local` driver is single-host only. For multi-host (a service that can be rescheduled
to any node and needs the same data) you need a driver that backs onto shared/network
storage:
```
docker plugin install vieux/sshfs
docker volume create -d vieux/sshfs -o sshcmd=user@host:/path -o password=<PW> sshvolume
```
NFS and CIFS need no third-party plugin: the `local` driver accepts `type`, `o` and `device`
options (for example `-o type=nfs -o o=addr=<nfs-host>,rw -o device=:/export/path`, see
`local-volume-driver-nfs-cifs-and-plugins`). Other drivers come from plugins; check each
plugin's own documentation and maintenance status before depending on it.

## Volume lifecycle pitfalls
- `docker compose down` **without** `-v` keeps named volumes; **with** `-v` deletes them.
  Confirm which one a script runs before trusting "it'll just restart with data intact" —
  this has destroyed dev databases more than once.
- `docker volume prune` removes unused local volumes, meaning volumes not referenced by any
  container. By default it removes only **anonymous** volumes; `--all` (`-a`) also removes
  unused named volumes. Anonymous volumes (for example from a Dockerfile `VOLUME` with no
  mount specified) are the ones that accumulate and get pruned.
- Compose does not remove anonymous volumes by default on `docker compose down`, and they have
  no stable name, so they are easy to leak.
- When a volume backed by a plugin disappears from `docker volume ls`, check that the plugin
  is still enabled (`docker plugin ls`): with the plugin disabled its volumes are not listed.

## Storage driver vs volume driver — don't confuse them
The **storage driver** (`overlay2` is the default on supported distributions) governs how image *layers* are stored and
unioned; it has nothing to do with volume persistence. `docker info` shows which one is
active. Changing the storage driver makes existing containers and images inaccessible on the
host, so back up or save what you need first.

## Verify
`docker volume inspect <name>` shows the `Driver` field matching what you intended (not
silently `local` when you meant a network driver); for a multi-host driver, stop the
container on node A, start an equivalent container on node B, and confirm the data is
actually there, not just that the volume name resolved.

## Checked

Date: 2026-10-24. Documentation release: Docker Engine storage docs, `docker volume prune`, `docker compose down` and `docker plugin install` references (docker/docs, docker/cli, docker/compose main).
Confirmed: bind mounts obscuring existing files, tmpfs semantics, named volumes under `/var/lib/docker/volumes`,
`docker compose down -v` removing declared named volumes, the sshfs plugin install and volume create form, and that
changing the storage driver makes existing images and containers inaccessible. Corrected: `docker volume prune` removes
only anonymous volumes by default (`--all` for named ones), `-v` cannot create tmpfs mounts, and changing the storage
driver does not require wiping the data directory. Removed: third-party plugin names (local-persist, rexray, cloud
drivers) and the unconfirmed older-version plugin error behaviour.

Method: documentation only; no commands were run.
