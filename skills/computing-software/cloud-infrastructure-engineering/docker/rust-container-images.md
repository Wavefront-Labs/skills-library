---
id: computing-software.cloud-infrastructure-engineering.docker.rust-container-images
name: rust-container-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, rust, cargo-chef, rust-musl, multi-stage, language-images, static-binary]
level: practitioner
description: "Build small, cache-friendly Rust images: cargo-chef dependency layers or cache mounts, musl static targets for scratch, and glibc distroless runtimes."
sources: ["https://github.com/LukeMathWalker/cargo-chef", "https://github.com/GoogleContainerTools/distroless", "https://doc.rust-lang.org/rustc/platform-support.html", "https://docs.docker.com/build/cache/optimize/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rust container images

Rust compiles dependencies from source; without layer tricks every source change rebuilds
the whole dependency tree (minutes).

## cargo-chef (dependency layer caching)
```dockerfile
# syntax=docker/dockerfile:1
FROM rust:1 AS chef
RUN cargo install cargo-chef --locked
WORKDIR /app

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json     # cached until deps change
COPY . .
RUN cargo build --release --bin api

FROM gcr.io/distroless/cc-debian13:nonroot
COPY --from=builder /app/target/release/api /api
ENTRYPOINT ["/api"]
```
The distroless README lists `cc-debian13` (tags `latest`, `nonroot`, `debug`, `debug-nonroot`); the
`cc` variant is the one meant for dynamically linked binaries needing libc (check the README
for each variant's contents). cargo-chef's own README uses `debian:trixie-slim` as the runtime
stage.

## Alternative: cache mounts
```dockerfile
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release && cp target/release/api /api
```
Simpler; the cache lives on the builder (see Docker's cache-mount documentation), whereas
cargo-chef produces ordinary image layers that any layer cache can reuse.

## musl static binaries for scratch
```dockerfile
FROM clux/muslrust:stable AS builder      # cargo-chef README's recommended musl base
WORKDIR /app
COPY . .
RUN cargo build --release --target x86_64-unknown-linux-musl --bin api

FROM scratch
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/api /api
USER 10001
ENTRYPOINT ["/api"]
```
- The cargo-chef README recommends building for `x86_64-unknown-linux-musl` with `muslrust`
  and notes this is cross-compiling, so pass `--target` to **both** `cargo chef cook` and
  `cargo build`. It uses `alpine` as the runtime stage in its example.
- A `scratch` image has no CA certificates or other files; copy in what the program needs.

## Gotchas
- `cargo chef cook` and `cargo build` must run from the same working directory and use the
  same profile, features and target (README), or the cache misses.
- Workspaces: keep `--bin` / `-p` selection consistent between cook and build.
- The README warns cargo-chef is not meant to be run locally (it is for Docker layer caching).

## Verify
Touch a source file and rebuild: the `cook` step should come from cache, because
`recipe.json` only changes when dependency manifests change.

## Checked
Date: 2026-10-26. Documentation: LukeMathWalker/cargo-chef README, GoogleContainerTools/distroless README (tags at debian13), rust-lang platform-support page (musl targets exist). Confirmed: prepare/cook flow and flags, stage layout, musl/muslrust recommendation and `--target` on both commands, same-directory rule, distroless variants and tags. Removed as unconfirmed: `rust:1.82` pins and the Alpine builder (replaced by README examples), `cc-debian12` tag (current is debian13), musl allocator and OpenSSL advice, `strip`/`lto` size claim, `cargo zigbuild` cross-arch advice, "cook step must be CACHED" and image-size expectations.
Method: documentation only; no commands were run.
