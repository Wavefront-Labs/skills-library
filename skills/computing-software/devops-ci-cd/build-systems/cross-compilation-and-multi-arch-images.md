---
id: computing-software.devops-ci-cd.build-systems.cross-compilation-and-multi-arch-images
name: cross-compilation-and-multi-arch-images
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, cross-compilation, multi-arch, multi-platform-images, qemu, binfmt, buildx-platforms, docker-buildx, manifest-list, oci-image-index, imagetools, native-arm-runners, cross-compilation-vs-emulation, targetplatform, buildplatform, goos-goarch, cgo-cross, rust-cross, cargo-zigbuild, cross-rs, musl-static, cmake-toolchain-file, zig-cc, arm64, graviton, apple-silicon, exec-format-error, platform-mismatch, buildkit, sysroot, cross-toolchain]
level: advanced
status: draft
description: "Build for amd64 and arm64 from one pipeline: cross-compile with BUILDPLATFORM/TARGETPLATFORM instead of QEMU, Go/Rust/C toolchain specifics, buildx manifest lists, native ARM runners."
sources: ["https://docs.docker.com/build/building/multi-platform/", "https://docs.docker.com/build/ci/github-actions/multi-platform/", "https://go.dev/doc/install/source#environment", "https://github.com/cross-rs/cross", "https://github.com/rust-cross/cargo-zigbuild", "https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-compilation and multi-arch images

**Goal:** one `docker buildx build --platform linux/amd64,linux/arm64` that finishes in
minutes (not the 10× QEMU slowdown), produces a single tag that pulls the right image on
any node, and doesn't surprise you with `exec format error` at 2 am.

## 1. Emulation vs cross-compilation
- **QEMU emulation** (`docker/setup-qemu-action`, `binfmt`): run the *target* arch's
  userland on the build host. Zero code changes; 5–20× slower for compile-heavy steps;
  occasional emulator bugs (JIT-heavy builds, Node/Java under qemu-aarch64 can hang or
  segfault). Fine for `apk add` + copying prebuilt binaries; wrong for compiling.
- **Cross-compilation**: run the host's native compiler and emit target-arch binaries.
  Fast; needs toolchain support (Go: trivial; Rust: good with the right linker; C/C++:
  needs a cross toolchain and target sysroot).
- **Native builders**: an arm64 runner (GitHub `ubuntu-24.04-arm`, GitLab SaaS arm64
  runners, Graviton self-hosted, Apple Silicon) builds arm64 natively; combine with
  amd64 runners and merge manifests. Best for C/C++/Java/Node where cross is painful.
Pick per layer: cross-compile the app, emulate (or pre-build) only trivial OS layers.

## 2. Dockerfile pattern: build on the host arch, target the other
```dockerfile
# syntax=docker/dockerfile:1.7
FROM --platform=$BUILDPLATFORM golang:1.23-alpine AS build
ARG TARGETOS TARGETARCH TARGETVARIANT
WORKDIR /src
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod go mod download
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH GOARM=${TARGETVARIANT#v} \
    go build -trimpath -ldflags="-s -w" -o /out/app ./cmd/app

FROM gcr.io/distroless/static:nonroot            # pulled for TARGETPLATFORM automatically
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
```
`--platform=$BUILDPLATFORM` on the build stage = runs natively; the final stage is
resolved per target platform. Without that `--platform`, BuildKit emulates the *whole*
build stage. `TARGETPLATFORM`/`TARGETOS`/`TARGETARCH`/`TARGETVARIANT` (and `BUILD*`)
are automatic build args — declare them with `ARG` in the stage that uses them.

Rust:
```dockerfile
FROM --platform=$BUILDPLATFORM rust:1.82 AS build
ARG TARGETARCH
RUN apt-get update && apt-get install -y gcc-aarch64-linux-gnu && rustup target add aarch64-unknown-linux-gnu x86_64-unknown-linux-gnu
ENV CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU_LINKER=aarch64-linux-gnu-gcc
RUN case "$TARGETARCH" in amd64) T=x86_64-unknown-linux-gnu;; arm64) T=aarch64-unknown-linux-gnu;; esac && \
    cargo build --release --target $T && cp target/$T/release/app /out/app
```
Simpler: `cargo-zigbuild` (`cargo zigbuild --target aarch64-unknown-linux-gnu.2.28` uses
zig as a C cross-compiler/linker, handles glibc version targeting) or `cross` (runs
builds in per-target containers, uses QEMU only for tests). C deps (openssl, sqlite):
prefer `vendored` features or musl static targets (`*-unknown-linux-musl`) to dodge sysroots.

C/C++: cross toolchain packages (`gcc-aarch64-linux-gnu`, `g++-aarch64-linux-gnu`) +
CMake toolchain file (`CMAKE_SYSTEM_NAME=Linux`, `CMAKE_SYSTEM_PROCESSOR=aarch64`,
`CMAKE_C_COMPILER=aarch64-linux-gnu-gcc`, `CMAKE_FIND_ROOT_PATH=/sysroot/arm64`), or
`zig cc -target aarch64-linux-gnu` as a drop-in `CC`. Tests that must *run* still need
QEMU (`qemu-aarch64-static ./test`) or a native runner.

Node/Python: pure code is arch-agnostic; native modules (`sharp`, `bcrypt`, `grpc`,
numpy wheels) need prebuilt binaries for the target — `npm ci --platform=linux --arch=arm64`
(npm ≥ 10 respects `npm_config_arch` for optional deps), `pip download --platform manylinux2014_aarch64 --only-binary=:all:`,
or build those layers natively/emulated.

JVM: bytecode is portable; only the base JDK image differs → multi-arch base image
(`eclipse-temurin:21` is a manifest list), build the jar once on any arch, `COPY` it.

## 3. buildx and manifest lists
```bash
docker buildx create --name multi --driver docker-container --use
docker buildx build --platform linux/amd64,linux/arm64 \
  -t ghcr.io/example/app:$SHA --push \
  --cache-from type=registry,ref=ghcr.io/example/app:buildcache \
  --cache-to type=registry,ref=ghcr.io/example/app:buildcache,mode=max \
  --provenance=mode=max --sbom=true .
docker buildx imagetools inspect ghcr.io/example/app:$SHA      # shows the index + per-platform manifests
```
`--push` is required for multi-platform (the local docker store can't hold an index
before Docker 25 containerd image store; `--load` only works for a single platform).
The result is an **OCI image index** (manifest list): one tag, N platform manifests,
plus attestation manifests (`unknown/unknown` platform entries — normal). Registries
without index support (old Nexus) need `--provenance=false` or per-arch tags.

Split-and-merge with native runners (fastest for heavy builds):
```yaml
build:
  strategy: { matrix: { include: [{ platform: linux/amd64, os: ubuntu-24.04 }, { platform: linux/arm64, os: ubuntu-24.04-arm }] } }
  runs-on: ${{ matrix.os }}
  steps:
    - uses: docker/build-push-action@v6
      with: { platforms: "${{ matrix.platform }}", outputs: "type=image,name=ghcr.io/example/app,push-by-digest=true,name-canonical=true,push=true" }
    # export digest as an artifact
merge:
  needs: build
  steps:
    - run: docker buildx imagetools create -t ghcr.io/example/app:$SHA ghcr.io/example/app@sha256:AMD ghcr.io/example/app@sha256:ARM
```
`docker buildx bake` with `platforms` per target and `--set` does the same declaratively.

## 4. Errors you will meet
| symptom | cause / fix |
|---|---|
| `exec /app: exec format error` | binary built for the wrong arch; check `file /app`, `docker image inspect --format '{{.Architecture}}'`; in Dockerfile the build stage lacked `--platform=$BUILDPLATFORM` + `GOARCH`, or a base image is single-arch |
| `no match for platform in manifest` | base image has no arm64 variant; pick another tag (`-alpine`, `-bookworm` usually have both) or build it yourself |
| build 10× slower on arm64 | emulation; move compile to `$BUILDPLATFORM` stage or native runner |
| `cannot execute binary file` during build | `RUN` of a target-arch tool in a cross stage; run it in a `--platform=$TARGETPLATFORM` stage or use the host tool |
| Go cgo errors | set `CGO_ENABLED=0` or provide `CC=aarch64-linux-gnu-gcc`; `CGO_ENABLED=0` breaks `net` DNS on some setups → `-tags netgo` |
| Rust `linker 'cc' not found`/wrong `cc` | set `CARGO_TARGET_<TRIPLE>_LINKER`; zigbuild avoids it |
| glibc version too new at runtime | cross-built against host glibc; target older via zig (`.2.28`), musl static, or build in an older base |
| node native module `invalid ELF header` | `node_modules` built for host arch copied into target image; install in a target-platform stage |
| QEMU hangs/segfaults | emulator bug; `tonistiigi/binfmt:latest` update, or avoid emulation for that step |
| ARM v7 (`linux/arm/v7`) builds fail | 32-bit targets need `GOARM`, musl 32-bit toolchains; most teams drop armv7 unless Raspberry Pi matters |

## 5. Testing and verification
Run the test suite natively on each arch at least on main (matrix of native runners);
smoke-run the built image under QEMU in CI if no native runner exists
(`docker run --platform linux/arm64 ghcr.io/example/app:$SHA --version`). Verify the
index: `docker buildx imagetools inspect` lists exactly the platforms you intend; pull on
an arm64 node and check `uname -m` inside. Pin base images by digest of the **index**
(multi-arch digest), not of one platform manifest.

## Verify
- [ ] `imagetools inspect` shows `linux/amd64` and `linux/arm64` manifests under one tag; attestations present.
- [ ] arm64 image starts on an arm64 node (Graviton/Apple Silicon/Pi) and amd64 on x86; no `exec format error`.
- [ ] Multi-arch build time is < 2× single-arch (compile happens natively/cross, not under QEMU).
- [ ] Tests run natively on both arches on main; native-module layers are built per platform.
