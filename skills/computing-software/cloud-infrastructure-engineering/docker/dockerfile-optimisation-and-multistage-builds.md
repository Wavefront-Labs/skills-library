---
id: computing-software.cloud-infrastructure-engineering.docker.dockerfile-optimisation-and-multistage-builds
name: dockerfile-optimisation-and-multistage-builds
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, buildkit, docker-buildx, multi-stage-build, build-performance, image-size, dive, docker-history, build-checks, progress-plain, copy-link, heredoc, docker-bake, multi-platform, cross-compilation, buildplatform, targetplatform, go-static-binary, python-venv, python-wheels, uv, jlink, spring-boot-layers, source-date-epoch, reproducible-builds, cache-invalidation, optimization, optimisation]
level: advanced
status: docs-checked
description: "Measure then cut Docker build time and image size: profile BuildKit steps, find cache busts, per-language multi-stage recipes (Go, Python, Java), multi-platform cross-builds, bake and reproducibility."
sources: ["https://docs.docker.com/build/checks/", "https://docs.docker.com/build/building/multi-platform/", "https://docs.docker.com/reference/dockerfile/", "https://docs.docker.com/build/ci/github-actions/reproducible-builds/", "https://github.com/wagoodman/dive", "https://docs.astral.sh/uv/guides/integration/docker/", "https://github.com/GoogleContainerTools/distroless"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dockerfile optimisation — measuring and cutting build time and image size

**Goal:** turn "the build is slow / the image is huge" into numbers, fix the biggest item
first, and keep it fixed. The baseline rules (stage shape, layer order, cache/secret mounts,
base choice, non-root, digests) are in
`computing-software.cloud-infrastructure-engineering.docker.multi-stage-dockerfiles` — apply
those first; this skill is the optimisation pass on top.

## 1. Measure before changing anything
```bash
docker buildx build --progress=plain --no-cache . 2>&1 | tee build.log   # per-step timings
docker buildx build --check .                       # built-in build checks (lint) without building
docker image ls <IMAGE>                              # total size
docker history --no-trunc <IMAGE>                    # size and command of each layer
dive <IMAGE>                                         # per-layer files, wasted space, efficiency score
CI=true dive <IMAGE>                                 # pass/fail from the rules in .dive-ci (e.g. lowestEfficiency: 0.95)
```
Record: cold build time, warm build after a one-line source change, final image size, and
the three biggest layers. Most wins come from one of these.

## 2. Find cache busts
A warm build that re-runs `npm ci`/`pip install` means something before it changed:
- `COPY . .` or a broad `COPY src/ ...` before installing deps.
- `ARG BUILD_DATE`/`GIT_SHA` declared early and used in a `RUN` — move build metadata to
  `LABEL` in the final stage, as late as possible.
- A `.dockerignore` that misses churny files (`.git`, coverage, logs).
- CI runners with no shared cache (fix with registry/GHA cache export — see the baseline skill).
`--progress=plain` prints `CACHED` per step; the first non-cached step names the culprit.

## 3. Per-language multi-stage recipes
**Go — static binary on scratch/distroless (smallest)**
```dockerfile
FROM --platform=$BUILDPLATFORM golang:<version> AS build
ARG TARGETOS TARGETARCH
WORKDIR /src
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod go mod download
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH go build -trimpath -o /out/app ./cmd/app
FROM gcr.io/distroless/static-debian13:nonroot
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
```
Pinning the build stage to `$BUILDPLATFORM` and compiling for `TARGETOS`/`TARGETARCH` avoids
running the compiler under emulation (Docker's multi-platform guide uses the same pattern).

**Python — build wheels/venv, copy only the venv**
```dockerfile
FROM python:3.12-slim AS build
COPY --from=ghcr.io/astral-sh/uv:<PINNED_VERSION> /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen
FROM python:3.12-slim
COPY --from=build /app /app
ENV PATH="/app/.venv/bin:$PATH"
```
Compilers and `-dev` headers belong only in the build stage.

## 4. BuildKit features that pay off
- `COPY --link` (and `ADD --link`) keeps files on their own layer so they are not invalidated
  when earlier layers change.
- Heredocs keep multi-command `RUN` readable without `&& \` chains:
  `RUN <<EOF` … `EOF` (needs `# syntax=docker/dockerfile:1`).
- `docker-bake.hcl` defines targets, platforms, tags and cache in one file:
  `docker buildx bake --push` builds them in parallel with shared context.
- Multi-platform: `docker buildx build --platform linux/amd64,linux/arm64 --push .`
  produces one manifest list; it needs an image store that supports manifest lists (the
  containerd image store, the default on fresh Docker Engine 29.0+ installs) or a
  `docker-container` builder.

## 5. Reproducibility
- Set `SOURCE_DATE_EPOCH` for the build: Docker's reproducible-builds guide says the image index,
  config and file metadata timestamps then reflect that Unix time.
- Lock every dependency (lockfiles, pinned base digests, pinned tool versions in `COPY --from`).

## Gotchas
- Deleting files in a later `RUN` never shrinks the image; clean up in the same `RUN`.
- Over-splitting into many tiny stages adds complexity with no gain; optimise the measured top items only.

## Verify
- [ ] Before/after table recorded: cold build, warm build, image size, top layers.
- [ ] Warm build after a one-line code change shows dependency steps `CACHED`.
- [ ] `docker buildx build --check` is clean; `dive` efficiency gate runs in CI.
- [ ] Multi-platform manifest contains each target (`docker buildx imagetools inspect <IMAGE>`).
- [ ] Two rebuilds of the same commit produce the same digest (if reproducibility is a goal).

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), docker/cli system events reference, Compose and Scout CLI reference data, dive, uv and distroless READMEs, action repositories at their latest releases. Confirmed: docker buildx build --check / docker build --check, BuildKit COPY --link semantics, heredoc and syntax directive, multi-platform guide ($BUILDPLATFORM pattern, containerd store default from Engine 29.0), SOURCE_DATE_EPOCH guide, dive CI mode (CI=true with a .dive-ci rules file; lowestEfficiency is a rule, not a flag), uv Docker guide (UV_COMPILE_BYTECODE, UV_LINK_MODE=copy, cache mount, sync --frozen, --no-install-project), distroless static-debian13 nonroot tag. Removed the wrong dive flag, the speed-up figure, the Java layering and jlink recipe, Go linker flags, the pinned golang and distroless debian12 tags, the --no-dev flag, and unconfirmed gotchas.

Method: documentation only; no commands were run.
