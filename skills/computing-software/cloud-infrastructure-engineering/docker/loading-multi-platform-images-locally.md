---
id: computing-software.cloud-infrastructure-engineering.docker.loading-multi-platform-images-locally
name: loading-multi-platform-images-locally
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, multi-platform, load-multi-platform, containerd-image-store, buildx-load, image-tree, run-platform]
level: practitioner
status: docs-checked
description: "Load a multi-arch build into the local image store (needs the containerd store), list platforms with image ls --tree, run a specific variant, and work around the classic store."
sources: ["https://docs.docker.com/engine/storage/containerd/", "https://docs.docker.com/build/building/multi-platform/", "https://docs.docker.com/reference/cli/docker/image/ls/", "https://docs.docker.com/reference/cli/docker/image/save/", "https://docs.docker.com/build/builders/drivers/docker-container/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading multi-platform images locally

## The classic-store limit
Multi-platform images need an image store that supports manifest lists, and the classic
graph-driver store does not, so loading a `--platform linux/amd64,linux/arm64` build into it
does not work.

## Fix: use the containerd image store
- Docker Desktop and Docker Engine 29.0 and later on fresh installations use the containerd
  image store by default; an upgraded Engine keeps the legacy graph drivers (overlay2) until you
  enable it.
- Engine: on upgraded hosts set
```json
{ "features": { "containerd-snapshotter": true } }
```
  in `/etc/docker/daemon.json` and restart. Existing images and containers in the old store
  become invisible (not deleted) until you switch back. The containerd image store is not
  available with user namespace remapping (`userns-remap`).
```bash
docker info -f '{{ .DriverStatus }}'        # shows the containerd snapshotter driver type
docker buildx build --platform linux/amd64,linux/arm64 -t app:dev --load .
docker image ls --tree app:dev              # --tree is marked EXPERIMENTAL in the CLI reference
docker run --rm --platform linux/arm64 app:dev uname -m
```

## Alternatives on the classic store
```bash
# load only the native platform for local testing
docker buildx build --platform linux/amd64 -t app:dev --load .
# keep the full multi-arch result as an OCI archive instead of loading
docker buildx build --platform linux/amd64,linux/arm64 -o type=oci,dest=app.tar .
# or push to a local registry
docker run -d -p 5000:5000 --name reg registry:3
docker buildx build --platform linux/amd64,linux/arm64 -t localhost:5000/app:dev --push .
```
A `docker-container` builder runs in its own container; the Docker docs' local-registry example
creates the builder with the driver option `network=host` so that it can reach a registry on
`localhost:5000`.

## Gotchas
- `docker save` and `docker load` accept `--platform` (comma-separated `os[/arch[/variant]]`)
  to save or load only the given platforms.
- The containerd image store uses more disk space than the legacy drivers, because it keeps
  both compressed and uncompressed layers.
- Running a non-native variant needs emulation (binfmt/QEMU) on the host.

## Checked

Checked 2026-10-23 against the Docker docs containerd image store page and "Multi-platform builds" page, and the docker/cli `image ls`, `save`, `load` references (main branches).

- containerd image store default on Docker Engine 29.0+ fresh installs (not on upgrades); `features.containerd-snapshotter` daemon.json key; `docker info -f '{{ .DriverStatus }}'` verification; hidden-not-deleted behaviour when switching; not available with `userns-remap`.
- `docker image ls --tree` is experimental; `docker save` / `docker load` `--platform`; the `registry:3` image and `network=host` driver option from the Docker docs local-registry example.
- Removed the quoted classic-store error string (not found in the docs), the claim about default pull behaviour and the Docker Desktop settings label.

Method: documentation only; no commands were run.
