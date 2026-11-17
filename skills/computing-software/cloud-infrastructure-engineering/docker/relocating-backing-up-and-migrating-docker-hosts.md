---
id: computing-software.cloud-infrastructure-engineering.docker.relocating-backing-up-and-migrating-docker-hosts
name: relocating-backing-up-and-migrating-docker-hosts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, data-root, data-root-move, relocate-docker-root, docker-backup, var-lib-docker-backup, docker-state-backup, host-migration]
level: advanced
description: "Move /var/lib/docker to a new disk with data-root, decide what Docker state is worth backing up, and migrate workloads to a new host by rebuilding, not copying."
sources: ["https://docs.docker.com/reference/cli/dockerd/#daemon-data-directory", "https://docs.docker.com/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes", "https://docs.docker.com/engine/daemon/", "https://docs.docker.com/engine/storage/drivers/overlayfs-driver/", "https://docs.docker.com/engine/swarm/admin_guide/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Relocating, backing up and migrating Docker hosts

## Move data-root to another disk
```sh
sudo systemctl stop docker docker.socket containerd
sudo rsync -aHAX --numeric-ids /var/lib/docker/ /srv/docker/
echo '{ "data-root": "/srv/docker" }' | sudo tee /etc/docker/daemon.json   # merge, don't overwrite existing keys
sudo systemctl start docker
docker info -f '{{.DockerRootDir}}'
docker ps -a && docker volume ls                # everything still there
sudo mv /var/lib/docker /var/lib/docker.old     # delete after a few days
```
- `data-root` is the daemon option for the root directory of persistent Docker state
  (default `/var/lib/docker`).
- Target filesystem must suit overlay2: Docker's overlay2 docs say `xfs` needs `ftype=1`
  (verify with `xfs_info`).
- Make sure the target path is mounted before Docker starts.

## What to back up
| Item | Back up? |
|---|---|
| Named volumes / bind-mounted data | **Yes** - application-consistent dumps preferred |
| `/etc/docker/` (daemon.json, certs), `~/.docker/config.json`, contexts | Yes |
| Compose files, `.env`, secrets source | Yes (in git / secret store) |
| Images | No - rebuild or re-pull from registry |
| Containers' writable layers | No - if something there matters, it should be a volume |
| Whole `/var/lib/docker` | Only with Docker stopped; restore to the same engine version and storage driver |
| Swarm | `/var/lib/docker/swarm`, backed up with Docker stopped on the manager (Swarm admin guide) |

## Migrating to a new host
1. Install the same (or newer) engine version; copy `/etc/docker/daemon.json`, certs.
2. Recreate networks and volumes declaratively (Compose).
3. Restore volume data (tar via helper container or app dump/restore).
4. `docker compose pull && docker compose up -d`; images come from the registry.
5. Cut traffic over (DNS/LB), keep the old host read-only until verified.

Images not in a registry: `docker save | ssh new docker load` for that set.

## Gotchas
- Container IDs and IPs change on migration; anything referencing them (monitoring, firewall) needs updating.

## Verify
On the new host, `docker compose ps` all healthy, app data checksums/row counts match, and
the old host's `docker ps` is empty after cutover.

## Checked
Date: 2026-10-26. Documentation: docker/docs main (last commit 2026-10-23): dockerd reference (`data-root`), overlayfs storage driver page, volumes page (back up, restore or migrate), Swarm admin guide (back up the swarm). Confirmed: `data-root` option and default, xfs `ftype=1` requirement, volume backup via helper containers, swarm directory and stop-before-backup. Removed as unconfirmed: rsync flag rationale, systemd RequiresMountsFor, containerd root relocation, the cross-version daemon-failure claim, `--info=progress2`. The `rsync` and `docker save | ssh docker load` commands are general-purpose tooling and are not documented by Docker in these pages; treat them as examples to adapt.
Method: documentation only; no commands were run.
