---
id: computing-software.cloud-infrastructure-engineering.docker.migrating-to-the-containerd-image-store
name: migrating-to-the-containerd-image-store
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, containerd-image-store, containerd-snapshotter, image-store, overlayfs-snapshotter, multi-platform-images, docker-engine-upgrade, daemon-json]
level: advanced
status: docs-checked
description: "Switch Docker Engine or Desktop from the classic graph-driver image store to the containerd image store without losing images or containers, and roll back."
sources: ["https://docs.docker.com/engine/storage/containerd/", "https://docs.docker.com/build/building/multi-platform/", "https://docs.docker.com/reference/cli/docker/image/ls/", "https://docs.docker.com/desktop/features/containerd/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating to the containerd image store

**Goal:** move a host from the classic image store (`overlay2` graph driver) to the containerd
image store (snapshotters) so it can hold multi-platform images and attestations locally,
without the "all my images vanished" surprise.

## What actually changes
- Images move from the legacy graph driver (`overlay2`) to containerd's content store and snapshotter, which uses a storage path separate from the Docker data directory. Docker does **not** convert existing
  data. After the switch, old images and containers are hidden but stay on disk; switching back
  makes them reappear.
- Volumes and networks are not mentioned as affected by the image store switch; verify with `docker volume ls` afterwards.
- Wins (per Docker's docs): multi-platform images stored locally, images with attestations (provenance, SBOM), Wasm containers, and pluggable snapshotters with lazy pulling (stargz, nydus, soci, overlaybd).
- Costs: more disk space, because containerd keeps both compressed and extracted layers; and containerd's storage path does not follow a custom Docker `data-root`, so set the containerd data directory separately to avoid filling the root partition.
- The containerd image store is not available with `userns-remap`.
- Docker Desktop has a setting "Use containerd for pulling and storing images", enabled by default. Engine 29.0 and later default to the containerd image store on fresh installs; an upgraded host keeps the legacy graph drivers until you enable it.

## Check what a host uses
```bash
docker info -f '{{ .DriverStatus }}'
# containerd image store: [[driver-type io.containerd.snapshotter.v1]]
```

## Migration procedure (Engine on Linux)
1. Inventory what must survive: `docker image ls` and `docker ps -a` for containers you cannot recreate from Compose.
2. Images that only exist locally (not in a registry): push them to a registry or `docker save -o local-images.tar <image> ...`.
   Everything else can be re-pulled.
3. Commit or document non-reproducible containers (`docker commit` + save); existing containers are hidden after the switch and must be recreated.
4. Enable the feature in `/etc/docker/daemon.json`:
   ```json
   { "features": { "containerd-snapshotter": true } }
   ```
   then `sudo systemctl restart docker`.
5. `docker load -i local-images.tar`, re-pull the rest, `docker compose up -d` per project.
6. When confident, reclaim the old store: switch back temporarily, `docker system prune -a`,
   switch forward again. Docker also has an experimental `containerd-migration` feature (and `DOCKER_MIGRATE_SNAPSHOTTER_THRESHOLD`, which switches automatically when there are no containers and the image layers total at or below the threshold); Docker recommends starting fresh instead and taking backups first.

## Docker Desktop
Toggle the "Use containerd for pulling and storing images" setting and apply. Save
local-only images first exactly as above.

## Rollback
Set `"containerd-snapshotter": false` (or untoggle), restart: the classic images and
containers return as they were. Anything built or pulled while on containerd is not
visible in the classic store, so `docker save` it before rolling back.

## Gotchas
- Multi-platform images can be built and stored locally only with the containerd image store; with the classic store a `docker-container` builder does not load its result into the local image store automatically.
- Disk usage grows during migration because both stores are populated; check free space first, including where containerd stores data.
- Lazily pulled images can run with some layer content missing from the content store, so `docker save` may be incomplete and `docker push` cannot upload the missing layers; pull again without lazy pulling (`"lazy-pull": false`) first.

## Verify
```bash
docker info -f '{{ .DriverStatus }}'    # shows io.containerd.snapshotter.v1
docker image ls --tree                  # experimental multi-platform tree view
docker volume ls                        # confirm volumes are still listed
```

## Checked

Checked against docker/docs `engine/storage/containerd.md`, `build/building/multi-platform.md` and the `docker image ls` reference (docker/docs latest commit 2026-10-23, Engine 29).

- Default on fresh installs from Engine 29.0, upgraded hosts keep the legacy drivers, `features.containerd-snapshotter` key and restart, `docker info -f '{{ .DriverStatus }}'` output, hidden-not-deleted behaviour of old images, higher disk use, separate containerd data directory, `userns-remap` exclusion, lazy pulling defaults and `lazy-pull` key, the experimental `containerd-migration` feature and `DOCKER_MIGRATE_SNAPSHOTTER_THRESHOLD`.
- Desktop setting name and default. `docker image ls --tree` is an experimental option.
- Removed as unconfirmed: the `moby` namespace and path claims, the `Driver` value comparison, third-party scanner and backup breakage, the exact build error message, the rootless store path and the claim that volumes are unaffected.

Method: documentation only; no commands were run.
