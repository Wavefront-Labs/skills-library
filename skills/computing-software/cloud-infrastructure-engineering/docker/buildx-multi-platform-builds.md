---
id: computing-software.cloud-infrastructure-engineering.docker.buildx-multi-platform-builds
name: buildx-multi-platform-builds
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, buildx, multi-arch, multi-platform, qemu, binfmt, tonistiigi/binfmt, buildplatform, targetplatform, targetarch, targetos, cross-compilation, manifest-list, oci-image-index, imagetools, docker-container-driver, kubernetes-driver, remote-driver, build-matrix]
level: advanced
status: docs-checked
description: "buildx multi-arch builds in depth: QEMU emulation vs TARGETPLATFORM cross-compilation, builder drivers, manifest-list anatomy, and the CI matrix-vs-single-build tradeoff."
sources: ["https://docs.docker.com/build/building/multi-platform/", "https://docs.docker.com/reference/cli/docker/buildx/build/#platform", "https://github.com/tonistiigi/binfmt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# buildx multi-platform builds, in depth

**Goal:** ship one tag (`app:1.2.3`) that resolves to the right architecture on any pull —
and know whether your build is actually compiling for the target or limping through
instruction-by-instruction emulation. `dockerfile-optimisation-and-multistage-builds`
mentions the one-line command; this is the mechanics underneath it, the failure modes, and
the CI-architecture decision.

## Two different ways to get arm64 output
1. **QEMU emulation** — binfmt handlers (bundled with official BuildKit and Docker Desktop, or
   installed with `docker run --privileged --rm tonistiigi/binfmt --install all`) route an
   arm64 binary's execution through a userspace QEMU translator even on an amd64 host.
   Every `RUN` in the Dockerfile executes emulated; the Docker docs warn this can be much
   slower than native builds, especially for compilation and compression.
2. **Cross-compilation** — the build runs natively on the host arch, using
   `--platform=$BUILDPLATFORM` on the builder stage and the compiler's own cross-target flag
   (`GOARCH=$TARGETARCH` for Go, `--target=` for clang/rustc) to produce a `$TARGETARCH`
   binary without ever emulating. BuildKit auto-populates `BUILDPLATFORM`, `TARGETPLATFORM`,
   `TARGETOS`, `TARGETARCH`, `TARGETVARIANT` as build args — no manual wiring needed:
   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM --platform=$BUILDPLATFORM golang:alpine AS build
   ARG TARGETOS TARGETARCH
   RUN GOOS=$TARGETOS GOARCH=$TARGETARCH CGO_ENABLED=0 go build -o /out/app
   FROM --platform=$TARGETPLATFORM alpine
   COPY --from=build /out/app /app
   ```
   Only the final stage runs at `$TARGETPLATFORM`; everything before it stays on the fast
   native host arch. This is the pattern to reach for any time the toolchain supports cross
   compiling (Go almost always does; C/C++ with vendored native deps often doesn't).

## Builder drivers
Multi-platform images need an image store that supports manifest lists. Docker Desktop and
Docker Engine 29.0+ use the containerd image store by default, which supports them out of the
box. On an older Engine (or one upgraded with classic storage), either enable the containerd
image store or create a `docker-container` builder:
```bash
docker buildx create --name container-builder --driver docker-container --bootstrap --use
```
Images built by a `docker-container` builder are not loaded into the Engine image store;
push them with `--push`. Docker Build Cloud (`docker buildx create --driver cloud
<ORG>/<BUILDER_NAME>`) provides managed native multi-node builders.

## Manifest lists / OCI image index
`docker buildx build --platform linux/amd64,linux/arm64 --push -t app:1.2.3 .` produces one
manifest **index** referencing one manifest per platform. `docker buildx imagetools inspect
app:1.2.3` shows exactly what's in it — the fastest way to confirm a release actually
shipped both arches (don't trust the build log alone; a silent `--platform` typo like
`linux/arm` vs `linux/arm64` produces a real but wrong-arch image). `docker buildx imagetools
create` can assemble a manifest list from separately-built, separately-pushed single-arch
images — useful when different CI runners build different arches natively and you stitch
the index afterward instead of QEMU'ing everything on one runner.

## Native-runner matrix vs single emulated build
Two valid CI strategies:
- **Single build, QEMU for the non-native arch** — simplest pipeline; emulation can be much
  slower, so it suits small, fast-compiling images.
- **Matrix of native runners** (an amd64 runner and an arm64 runner) each building their own
  platform natively, then `imagetools create` to merge. This avoids emulation, at the cost of
  needing arm64 CI capacity.
Pick based on how CPU-heavy the build is and whether arm64 CI minutes are already available
— not reflexively the fancier option.

## Gotchas
- Emulation needs registered binfmt handlers. Official BuildKit releases bundle QEMU user-mode
  emulators; if emulation fails (for example with a third-party BuildKit package) install them
  with `docker run --privileged --rm tonistiigi/binfmt --install all`, which needs Linux
  kernel 4.8 or later and `fix_binary` registration.
- A builder stage whose `FROM` is not pinned with `--platform=$BUILDPLATFORM` runs at the target
  platform, which means emulation on a non-native builder.
- Check that every base image has a variant for each target platform before committing to a
  multi-platform build.

## Verify
`docker buildx imagetools inspect app:1.2.3` lists every intended platform; pull and `docker
run --rm app:1.2.3 uname -m` on both an amd64 and an arm64 host returns the matching architecture.

## Checked

Checked 2026-10-23 against the Docker docs "Multi-platform builds" page (docker/docs main branch) and the docker/buildx `build --platform` reference.

- Prerequisites: containerd image store default on Docker Desktop and Docker Engine 29.0+, `docker-container` builder alternative and its `--push` requirement.
- Three strategies (QEMU, multiple native nodes, cross-compilation); `BUILDPLATFORM` / `TARGETPLATFORM` are predefined build args; `--platform=$BUILDPLATFORM` on `FROM` avoids emulation.
- `tonistiigi/binfmt --install all` and its prerequisites; `docker buildx create --driver cloud`.
- Removed the 5-20x slowdown figure, the pinned `golang:1.22` tag, the GitHub arm runner label and the claim that the `docker` driver cannot push multi-platform images (true only for the classic store).
- `docker buildx imagetools create` builds a manifest list from source manifests that already exist in the registry (docker/buildx reference).

Method: documentation only; no commands were run.
