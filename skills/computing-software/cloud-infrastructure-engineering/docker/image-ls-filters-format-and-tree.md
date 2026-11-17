---
id: computing-software.cloud-infrastructure-engineering.docker.image-ls-filters-format-and-tree
name: image-ls-filters-format-and-tree
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, image-ls-filter, image-tree, docker-images, digests, dangling-images, image-inspect]
level: practitioner
status: docs-checked
description: "List images precisely: docker image ls filters (reference, dangling, label, before/since), --format templates, --digests, --no-trunc and --tree for multi-platform images."
sources: ["https://docs.docker.com/reference/cli/docker/image/ls/", "https://docs.docker.com/engine/cli/filter/", "https://docs.docker.com/engine/cli/formatting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# docker image ls: filters, format and tree

## Filters
```bash
docker image ls --filter reference='reg.example.com/team/*:1.*'
docker image ls --filter dangling=true                 # <none>:<none> left by rebuilds
docker image ls --filter label=org.opencontainers.image.source=https://github.com/org/app
docker image ls --filter before=myapp:1.4              # created before that image
docker image ls --filter since=myapp:1.4
```
Several `reference` filters match either pattern (logical OR), as in the Docker docs.

## Formatting
```bash
docker image ls --format 'table {{.Repository}}:{{.Tag}}\t{{.ID}}\t{{.Size}}\t{{.CreatedSince}}'
docker image ls --format json                          # one JSON object per image
docker image ls -q myapp                                # IDs only, for scripting
docker image ls --digests --no-trunc myapp              # repo digest (sha256 of manifest) and full ID
```
Placeholders: `.ID .Repository .Tag .Digest .CreatedSince .CreatedAt .Size`.

## Tree view (experimental)
```bash
docker image ls --tree
```
Lists multi-platform images as a tree; the CLI marks `--tree` as experimental.

## Gotchas
- `docker image ls` hides intermediate and dangling images unless `-a` is given.
- A dangling image is an untagged leaf image (`<none>:<none>`), typically left when a rebuild takes the tag away.

## Checked
2026-10-25, against docker/docs engine pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: filters dangling, label, before, since, reference (glob pattern; several `reference` filters are OR); `--digests`, `--no-trunc`, `-q`, `-a`, `--tree` (marked experimental); `--format` placeholders `.ID .Repository .Tag .Digest .CreatedSince .CreatedAt .Size`; json format. Removed: `until` filter (not listed for `image ls`), `.Containers` placeholder, containerd-store and tree-detail claims, IMAGE ID versus DIGEST and size-accounting claims, `jq` and sort pipelines.
Method: documentation only; no commands were run.
