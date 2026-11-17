---
id: computing-software.cloud-infrastructure-engineering.docker.buildkit-advanced-features
name: buildkit-advanced-features
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, buildkit, docker-build, cache-mount, run---mount=type=cache, secret-mount, run---mount=type=secret, ssh-forwarding, dockerfile-syntax-directive, docker-container-driver, bake, docker-bake.hcl, buildx-bake, llb, frontend, dockerfile-frontend, build-context, additional-context, heredoc-dockerfile, buildkitd-toml]
level: advanced
status: docs-checked
description: "BuildKit features past classic docker build: persistent cache mounts, secret/SSH mounts that never land in layers, named contexts, heredocs, and bake."
sources: ["https://docs.docker.com/reference/dockerfile/", "https://docs.docker.com/build/buildkit/", "https://docs.docker.com/build/builders/drivers/", "https://docs.docker.com/reference/cli/docker/buildx/build/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BuildKit advanced features

**Goal:** stop paying for a cold `npm install`/`pip install` on every build, stop leaking
credentials into image layers, and use `bake` instead of a pile of `docker build` flags.
Needs `# syntax=docker/dockerfile:1` at the top of the Dockerfile to opt into the latest
frontend (BuildKit is the default builder on Docker Desktop and Engine, except for Windows containers).

## Cache mounts — the single highest-leverage trick
`RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt` persists
`/root/.cache/pip` **across builds**, outside the layer, identified by `id`, which defaults to the `target` path (set `id=` to keep separate caches for the same path). Unlike a
layer-cache hit (which requires the instruction and everything before it to be byte-identical),
a cache mount survives even when `requirements.txt` changed — only the actually-changed
packages re-download/re-compile. Use it for package manager caches (`apt`, `pip`, `npm`,
`cargo`, `go build`), not for build *output* you need in the final image (that still has to
be `COPY`'d out — cache mount contents never ship).
- `sharing` is one of `shared` (default, concurrent writers allowed), `private` (new mount if
  there are multiple writers) or `locked` (second writer waits). Use `locked` for apt caches.
- Cache mounts live in the builder's local store; see `build-cache-strategy-at-scale` for CI.

## Secret and SSH mounts
`RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm install`, invoked with
`docker build --secret id=npmrc,src=$HOME/.npmrc`. The file is mounted only for that `RUN`
step and never written to a layer — unlike `COPY secret.txt .` (which lands in the layer
forever, even if you `rm` it in a later step) or `ARG`/`ENV` secrets (visible in
`docker history` and `docker inspect`). Same idea for private git/SSH:
`RUN --mount=type=ssh git clone git@...` with `docker build --ssh default` (or
`--ssh default=$SSH_AUTH_SOCK`) gives that step access to the host's ssh-agent.

## Named/additional build contexts
`docker buildx build --build-context base=docker-image://alpine:3.19 .` or
`--build-context shared=../shared-lib` (name=value) lets a Dockerfile `FROM base` or `COPY --from=shared`
pull from something other than the main build context or a registry — useful for pinning a
base image independently of the Dockerfile text, or stitching a monorepo without a giant
shared context.

## Heredocs
```dockerfile
RUN <<EOF
set -e
apt-get update
apt-get install -y curl
EOF
```
avoids the `&&`/`\` chain and is easier to diff; also works for `COPY <<EOF /app/config.yml`
to inline small generated files without a separate source file.

## `docker buildx bake`
A `docker-bake.hcl` (or `.json`) file declares build **targets** (context, dockerfile,
args, tags, platforms, cache-from/to) so `docker buildx bake web worker` replaces a shell
script of five long `docker build` invocations, builds them in parallel, and is the natural
place to define CI's matrix of images. Groups (`group "default" { targets = [...] }`) make
`docker buildx bake` with no args build everything.

## Gotchas
- The default `docker` driver has no tarball output or multi-arch images, and cache export only
  for some backends with the containerd image store; use a `docker-container` builder
  (`docker buildx create --use`) for those. `docker buildx ls` shows the current builder.
- `--mount=type=secret` has `required` defaulting to `false`, so a missing `--secret` does not
  fail the build; add `required=true` to make the instruction error when the secret is absent.
- Cache mounts live in the builder's local state, so a fresh CI runner starts cold; see
  `build-cache-strategy-at-scale` for cache export.

## Verify
`docker history <image>` should show no secret material in any layer; re-run the same build
twice and confirm the second run reuses the cache mount (add one dependency and confirm
only it downloads).

## Checked

2026-10-26 against Docker docs (docker/docs main, commit of 2026-10-23). Confirmed in the Dockerfile reference and buildx/BuildKit docs: cache mount id default (target) and sharing values and default, secret mount required option default false (the earlier text had this inverted), --ssh forms, --build-context name=value with docker-image:// scheme, BuildKit default builder statement, driver feature table. Removed the Docker 23 version claim and unconfirmed cache-from behaviour.

Method: documentation only; no commands were run.
