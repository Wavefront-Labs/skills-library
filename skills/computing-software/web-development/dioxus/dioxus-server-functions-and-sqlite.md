---
id: computing-software.web-development.dioxus.dioxus-server-functions-and-sqlite
name: dioxus-server-functions-and-sqlite
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, server-function, post, server-feature, dioxus-serve, rusqlite, use-server-future]
level: advanced
status: docs-checked
description: "Add a Dioxus fullstack backend: fullstack/server features, #[post] server functions, server-only code behind cfg(feature), rusqlite storage."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/tutorial/backend.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/tutorial/databases.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/tutorial/routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fullstack: server functions and SQLite

## Enable fullstack
```toml
[dependencies]
dioxus = { version = "0.7.0", features = ["fullstack"] }

[features]
default = []            # remove the default web target
web = ["dioxus/web"]
desktop = ["dioxus/desktop"]
mobile = ["dioxus/mobile"]
server = ["dioxus/server"]
```
dx cannot hot-reload this change; restart the dev server and run `dx serve --web`.

## Server functions
An async function with a macro like `#[post("/api/save_dog")]` returning `Result<()>`; arguments must be serializable. On the client it expands to a reqwest call, on the server to an axum handler. `dioxus::launch` registers them automatically. For a custom axum router use `dioxus::serve`:
```rust
fn main() {
    #[cfg(not(feature = "server"))]
    dioxus::launch(App);

    #[cfg(feature = "server")]
    dioxus::serve(|| async move {
        let router = dioxus::server::router(App);
        // .. customize it however you want ..
        Ok(router)
    })
}
```
Client call: `_ = save_dog(current).await;` inside an async `onclick`.

## Client/server split
Dioxus builds two apps: the client with `--features web`, the server with `--features server`. Anything not gated by the server feature ships to the client, so a top-level `static DB_PASSWORD` would leak. Put server-only code in `#[cfg(feature = "server")] mod server_utils { ... }`. Client-only code (for example `web_sys::window()` before `launch`) panics on the server; gate it on a client feature such as web. Optional server dependencies: `tokio = { version = "1", optional = true }` with `server = ["dep:tokio"]`.

## SQLite with rusqlite
```toml
rusqlite = { version = "0.32.1", optional = true }
server = ["dioxus/server", "dep:rusqlite"]
```
Connections are not thread-safe, so use a thread_local:
```rust
#[cfg(feature = "server")]
thread_local! {
    pub static DB: rusqlite::Connection = {
        let conn = rusqlite::Connection::open("hotdog.db").expect("Failed to open database");
        conn.execute_batch(
            "CREATE TABLE IF NOT EXISTS dogs (id INTEGER PRIMARY KEY, url TEXT NOT NULL);",
        ).unwrap();
        conn
    };
}

#[server]
async fn save_dog(image: String) -> Result<()> {
    DB.with(|f| f.execute("INSERT INTO dogs (url) VALUES (?1)", &[&image]))?;
    Ok(())
}
```
Read with `use_server_future(list_dogs)?`, which waits for the future before rendering and serializes the data from server to client.

## Gotcha
The docs recommend a mainstream relational database such as PostgreSQL or MySQL for most apps, and an embedded one like SQLite for single-instance or per-user data.

## Checked

2026-11-09. Confirmed against the Dioxus 0.7 tutorial pages backend.md, databases.md and routing.md and the guide_backend.rs, guide_databases.rs and guide_router.rs examples: the Cargo.toml feature lines, the dx restart and `dx serve --web` note, server function restrictions and the reqwest and axum expansions, dioxus::launch versus dioxus::serve, the client and server feature split and the leak example, optional dependencies, the rusqlite thread_local code and use_server_future. Nothing removed.

Method: documentation only; no commands were run.
