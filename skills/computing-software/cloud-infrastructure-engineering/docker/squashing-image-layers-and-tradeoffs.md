---
id: computing-software.cloud-infrastructure-engineering.docker.squashing-image-layers-and-tradeoffs
name: squashing-image-layers-and-tradeoffs
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, image-slimming, layer-squash, squash, flatten-image, docker-export, docker-import, multi-stage]
level: practitioner
status: docs-checked
description: "Flatten an image into one layer (scratch copy stage, export/import, legacy --squash), what each method loses, and why squashing usually hurts pulls and caching."
sources: ["https://docs.docker.com/reference/cli/docker/image/build/#squash", "https://docs.docker.com/reference/cli/docker/container/export/", "https://docs.docker.com/reference/cli/docker/image/import/", "https://docs.docker.com/build/building/multi-stage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Squashing layers

Each layer is a tar diff, so files deleted in a later layer still ship in the earlier one.
Squashing merges layers so deleted files disappear and the layer count drops.

## Methods
**1. Multi-stage copy into scratch (works with BuildKit, keeps control)**
```dockerfile
FROM ubuntu:<version> AS fat
RUN apt-get update && apt-get install -y build-essential && ... && rm -rf /var/lib/apt/lists/*

FROM scratch
COPY --from=fat / /
# restate image metadata (ENV, WORKDIR, USER, ENTRYPOINT) in the final stage
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
WORKDIR /app
USER 1000
ENTRYPOINT ["/app/run"]
```

**2. export/import a container (flattens the filesystem)**
```bash
docker create --name tmp myimage:fat
docker export tmp | docker import \
  --change 'ENV PATH=/usr/local/bin:/usr/bin:/bin' \
  --change 'WORKDIR /app' --change 'USER 1000' \
  --change 'ENTRYPOINT ["/app/run"]' - myimage:flat
docker rm tmp
```
`docker import` applies Dockerfile instructions with `--change`; `docker export` writes the
container filesystem without volume contents. Restate the metadata you need as above.

**3. `docker build --squash`**: marked experimental in the `docker image build` reference
("Squash newly built layers into a single new layer"). Do not build new pipelines on it.

## What you lose
- **Layer sharing**: images built on the same base no longer share base layers.
- **Cache and incremental pulls**: a one-line change re-ships the whole layer.
- **History**: `docker history` shows one step.

## When it is justified
- A secret was baked into an early layer (squash, then rotate the secret anyway: old tags and
  caches still have it).
- Shipping a single self-contained artifact where sharing does not matter.
Otherwise fix the cause: combine `RUN` steps and clean up in the same step, or use a proper
multi-stage build that copies only artifacts.

## Verify
```bash
docker history myimage:flat              # one layer
docker image inspect -f '{{json .Config}}' myimage:flat
```

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), Compose file reference, tini, Trivy and metadata-action documentation. Confirmed in the docker image build, docker export and docker import references: --squash is marked experimental with the description above, docker import --change applies Dockerfile instructions, docker export excludes volume contents; multi-stage COPY --from and FROM scratch from the Dockerfile reference. Removed the unconfirmed ~125 layer limit, the parallel download claim, the daemon.json experimental detail, the claim that BuildKit ignores --squash, the scanner base-image-link claim and the pinned ubuntu tag.

Method: documentation only; no commands were run.
