---
id: computing-software.software-engineering.crystal.multi-stage-docker
name: multi-stage-docker
category: computing-software
field: software-engineering
product: crystal
tags: [multi-stage-docker, docker-static, dockerfile, multi-stage, docker-build, caching-shards, non-root, healthcheck, container, minimal-image, crystal]
level: practitioner
status: docs-checked
description: "Write a multi-stage Dockerfile that caches shards, builds a static release binary, runs as non-root and uses a minimal image."
sources:
  - https://crystal-lang.org/reference/latest/man/crystal/
  - https://crystal-lang.org/reference/latest/man/shards/
  - https://hub.docker.com/r/crystallang/crystal
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-stage Dockerfile for Crystal apps

Goal: small, cache-friendly images.

```dockerfile
FROM crystallang/crystal:1.14-alpine AS build
WORKDIR /src
COPY shard.yml shard.lock ./
RUN shards install --production
COPY src ./src
RUN shards build --release --static --no-debug

FROM scratch
COPY --from=build /src/bin/app /app
USER 10001:10001
EXPOSE 8080
ENTRYPOINT ["/app"]
```
(pin to a tag you have checked; `1.14-alpine` is only an example of the documented `x.y-alpine` tag form.)
- Docker Hub tags: `x`, `x.y`, `x.y.z` are Ubuntu-based, `-alpine` variants are Alpine-based; the images include the compiler, shards and the libraries the standard library needs. Docker Hub says no ARM images are built by the Crystal project.
- Copy `shard.yml`/`shard.lock` before sources so the dependency layer can be cached; for an application both files are checked in. `shards install --production` installs only locked, non-development dependencies and fails if the two files are out of sync.
- `shards build` builds the targets into `bin` and passes the options after it to `crystal build`; `--release` means `-O3 --single-module`, `--static` links statically and `--no-debug` drops debug symbols to shrink the file.
- This skill does not cover certificates, signals, health checks or `.dockerignore` content; check those against Docker and your app's needs.

Verify: `docker run` the image and check that the app answers.

## Checked

Checked 2026-11-08 against the `crystal` man page (build flags, optimisation), the `shards` man page (`--production`, `shards build`, lockfile advice) and the crystallang/crystal Docker Hub page (tag scheme, ARM note). Removed: the CA-certificate copy, SIGTERM and health-endpoint advice, the `.dockerignore` list, the RAM and QEMU gotchas and the `--threads` suggestion, none of which the cited pages state.

Method: docs-only read of cited pages, 2026-11-08
