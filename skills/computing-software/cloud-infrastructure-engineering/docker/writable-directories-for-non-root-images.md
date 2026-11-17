---
id: computing-software.cloud-infrastructure-engineering.docker.writable-directories-for-non-root-images
name: writable-directories-for-non-root-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, non-root, nonroot-writable-dirs, copy-chown, file-ownership, user-instruction, volumes]
level: practitioner
status: docs-checked
description: "Make non-root images work: create and own writable dirs before USER, COPY --chown/--chmod, volume mountpoint population, and keeping app code read-only."
sources: ["https://docs.docker.com/reference/dockerfile/#copy---chown---chmod", "https://docs.docker.com/reference/dockerfile/#user", "https://docs.docker.com/engine/storage/volumes/#populate-a-volume-using-a-container"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writable directories for non-root images

After switching to `USER app`, the usual failures are `EACCES` on cache dirs, pid files,
uploads and log files. Decide which paths are writable, own exactly those, and keep the rest
root-owned and read-only.

## Pattern
```dockerfile
FROM python:3.13-slim
RUN groupadd -r -g 10001 app && useradd -r -u 10001 -g app -d /app -s /sbin/nologin app

WORKDIR /app
# code: owned by root, readable by all -> the app cannot modify itself
COPY --chmod=755 --chown=root:root . /app

# writable paths: created and owned before USER, so volumes mounted there inherit their content
RUN mkdir -p /app/data /app/tmp && chown 10001:10001 /app/data /app/tmp && chmod 0750 /app/data /app/tmp

USER 10001:10001
ENV TMPDIR=/app/tmp
VOLUME ["/app/data"]
```

## Why each choice
- `COPY --chown=<user>[:<group>]` and `--chmod` set ownership and mode as files are copied. Names are resolved by
  BuildKit from `/etc/passwd` and `/etc/group` in the image root filesystem, and the build fails if they are missing
  there; numeric IDs need no lookup. With only `--chown=1000:` a numeric UID uses the same number for the GID.
- `--chmod` accepts octal (`755`) and symbolic (`g=u`; symbolic needs Dockerfile syntax 1.14 or later).
- `USER` sets the default user and group for later `RUN` instructions and for `ENTRYPOINT` and `CMD`. A user with no
  primary group runs with the root group.
- Create the directory **in the image** where you want a named volume: when an empty volume is mounted on a directory
  that has content in the image, Docker copies that content into the volume by default (disable with
  `volume-nocopy`). A non-empty volume obscures the image's content instead.
- `VOLUME` only declares a mount point; you cannot mount a host directory from a Dockerfile.

## Gotchas
- `WORKDIR` creates a missing directory even if later instructions never use it; create and own the directories
  you need explicitly.
- Changing the UID later breaks existing volumes owned by the old UID; pick a stable UID once.
- Make the app's cache, temp and log paths point at the directories you own (for example `TMPDIR`), or mount a writable
  `tmpfs`/volume there.

## Verify
```bash
docker run --rm --entrypoint sh <img> -c 'id; ls -ld /app /app/data /app/tmp; touch /app/x'   # last one should fail
```

## Checked
2026-10-28. Confirmed on the Dockerfile reference (COPY --chown/--chmod behaviour and symbolic-mode version, name
resolution via /etc/passwd, USER, VOLUME, WORKDIR creation) and Docker's "Populate a volume using a container" page
(empty-volume copy, volume-nocopy, obscuring of non-empty volumes). Removed (not in the fetched pages): the claim that
a `RUN chown -R` layer can double image size, the "BuildKit needed for --chmod" claim, the per-runtime table (Python,
Node, Java, nginx, Rails paths), the claim that volumes inherit ownership, and the read-only/tmpfs run check.
Method: documentation only; no commands were run.
