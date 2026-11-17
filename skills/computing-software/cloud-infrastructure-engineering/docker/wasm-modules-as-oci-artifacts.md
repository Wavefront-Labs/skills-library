---
id: computing-software.cloud-infrastructure-engineering.docker.wasm-modules-as-oci-artifacts
name: wasm-modules-as-oci-artifacts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, oci-artifacts, wasm-oci, webassembly, wasi, oras, wasm-to-oci]
level: advanced
status: docs-checked
description: "Distribute WebAssembly modules via OCI registries: scratch images with a .wasm entrypoint vs the CNCF Wasm artifact layout, pushing with buildx or oras, runtime support."
sources: ["https://docs.docker.com/desktop/features/wasm/", "https://github.com/containerd/runwasi/blob/main/crates/oci-tar-builder/README.md", "https://github.com/containerd/runwasi/blob/main/docs/src/getting-started/demos.md", "https://github.com/bytecodealliance/wasm-pkg-tools", "https://github.com/oras-project/oras/blob/main/cmd/oras/root/push.go", "https://doc.rust-lang.org/rustc/platform-support/wasm32-wasip1.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wasm modules as OCI artifacts

Two packaging conventions exist; pick by consumer.

## 1. "Wasm image": scratch image with the module as entrypoint
Used by Docker's Wasm support (containerd shims via runwasi) and many Kubernetes Wasm
runtimes.
```dockerfile
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM rust:<version> AS build
RUN rustup target add wasm32-wasip1
WORKDIR /src
COPY . .
RUN cargo build --release --target wasm32-wasip1

FROM scratch
COPY --from=build /src/target/wasm32-wasip1/release/app.wasm /app.wasm
ENTRYPOINT ["/app.wasm"]
```
```bash
docker buildx build --platform wasi/wasm -t reg.example.com/app-wasm:1.0 --push .
docker run --rm --runtime=io.containerd.wasmtime.v1 --platform=wasi/wasm reg.example.com/app-wasm:1.0   # Docker's docs show io.containerd.wasmedge.v1; runwasi also provides wasmtime, wasmer and wamr shims
```
`--platform wasi/wasm` selects the Wasm platform. Docker's own Wasm workloads feature in Docker
Desktop is documented as Beta and deprecated (to be removed in a future release).

## 2. CNCF Wasm OCI artifact
A dedicated layout (`application/vnd.wasm.config.v0+json` config, layers of
`application/wasm`) produced by Wasm tooling (for example `wkg publish` from wasm-pkg-tools, or runwasi's
`oci-tar-builder`). The runwasi README shows such an artifact: config media type
`application/vnd.wasm.config.v0+json` and a layer with media type `application/wasm`.
Generic push with oras (`--config` sets the config blob and its media type):
```bash
oras push reg.example.com/components/greeter:1.0 \
  --config config.json:application/vnd.wasm.config.v0+json \
  greeter.wasm:application/wasm
oras pull reg.example.com/components/greeter:1.0
```

## Choosing
| Need | Convention |
|---|---|
| `docker run` / containerd shim / Kubernetes RuntimeClass | Wasm image (scratch + entrypoint) |
| Component registries and tooling such as `wkg` | Wasm OCI artifact |

## Gotchas
- Docker Desktop's Wasm workloads need the containerd image store and the Wasm option turned on
  (Settings, Beta features); the feature is deprecated.
- runwasi's demos note that containerd's `ctr` can fail with `unknown image config media type
  application/vnd.wasm.config.v0+json` for the artifact form: use the image form with `ctr`.
- Registries must accept the custom media types for the artifact form; test with your registry.

## Checked

2026-10-25, against Docker Desktop's Wasm docs, containerd/runwasi `oci-tar-builder` README and demos, wasm-pkg-tools README, ORAS `push.go`, and the rustc platform-support page for `wasm32-wasip1`. Confirmed: `wasi/wasm` platform with `docker buildx build`, `--runtime` and `--platform` flags on `docker run`, runwasi shim names, Wasm artifact config and layer media types, `oras push --config file:mediatype`, `wkg publish`, tier-2 `wasm32-wasip1`. Corrected: `wkg oci push` is not documented (use `wkg publish`); an `--artifact-type` push does not set the config media type; Docker Desktop Wasm workloads are deprecated. Removed the unconfirmed registry list, signing remark and pinned Rust version.

Method: documentation only; no commands were run.
