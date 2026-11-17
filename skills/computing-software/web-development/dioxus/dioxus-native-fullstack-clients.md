---
id: computing-software.web-development.dioxus.dioxus-native-fullstack-clients
name: dioxus-native-fullstack-clients
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, desktop, mobile, set-server-url, use-action, api-versioning, native-clients]
level: practitioner
status: docs-checked
description: "Call Dioxus server functions from desktop and mobile apps: set_server_url, stable get/post endpoints, backward-compatible API changes, and which fullstack features are disabled."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/native.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use fullstack from native (desktop and mobile) clients

Goal: let a desktop or mobile Dioxus app call your server functions and survive redeploys.

Server functions work the same as on the web, but server-side-rendering does not apply. Enable features and serve with `dx serve --<platform>`:

```toml
[dependencies]
dioxus = { version = "0.7", features = ["fullstack"] }
[features]
server = ["dioxus/server"]
desktop = ["dioxus/desktop"]
```

```sh
dx serve --desktop
```

## Tell the client where the server is

On the web, requests go to the current host origin. Native apps are not served from a URL, so call `set_server_url` before any request:

```rust
fn main() {
    #[cfg(not(feature = "server"))]
    dioxus::fullstack::set_server_url("https://hot-dog.fly.dev");
    dioxus::launch(app);
}
```

A server function can be driven from UI with `use_action(get_message)` and `message.call("world".into(), 30)`.

## Disabled with native fullstack

There is no hydration context or hydration data; the app is never rendered on the server, so `#[cfg(feature = "server")]` code is skipped; there is no `FullstackContext` while rendering components; HTML streaming and SSG have no effect.

## Prefer known endpoints and version them

`#[server]` generates a path with a hash that may change when the signature or body changes (the docs show `/api/do_it12nldkj2378jnakls`). For native clients use `#[get]` / `#[post]` with a fixed path.

Installed clients may be older than your backend, so do not break an endpoint's signature. Either add new arguments as `Option<T>`:

```rust
#[post("/api/do_it")]
async fn do_it(name: Option<String>) -> Result<()> { /* */ }
```

or version the path: `#[post("/api/v1/do_it")]` and `#[post("/api/v2/do_it")]`.

## Deploying

Server apps produce a `server` binary and a `/public/` folder; native apps produce a bundle (`.app`, `.ipa`, `.apk`, etc.). Upload the server to a host; as long as the native app has `server_url` set it can reach the backend.

## Checked
Checked 2026-11-07 against the 0.7 Native Clients page (read in full; code is inline). Confirmed: Cargo features, dx serve --desktop, set_server_url, use_action example, disabled features list, hashed #[server] path, stable #[get] and #[post], Option<T> and versioned paths, deploy artifacts. Nothing removed.
Method: documentation only; no commands were run.
