---
id: computing-software.web-development.leptos.deploy-ssr-app
name: deploy-ssr-app
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, deployment, ssr, docker, container, fly-io, serverless]
level: practitioner
status: docs-checked
description: "Deploy a cargo-leptos SSR app: Debian or Alpine Containerfile, env vars, Caddy reverse proxy, Fly.io launch, and AWS Lambda or Deno and Cloudflare limits."
sources: [https://book.leptos.dev/deployment/ssr.html, https://book.leptos.dev/deployment/index.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy a Leptos full-stack SSR app

Goal: ship a `cargo-leptos` SSR app. General advice: always deploy `--release`, and test locally in release mode too, because the framework applies optimizations only there (a behavioral difference is likely a framework bug worth a GitHub issue).

## Containerfile (Debian)

Builder stage (key lines): base `rustlang/rust:nightly-trixie` (or `rust:<ver>-trixie` for stable), install `cargo-binstall`, `apt-get install clang`, `cargo binstall cargo-leptos -y`, `rustup target add wasm32-unknown-unknown`, `COPY . .`, then:

```
RUN cargo leptos build --release -vv
```

Runtime stage `debian:trixie-slim` with `openssl ca-certificates`; copy three things from the builder, then set env and run:

```
COPY --from=builder /app/target/release/leptos_start /app/
COPY --from=builder /app/target/site /app/site
COPY --from=builder /app/Cargo.toml /app/
ENV RUST_LOG="info"
ENV LEPTOS_SITE_ADDR="0.0.0.0:8080"
ENV LEPTOS_SITE_ROOT="site"
EXPOSE 8080
CMD ["/app/leptos_start"]
```

Replace `leptos_start` with your binary name from Cargo.toml. An Alpine variant uses `rustlang/rust:nightly-alpine`, `apk add bash curl npm libc-dev binaryen`, `npm install -g sass`, and the cargo-leptos installer script from its GitHub releases; same copies and env (`LEPTOS_SITE_ROOT=./site`).

## Reverse proxy

Prefer a proxy (Caddy, Nginx, Traefik, Apache) for TLS, compression and headers. Minimal Caddyfile:

```
example.com {
    reverse_proxy leptos-app:8080
}
```

## Fly.io

Put the Dockerfile in the repo root, install `flyctl`, then `fly auth login` and `fly launch`. Fly auto-stops idle machines; set `min_machines_running` to 1 in `fly.toml` to avoid cold starts. For CI: `fly launch --no-deploy`, commit `fly.toml`, create a Fly access token, store it as the repo secret `FLY_API_TOKEN`, and run `flyctl deploy --remote-only` from a GitHub Actions workflow on pushes to main.

## Serverless

- AWS Lambda: via Cargo Lambda, template `leptos-rs/start-aws` (Axum). Disk writes and state extractors are unreliable across requests; use a database. Mind cold starts.
- Deno / Cloudflare Workers: Leptos-Axum can run in JS-hosted WASM runtimes: `crate-type = ["cdylib"]`, enable the `wasm` feature on `leptos_axum`; all crates must be WASM-compatible.
- Spin and Shuttle.rs: described as in progress or unsupported at the time of writing.

Sub-path hosting: computing-software.web-development.leptos.deploy-non-root-path. Static CSR apps: computing-software.web-development.leptos.deploy-csr-static-hosts.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/deployment/ssr.html, https://book.leptos.dev/deployment/index.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
