---
id: computing-software.web-development.dioxus.dioxus-deploy-fly-docker
name: dioxus-deploy-fly-docker
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, deploy, fly-io, dockerfile, cargo-chef, set-server-url, server-endpoint, github-actions]
level: advanced
status: docs-checked
description: "Deploy a Dioxus fullstack app to Fly.io: cargo-chef Dockerfile running dx bundle, IP/PORT env, fly launch/deploy, a SQLite volume, set_server_url for native clients."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/tutorial/deploy.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/guide_deploy.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deploy a Dioxus fullstack app (Docker + Fly.io)

A Dioxus web app is a client bundle plus a server executable; any provider that exposes a simple container works. The server runs with `./server` and honours the `IP` and `PORT` environment variables. WASM-container providers (Cloudflare Workers, Fermyon Spin) need a manually created WASM build of your server. Desktop apps are deployed by hosting the bundles (GitHub, S3); app stores need extra steps. Dioxus itself does not offer a deploy platform yet.

## Dockerfile (three phases)
```dockerfile
FROM rust:1 AS chef
RUN cargo install cargo-chef
WORKDIR /app

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json
COPY . .
# Install `dx`
RUN curl -L --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/cargo-bins/cargo-binstall/main/install-from-binstall-release.sh | bash
RUN cargo binstall dioxus-cli --root /.cargo -y --force
ENV PATH="/.cargo/bin:$PATH"
RUN dx bundle --web --release

FROM chef AS runtime
COPY --from=builder /app/target/dx/hot_dog/release/web/ /usr/local/app
ENV PORT=8080
ENV IP=0.0.0.0
EXPOSE 8080
WORKDIR /usr/local/app
ENTRYPOINT [ "/usr/local/app/server" ]
```
Also add a `.dockerignore` (the page lists `**/target`, `**/dist`, `LICENSES`, `LICENSE`, `temp`, `README.md`).

## Fly.io
Sign up, install `flyctl`, put the Dockerfile and .dockerignore in the project, then:
```sh
fly launch    # initializes fly.toml, builds and deploys
fly deploy    # redeploy later
```
Persist SQLite by adding to fly.toml:
```toml
[mounts]
  source = "hotdogdb"
  destination = "/usr/local/app/hotdogdb"
```
Continuous deployment: `.github/workflows/fly-deploy.yml` triggered on push to main, using `superfly/flyctl-actions/setup-flyctl@master`, `flyctl deploy --remote-only` and `FLY_API_TOKEN` from secrets.

## Native clients need the server URL
Dioxus does not know where your API lives, so set it for non-server builds:
```rust
fn main() {
    #[cfg(not(feature = "server"))]
    server_fn::client::set_server_url("https://hot-dog.fly.dev");
    dioxus::launch(App);
}
```
## Gotcha: stable endpoints
`#[server]` generates endpoints like `/api/fetch_dogs-jkhj12`; the trailing hash changes as you edit server functions. Pin them with `#[server(endpoint = "list_dogs")]` so deployed native apps keep working.

## Checked
Checked 2026-11-07 against the 0.7 Deploying tutorial page and the guide_deploy.rs snippet file (both read in full). Confirmed: deploy requirements, three-phase cargo-chef Dockerfile, .dockerignore entries, fly launch and fly deploy, [mounts] block, fly-deploy.yml workflow, set_server_url, stable endpoint attribute. Nothing removed.
Method: documentation only; no commands were run.
