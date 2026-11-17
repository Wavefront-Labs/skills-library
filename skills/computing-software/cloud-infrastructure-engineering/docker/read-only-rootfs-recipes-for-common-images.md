---
id: computing-software.cloud-infrastructure-engineering.docker.read-only-rootfs-recipes-for-common-images
name: read-only-rootfs-recipes-for-common-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, read-only-rootfs, read-only-nginx, read-only-tmpfs, writable-paths, postgres, hardening]
level: practitioner
status: docs-checked
description: "Read-only (--read-only) recipes for nginx, PostgreSQL and Redis from the official image docs, in docker run and Compose form, and finding missing paths."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/#read-only", "https://docs.docker.com/engine/storage/tmpfs/", "https://hub.docker.com/_/nginx", "https://hub.docker.com/_/postgres", "https://hub.docker.com/_/redis", "https://github.com/compose-spec/compose-spec/blob/main/spec.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read-only rootfs recipes for common images

`--read-only` makes the container's root filesystem immutable. Each image needs a known set
of writable paths: give it tmpfs for scratch and volumes for data.

## nginx (official image)
The nginx image README: in read-only mode, mount a volume at every location nginx writes to;
the default configuration needs write access to `/var/cache/nginx` and `/var/run`. tmpfs
mounts serve the same purpose:
```bash
docker run -d --read-only \
  --tmpfs /var/cache/nginx --tmpfs /var/run \
  -p 8080:80 nginx
```

## PostgreSQL
Keep the data directory on a volume, and note the container's default `/dev/shm` is 64 MB,
so large queries may need `--shm-size`. The README says to mount at `/var/lib/postgresql/data`
for PostgreSQL 17 and below (mounting `/var/lib/postgresql` does not persist data there), and at
`/var/lib/postgresql` for 18 and above, where `PGDATA` is version specific:
```bash
docker run -d --read-only \
  -v pgdata:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD_FILE=/run/secrets/pg -v ./pg.txt:/run/secrets/pg:ro \
  --shm-size 256m postgres:17
```
Other writable paths are not documented in the README; discover them with `docker diff` (below).

## Redis
The README persists data under `/data`; mount a volume there:
```bash
docker run -d --read-only -v redisdata:/data redis
```

## Other runtimes (Node.js, Python, JVM)
Per-runtime writable paths are not covered by Docker's documentation; find them empirically
with `docker diff`. tmpfs mounts accept `size=` and `mode=`, and `exec` or `noexec` options.

## Compose form
Compose spec fields `read_only` and `tmpfs`:
```yaml
services:
  web:
    image: nginx
    read_only: true
    tmpfs: ["/var/cache/nginx", "/var/run"]
```

## Finding missing paths
Run once without `--read-only`, exercise the app, then `docker diff <c>`: every `A`/`C` path
outside volumes needs a tmpfs or volume. Errors like `Read-only file system` in logs name the
remaining ones.

## Checked
Date: 2026-10-26. Documentation: docker-library nginx, postgres and redis READMEs; docker/docs main (last commit 2026-10-23) tmpfs page and run reference; compose-spec `read_only` and `tmpfs`. Confirmed: nginx writable paths, Postgres shm default and the version-dependent data mount path, Redis `/data`, tmpfs options, Compose fields. Removed as unconfirmed: the Postgres `/var/run/postgresql` tmpfs, nginx templates note and nginx-unprivileged claim, Node.js, Python and JVM recipes (environment variables, gunicorn and Netty claims), the "Tested" wording, pinned tags.
Method: documentation only; no commands were run.
