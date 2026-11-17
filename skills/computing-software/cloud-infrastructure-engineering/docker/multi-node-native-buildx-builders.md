---
id: computing-software.cloud-infrastructure-engineering.docker.multi-node-native-buildx-builders
name: multi-node-native-buildx-builders
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, buildx, multi-platform, arm64, multi-node-builder, native-builders, buildx-append, remote-driver]
level: advanced
description: "Build multi-arch images without QEMU by joining native amd64 and arm64 BuildKit nodes into one buildx builder with create --append and per-node --platform."
sources: ["https://docs.docker.com/build/building/multi-platform/#multiple-native-nodes", "https://docs.docker.com/reference/cli/docker/buildx/create/", "https://docs.docker.com/build/builders/drivers/remote/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multi-node native buildx builders

**Goal:** avoid emulation by sending each platform to a machine of that architecture and
merging the result into one manifest list.

## Set up
Each node needs a reachable Docker engine (context) or a standalone `buildkitd`.
```sh
docker context create amd64-box --docker host=ssh://builder@amd64.internal
docker context create arm64-box --docker host=ssh://builder@arm64.internal

docker buildx create --name native --driver docker-container \
  --node amd64 --platform linux/amd64 amd64-box
docker buildx create --name native --append \
  --node arm64 --platform linux/arm64,linux/arm/v8 arm64-box
docker buildx inspect native --bootstrap
```
`--node` names the node, `--platform` sets fixed platforms for it, and `--append` adds a node to
an existing builder. `inspect --bootstrap` boots the builder and lists its nodes. Use the builder
per command (`--builder native`) or `docker buildx use native`.

## Build
```sh
docker buildx build --builder native --platform linux/amd64,linux/arm64 \
  -t registry.example.com/app:1.4.0 --push .
```
Each platform is built on a node that declared it, and the result is pushed as a single
multi-platform image.

## Remote buildkitd nodes (no Docker engine on the builder)
```sh
docker buildx create --name native --driver remote \
  --driver-opt cacert=ca.pem,cert=cert.pem,key=key.pem \
  --node arm64 tcp://arm64.internal:1234 --platform linux/arm64
```
Run buildkitd with `--addr tcp://0.0.0.0:1234 --tlscacert ... --tlscert ... --tlskey ...`. The
Docker docs advise against exposing BuildKit over TCP without TLS, because that allows
arbitrary access to BuildKit.

## Gotchas
- `--platform` on `docker buildx create` fixes the platforms of a node; check the platforms the
  builder reports with `docker buildx inspect`.
- Registry cache (`--cache-to` / `--cache-from type=registry,...`) is one way to share cache
  across runs.
- `--load` cannot import a multi-platform result into an image store that lacks manifest list
  support (the classic store); push to a registry, or use the containerd image store.
- `docker buildx rm native` removes the builder; `docker buildx create --name native --leave
  --node arm64` removes one node.

## Verify
`docker buildx imagetools inspect registry.example.com/app:1.4.0` lists both platforms.

## Checked

Checked 2026-10-23 against the Docker docs "Multi-platform builds" page (multiple native nodes), the docker/buildx `buildx create` reference (`--append`, `--node`, `--platform`, `--leave`, `--buildkitd-config`, `--driver-opt`) and the Docker docs remote driver page (main branches).

- Multi-node builder creation with `--append`, per-node `--platform`, and Docker Build Cloud as an alternative.
- Remote driver options `cacert`, `cert`, `key`, `servername` with a `tcp://` endpoint, and buildkitd `--addr` / `--tlscacert` / `--tlscert` / `--tlskey` flags; TLS recommendation.
- Removed the claims about the platform being only a scheduling hint, per-node cache, SSH key handling and the QEMU verification line, and the timing claim in the goal.

Method: documentation only; no commands were run.
