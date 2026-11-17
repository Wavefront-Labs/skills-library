---
id: computing-software.software-engineering.erlang.docker-release-image
name: docker-release-image
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-containers-ci, docker-release-image]
level: practitioner
status: draft
description: "Containerising an Erlang release: build stage, prod release with ERTS, slim runtime image, SIGTERM and entrypoint."
sources:
  - https://github.com/erlef/setup-beam
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-stage Docker images for releases
**Goal:** ship a small image containing only the release.

```dockerfile
FROM erlang:27-alpine AS build
WORKDIR /src
COPY rebar.config rebar.lock ./
RUN rebar3 get-deps
COPY . .
RUN rebar3 as prod release

FROM alpine:3.20
RUN apk add --no-cache openssl ncurses-libs libstdc++
WORKDIR /app
COPY --from=build /src/_build/prod/rel/myapp ./
USER nobody
ENTRYPOINT ["/app/bin/myapp"]
CMD ["foreground"]
```
- Build and runtime base images must share the libc (musl vs glibc); with `include_erts` the runtime needs only the native libraries.
- SIGTERM triggers a graceful `init:stop/0` in the VM, so containers stop cleanly if the entrypoint is the release script run in the foreground (or `exec` it).
- Copy `rebar.config`/`rebar.lock` first so dependency layers cache.
- Set `RELEASE_COOKIE` and node name via environment; expose only needed ports.

## Gotchas
- Alpine images have a different DNS and libc behaviour; test networking and TLS roots (`public_key:cacerts_get/0` needs OS certificates present: install `ca-certificates`).
- Tag versions pinned (OTP image tag) for reproducibility.

## Self-check
Build the image, run it, `docker stop` it, and confirm a clean exit within seconds.
