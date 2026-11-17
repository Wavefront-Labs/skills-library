---
id: computing-software.cloud-infrastructure-engineering.docker.build-cache-key-and-invalidation-rules
name: build-cache-key-and-invalidation-rules
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, layer-caching, cache-key-rules, arg-cache-invalidation, cache-invalidation, buildkit, dockerfile]
level: advanced
status: docs-checked
description: "Know exactly what busts a BuildKit cache step: RUN command text, COPY/ADD content checksums, ARG first use, base digest, and what never counts (mtime, secrets, cache mounts)."
sources: ["https://docs.docker.com/build/cache/invalidation/", "https://docs.docker.com/reference/dockerfile/#impact-on-build-caching", "https://docs.docker.com/reference/cli/docker/buildx/history/inspect/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Build cache key and invalidation rules

Once one step misses the cache, **every later step in that stage** re-runs. Order the
Dockerfile from least to most frequently changing input, and know what each instruction keys on.

## General rules (Docker build cache invalidation docs)
- The builder first checks whether the base image is cached, then compares each instruction with
  cached layers; if no cached layer matches exactly, the cache is invalidated.
- For `ADD`, `COPY` and `RUN --mount=type=bind` the builder computes a cache checksum from file
  metadata; a change to any involved file invalidates the cache. The modification time (`mtime`)
  is not part of that checksum.
- Other instructions are matched on the instruction text: for `RUN apt-get -y update` the files it
  changed are not examined, only the command string.
- After an invalidation all later instructions are rebuilt.
- A `RUN` cache entry is not refreshed automatically: rebuilding a week later with
  `RUN apk add curl` gives the same packages. To force re-execution change an earlier layer,
  run `docker builder prune`, or use `--no-cache` or `--no-cache-filter <stage>`.
- `WORKDIR` respects the `SOURCE_DATE_EPOCH` build arg: changing it invalidates `WORKDIR` and every
  later instruction. Use a fixed value (for example `0`) for reproducible builds that keep cache.
- Build secret contents are not part of the cache key, so changing a secret does not invalidate
  the cache; its id and mount path do. To force invalidation pass a changing build arg
  (for example `ARG CACHEBUST`).

## ARG rules
- An `ARG` whose value differs from the previous build causes a miss at its first **use**, not its
  declaration. All `RUN` instructions after an `ARG` use it implicitly as an environment variable,
  so a changed value causes a miss at the next `RUN` even if the command does not mention it.
- An `ENV` that references an `ARG` (`ENV V=$V`) causes the miss at the `ENV` line, because the value
  is persisted in the image.
- Predefined `ARG`s (such as the proxy variables) are exempt from caching unless a matching `ARG`
  statement is in the Dockerfile.
- So declare `ARG VERSION` / `ARG GIT_SHA` as late as possible, right before the step needing it:
```dockerfile
COPY package.json package-lock.json ./
RUN npm ci                     # stays cached when GIT_SHA changes
COPY . .
ARG GIT_SHA                    # declared here, not at the top
RUN echo "$GIT_SHA" > /app/REVISION
```

## Classic traps
- `RUN apt-get update` alone in a layer is cached until something earlier changes, so a later
  `apt-get install` may use stale package lists; run them in one `RUN`.
- `COPY . .` early: any source change invalidates the dependency install below it. Copy the
  dependency manifests first and keep unneeded files out with `.dockerignore`.
- A changing value baked in near the top (a timestamp argument, `SOURCE_DATE_EPOCH` set from a
  commit time) invalidates everything after it.
- Changing file metadata (mode, ownership as seen by `COPY`) changes the checksum.

## Verify
```bash
docker build --progress=plain .
docker buildx history inspect
```
Change one input at a time (source file, build arg) and note the first step that stops saying
`CACHED`.

## Checked

Checked 2026-10-23 against docker/docs "Build cache invalidation" and the Dockerfile reference (ARG "Impact on build caching", SOURCE_DATE_EPOCH).
Confirmed: base-image-then-instruction comparison, file metadata checksum for ADD/COPY/bind mounts without mtime, RUN keyed on the command string, `--no-cache` and `--no-cache-filter`, SOURCE_DATE_EPOCH and WORKDIR, secrets excluded from the key, ARG and ENV miss behaviour, predefined ARG exemption. Removed the per-instruction key table, which asserted behaviour (FROM digest re-resolution, `ADD <url>` and `--exclude` handling, mount options) that the documentation does not state.

Method: documentation only; no commands were run.
