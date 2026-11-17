---
id: computing-software.cloud-infrastructure-engineering.docker.setting-and-querying-image-labels
name: setting-and-querying-image-labels
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, labels, oci-labels, build-label-flag, dynamic-labels, label-filter, inspect-labels, crane-config, image-metadata]
level: practitioner
description: "Stamp build-time labels via --label or ARG, then find and read them with --filter label=, docker inspect templates and crane config without pulling."
sources: ["https://docs.docker.com/engine/manage-resources/labels/", "https://docs.docker.com/reference/cli/docker/buildx/build/#label", "https://docs.docker.com/reference/cli/docker/container/ls/#filter", "https://docs.docker.com/reference/cli/docker/image/prune/", "https://docs.docker.com/reference/dockerfile/#label", "https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_config.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting and querying image labels

## Dynamic labels at build time
```sh
docker build \
  --label org.opencontainers.image.revision="$(git rev-parse HEAD)" \
  --label org.opencontainers.image.created="$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  -t app:1 .
```
Or through ARG so the Dockerfile documents them:
```dockerfile
ARG GIT_SHA=unknown
ARG BUILD_DATE
LABEL org.opencontainers.image.revision=$GIT_SHA \
      org.opencontainers.image.created=$BUILD_DATE
```
Put these LABEL lines **last** in the final stage so a changing value does not invalidate
earlier layers. In CI `docker/metadata-action` emits the OCI label set (see
`labels-and-annotations-from-metadata-action`).

## Filtering by label
```sh
docker ps --filter label=com.example.team=payments
docker ps -a --filter label=com.docker.compose.project=shop
docker images --filter label=org.opencontainers.image.source
docker image prune -a --filter label!=keep=true
docker system prune --filter label=env=ci
```
`label=key` matches presence, `label=key=value` an exact value, and for prune
`label!=key` or `label!=key=value` selects images without the label. Using the same filter key
twice is a logical OR, different keys are ANDed.

## Reading labels
```sh
docker image inspect -f '{{json .Config.Labels}}' app:1
docker inspect -f '{{index .Config.Labels "org.opencontainers.image.revision"}}' app:1
docker ps --format '{{.Names}}\t{{.Label "com.docker.compose.service"}}'
# remote, no pull
crane config registry.example.com/app:1
skopeo inspect docker://registry.example.com/app:1
```
Use `index` for label keys that contain dots; `.Label` is available in `docker ps` format strings.

## Gotchas
- Labels in base images (the `FROM` line) are inherited by your image; if a label already exists
  with a different value, the most recent value is used.
- Docker reserves the `com.docker.*`, `io.docker.*` and `org.dockerproject.*` label namespaces;
  use reverse-DNS keys for your own labels.
- Labels are not annotations: annotations are metadata on manifests and indexes (`buildx build
  --annotation`), labels are part of the image config.

## Verify
`docker image inspect` shows the revision matching `git rev-parse HEAD`; the filter returns
exactly the expected containers.

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), Compose file reference, tini, Trivy and metadata-action documentation. Confirmed: docker ps, images, image prune and system prune label filters (including label!= for prune and OR/AND rules), docker ps --format .Label, inherited labels behaviour and reserved label namespaces (Dockerfile reference and labels guide), buildx --annotation, crane config and skopeo inspect usage. Removed the jq pipelines, the unconfirmed claims about CLI labels and the cache, container label merging, and crane platform handling.

Method: documentation only; no commands were run.
