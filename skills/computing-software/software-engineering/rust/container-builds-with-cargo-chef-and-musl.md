---
id: computing-software.software-engineering.rust.container-builds-with-cargo-chef-and-musl
name: container-builds-with-cargo-chef-and-musl
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-release-ci, rust-docker-builds, docker, cargo-chef, musl, distroless, build-cache]
level: practitioner
status: docs-checked
description: "Build small Rust container images with cargo-chef dependency layer caching, musl static builds for Alpine and a non-root runtime user."
sources:
  - https://github.com/LukeMathWalker/cargo-chef
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Container builds with cargo-chef and musl

**Goal:** fast rebuilds (dependencies cached) and a small runtime image without the Rust toolchain.

cargo-chef has two commands. `cargo chef prepare --recipe-path recipe.json` analyses the project and writes a recipe (the skeleton: all `Cargo.toml` files and `Cargo.lock`, with libraries and binaries declared explicitly). `cargo chef cook --release --recipe-path recipe.json` re-hydrates that skeleton and builds it to cache dependencies. It is not meant to be run locally: run it before the real source is copied, so no files are overwritten.

```dockerfile
FROM lukemathwalker/cargo-chef:latest-rust-1 AS chef
WORKDIR /app

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
# Build dependencies - this is the caching Docker layer
RUN cargo chef cook --release --recipe-path recipe.json
COPY . .
RUN cargo build --release --bin app

# The Rust toolchain is not needed to run the binary
FROM debian:trixie-slim AS runtime
WORKDIR /app
COPY --from=builder /app/target/release/app /usr/local/bin
ENTRYPOINT ["/usr/local/bin/app"]
```

As long as dependencies do not change, `recipe.json` stays the same, so the `cook` layer is cached. Without the pre-built image, install the CLI in the first stage with `cargo install --locked cargo-chef`. Pre-built image tags follow `<cargo-chef version>-rust-<alias>` and `latest-rust-<alias>`, with aliases taken from the official Rust images. Override the toolchain with `cargo +nightly chef cook --recipe-path recipe.json`.

Alpine needs a fully static binary: build for `x86_64-unknown-linux-musl` (the README recommends the `clux/muslrust` image as the base). This is cross-compiling, so pass the target explicitly to both `cook` and `build`:

```dockerfile
FROM clux/muslrust:stable AS chef
USER root
RUN cargo install --locked cargo-chef
WORKDIR /app
# planner stage as above
FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --target x86_64-unknown-linux-musl --recipe-path recipe.json
COPY . .
RUN cargo build --release --target x86_64-unknown-linux-musl --bin app

FROM alpine AS runtime
RUN addgroup -S myuser && adduser -S myuser -G myuser
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /usr/local/bin/
USER myuser
CMD ["/usr/local/bin/app"]
```

## Gotchas
- Use the same Rust version in every stage, or caching does not work as expected.
- `cargo chef cook` and `cargo build` must run from the same working directory (the `*.d` files hold absolute paths).
- `cargo build` rebuilds local dependencies outside the project from scratch even if unchanged (timestamp-based fingerprinting).
- Copying the full source before `cook` defeats the cached layer; copy only the recipe first.

## Verify
Rebuild after touching only application source: the `cook` step should be reported as cached.

## Checked
2026-11-08. Read in full: cargo-chef README (LukeMathWalker/cargo-chef, raw README). Confirmed: prepare and cook, recipe contents, Dockerfile stages, pre-built image tags, nightly override, musl and Alpine Dockerfile, limitations. Removed (not in the README): rust:1.85-bookworm and distroless bases, BuildKit cache mounts (Docker caching page not read), musl allocator and OpenSSL caveats, security checklist, target-cpu=native and image size claims, `--locked` on build.
Method: documentation only; no commands were run.
