---
id: computing-software.software-engineering.assembly.docker-multiarch
name: docker-multiarch
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, docker-multiarch, asm-containers-ci]
level: practitioner
status: docs-checked
description: "Containerised assembly builds for several CPU architectures with Docker buildx: --platform, QEMU emulation, native nodes and BUILDPLATFORM/TARGETARCH."
sources:
  - https://docs.docker.com/build/building/multi-platform/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker multi-arch builds
**Goal:** build assembly for linux/amd64 and linux/arm64 in reproducible containers.

```sh
docker buildx build --platform linux/amd64,linux/arm64 .
# install QEMU emulators and register them with binfmt_misc on the host
docker run --privileged --rm tonistiigi/binfmt --install all
```
```dockerfile
# run the build stage on the builder's own architecture (no emulation)
FROM --platform=$BUILDPLATFORM debian AS build
ARG TARGETARCH
# pick AArch64 or x86-64 sources / assembler flags from $TARGETARCH
```
- A container shares the host kernel, so code inside must match the host architecture; a linux/amd64 container does not run on an arm64 host without emulation.
- A multi-platform build packages several variants of the same image into one. The `--platform` flag lists the targets.
- Three ways to build for another architecture: QEMU emulation, a builder with multiple native nodes, or cross-compilation in a multi-stage build.
- Emulation needs no Dockerfile change, but can be much slower than native builds, especially for compilation. Docker Desktop supports it by default; official BuildKit releases bundle QEMU user-mode emulators, and the `tonistiigi/binfmt` command above is the fallback install.
- `BUILDPLATFORM` and `TARGETPLATFORM` are available automatically; `TARGETOS` and `TARGETARCH` need an `ARG` line in the stage that uses them. Pinning `FROM` with `--platform=$BUILDPLATFORM` stops emulation from kicking in for that stage.
- An assembler selected per target (for example one assembler for x86-64 sources and GNU `as` for AArch64 sources) is your own build logic: branch on `$TARGETARCH` in the Dockerfile or Makefile.

## Gotchas
- A Dockerfile without the `--platform=$BUILDPLATFORM` pin and `ARG` lines falls back to emulation for every target.

## Self-check
Build for both platforms and print `TARGETARCH` in each build stage to confirm which variant ran.

## Checked
2026-11-08. Checked against the Docker multi-platform builds page: the `--platform` flag, the three strategies, QEMU speed note and bundled emulators, the `tonistiigi/binfmt --install all` command, `BUILDPLATFORM`, `TARGETPLATFORM`, `TARGETOS`, `TARGETARCH` and the need for `ARG`. Removed (not on that page): the Debian/apt Dockerfile and package list, the NASM x86-only claim, `docker run --platform`, the SYS_PTRACE and seccomp advice, image pinning and the Apple Silicon remark. Replaced the unrelated LLVM docs source.

Method: documentation only; no commands were run.
