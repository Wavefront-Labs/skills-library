---
id: computing-software.cloud-infrastructure-engineering.docker.copy-from-external-image-as-stage
name: copy-from-external-image-as-stage
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, multi-stage, copy-from-image, external-stage, copy-from, binary-from-image, buildkit]
level: practitioner
description: "Pull binaries and files straight out of other images with COPY --from=image:tag or a named external stage, instead of installing or compiling them."
sources: ["https://docs.docker.com/build/building/multi-stage/#use-an-external-image-as-a-stage", "https://docs.docker.com/reference/dockerfile/#copy---from", "https://docs.docker.com/build/concepts/context/#named-contexts"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Using an external image as a stage (COPY --from=image)

**Goal:** get `kubectl`, `tini`, `wait-for`, a compiled Go tool or a vendor CLI into your
image in one layer by copying it from the image that already ships it.

## Direct form
```dockerfile
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
COPY --from=registry.example.com/tools/mytool:1.2 /usr/bin/mytool /usr/local/bin/mytool
```
`--from` accepts a build stage, a named context or an image reference (a local image name, or a
tag or ID available locally or on a registry); the client pulls the image if necessary. The source
path is always resolved from the filesystem root of that image or stage.

## Named external stage
When you copy several things or want one place to bump the version:
```dockerfile
FROM registry.example.com/tools/mytool:1.2 AS mytool
FROM alpine
COPY --from=mytool /usr/bin/mytool /usr/local/bin/
```
A stage with no `RUN` of its own only contributes the image it names.

## Platform caveat
In a multi-platform build, pick the platform of an external stage explicitly when it matters:
`FROM --platform=$BUILDPLATFORM image AS tool` selects the build platform's variant, while a plain
`FROM image` uses the target platform.

## Dynamic library pitfall
A dynamically linked binary copied from a glibc image into a musl (Alpine) or static/scratch image
can fail with `not found` even though the file exists, because the dynamic loader or libraries
are missing. Prefer statically linked binaries, and also copy anything the tool needs at runtime
(CA certificates, `/etc/passwd` entries, plugin directories).

## Overriding the source at build time
```sh
docker buildx build --build-context mytool=docker-image://registry.example.com/tools/mytool:1.3 .
```
A named context passed with `--build-context` can be used as `COPY --from=mytool`, and a context
named like an image reference overrides that reference in the Dockerfile. The `docker-image://`
prefix marks the context as an image (local or in a registry), so CI can swap an image without
editing the Dockerfile.

## Gotchas
- Use `--chown=<user>:<group>` on `COPY --from` if your runtime user needs to own the files.
- Copying a directory copies its *contents* (same rule as plain COPY): write
  `COPY --from=x /usr/share/foo/ /usr/share/foo/`.
- Tag-only references can change over time; pin a digest (`image@sha256:...`) for anything that
  ships to production.

## Verify
Run the copied tool inside the built image (for example with `--version`) and check `docker history`
shows a `COPY` layer rather than an install layer.

## Checked

Checked 2026-10-23 against the Dockerfile reference (`COPY --from`, main branch of moby/buildkit docs) and the docker/docs build pages for multi-stage builds and build contexts.
Confirmed: `--from` takes an image, stage or named context; the source path is resolved from the root of that image; directory sources copy their contents; `--chown` on COPY; `--build-context name=docker-image://...` and overriding an image reference with a same-named context. Removed unconfirmed pinned image tags, the ldd command and the claim that a same-named context replaces a stage.

Method: documentation only; no commands were run.
