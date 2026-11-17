---
id: computing-software.cloud-infrastructure-engineering.docker.oci-image-labels-and-metadata
name: oci-image-labels-and-metadata
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, labels, oci-labels, image-metadata, annotations, label-schema, org-opencontainers-image, docker-label, image-config, buildx-annotations]
level: practitioner
status: docs-checked
description: "Stamping images with org.opencontainers.image.* labels and OCI annotations at build time (source, revision, version, created), querying them, and the label vs annotation distinction."
sources: ["https://github.com/opencontainers/image-spec/blob/main/annotations.md", "https://docs.docker.com/reference/dockerfile/#label", "https://docs.docker.com/build/building/variables/", "https://docs.docker.com/reference/cli/docker/buildx/build/#annotation", "https://github.com/docker/metadata-action", "https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package", "https://docs.docker.com/engine/manage-resources/labels/", "https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/reference.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCI image labels and metadata

**Goal:** any image in the registry can answer "which commit, which repo, when, which
licence" from `docker inspect` alone, and scanners/registries render that metadata.

## The standard keys (OCI image-spec annotations.md)
Use the `org.opencontainers.image.` prefix defined by the OCI annotations spec:

| Key | Value |
|---|---|
| `created` | RFC 3339 UTC, e.g. `2026-10-15T09:12:00Z` |
| `source` | URL of the repo (`https://github.com/org/repo`) |
| `revision` | full commit SHA |
| `version` | semver or tag (`1.4.2`) |
| `url` | URL to find more information on the image |
| `documentation` | URL to get documentation on the image |
| `title`, `description`, `vendor`, `authors` (contact details), `licenses` (SPDX license expression, e.g. `Apache-2.0`) |
| `ref.name` | name of the reference for a target |
| `base.name`, `base.digest` | base image ref and digest (for provenance tooling) |

## Set them at build time, not in the Dockerfile
Hardcoding `LABEL version=1.4.2` goes stale. Declare args, fill them from CI:
```dockerfile
ARG GIT_SHA=unknown
ARG BUILD_DATE
ARG VERSION=dev
LABEL org.opencontainers.image.source="https://github.com/org/repo" \
      org.opencontainers.image.revision="$GIT_SHA" \
      org.opencontainers.image.created="$BUILD_DATE" \
      org.opencontainers.image.version="$VERSION" \
      org.opencontainers.image.licenses="MIT"
```
```bash
docker build \
  --build-arg GIT_SHA=$(git rev-parse HEAD) \
  --build-arg BUILD_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --build-arg VERSION=$(git describe --tags --always) -t app .
```
Or skip the Dockerfile entirely: `docker build --label org.opencontainers.image.revision=$SHA`
sets labels without editing the Dockerfile. In GitHub Actions, `docker/metadata-action` provides
`steps.meta.outputs.labels`; feed it to `build-push-action`'s `labels:`. Declare the build-time
`ARG`s next to the `LABEL` instruction (see `build-args-vs-environment-variables`).

## Labels vs annotations
- **Labels** describe Docker resources (images, containers, networks, volumes). Labels from a
  base or parent image are inherited by your image; if a key already exists with a different
  value, the most recently applied value wins. Visible via `docker inspect`.
- **Annotations** describe OCI image components: manifests, indexes and descriptors. They can be
  put on an image index. Set with buildx:
  ```bash
  docker buildx build --push \
    --annotation "index:org.opencontainers.image.source=https://github.com/org/repo" \
    --annotation "org.opencontainers.image.description=..." -t ghcr.io/org/app .
  ```
  The type prefix selects the level: `manifest` (the default), `index`, `manifest-descriptor`,
  comma-separated for several, with an optional `[os/arch]` platform qualifier (no wildcards).
  The Docker Engine image store cannot load images with annotations: push straight to a
  registry (`--push`).
- GitHub's docs connect a container image to a repository with a
  `LABEL org.opencontainers.image.source=https://github.com/OWNER/REPO` line in the Dockerfile.

## Query and filter
```bash
docker inspect --format '{{json .Config.Labels}}' app
docker images --filter label=org.opencontainers.image.vendor=Acme
docker ps --filter label=com.example.tier=web
docker buildx imagetools inspect ghcr.io/org/app:1.4 --raw     # annotations appear in the index JSON
```
Labels on *containers* (`docker run --label`, Compose `labels:`) use the same key rules.

## Gotchas
- Third-party keys should use reverse-DNS notation of a domain you own; `com.docker.*`,
  `io.docker.*` and `org.dockerproject.*` are reserved by Docker.
- The `MAINTAINER` instruction is deprecated; use the `org.opencontainers.image.authors` label.

## Verify
`docker inspect --format '{{index .Config.Labels "org.opencontainers.image.revision"}}' app`
returns the 40-char SHA you built from; on a pushed multi-platform image,
`docker buildx imagetools inspect --raw` shows `annotations` on the index.

## Checked

2026-10-25, against the OCI image-spec `annotations.md`, Docker docs (annotations, labels, buildx build reference, `docker/metadata-action` README), BuildKit Dockerfile reference and GitHub's connecting-a-repository-to-a-package page. Confirmed: all listed `org.opencontainers.image.*` keys and their meaning, `--annotation [type:]key=value` with `manifest`/`index`/`manifest-descriptor` types and platform qualifier, engine image store not loading annotated images, label inheritance and override order, reserved Docker namespaces, `MAINTAINER` deprecated, `docker/metadata-action` labels output, GitHub `org.opencontainers.image.source` link. Removed as unconfirmed: deprecation of the label-schema keys, registry display claims, the cache-busting claim, layer-per-LABEL claims, `--label` versus `LABEL` precedence, and jq pipelines.

Method: documentation only; no commands were run.
