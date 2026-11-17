---
id: computing-software.web-development.dioxus.dioxus-websockets
name: dioxus-websockets
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, fullstack, websocket, websocketoptions, use-websocket, on-upgrade, cborencoding, jsonencoding]
level: practitioner
status: docs-checked
description: "Build typed websockets in Dioxus fullstack with WebSocketOptions, Websocket<In, Out, Encoding>, on_upgrade and the use_websocket hook."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/fullstack/websockets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Websockets in Dioxus fullstack

Goal: two-way, typed, ordered messaging between client and server alongside server functions.

Websockets are stateful: a connection ties a client and server together for a session. In a serverless environment with request time limits you need a way to store the session across requests.

## Server

Take `WebSocketOptions` as the body and return `Websocket`:

```rust
#[get("/api/uppercase_ws")]
async fn uppercase_ws(options: WebSocketOptions) -> Result<Websocket> {
    Ok(options.on_upgrade(move |mut socket| async move {
        _ = socket.send("Hello!".to_string()).await;
        while let Ok(msg) = socket.recv().await {
            _ = socket.send(msg.to_ascii_uppercase()).await;
        }
    }))
}
```

`Websocket<In = String, Out = String, E = JsonEncoding>` is generic over input type, output type and encoding. `.send()` and `.recv()` use those types and return an error if deserialization fails. `on_upgrade` wraps Axum's; its future is spawned on a tokio `LocalSet`, so it does not need to be `Send`.

```rust
async fn uppercase_ws(options: WebSocketOptions)
    -> Result<Websocket<ClientEvent, ServerEvent, CborEncoding>> { /* .. */ }
```

Cbor or MsgPack suit Rust-only clients; third-party clients are better served by the default JSON. Path/query parameters and header extraction still work, e.g. `#[get("/api/uppercase_ws?name&age")]` with `name: String, age: i32, options: WebSocketOptions`.

## Client

Call the server function and await it, for example in `use_future`; `.recv()` waits for the connection and deserializes messages. Lower-level APIs such as `send_raw` send raw frames.

For a handle usable across the component use `use_websocket`, which adds signal-based reactivity: `.status()` reads connection state and `.send()` sends.

```rust
let mut socket = use_websocket(|| uppercase_ws("John Doe".into(), 30, WebSocketOptions::new()));

use_future(move || async move {
    while let Ok(msg) = socket.recv().await { messages.push(msg); }
});

rsx! { input { oninput: move |e| async move { _ = socket.send(ClientEvent::TextInput(e.value())).await; } } }
```

If the connection fails, restart it by calling `.set()` on the handle with a new websocket object.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 websockets page (read in full): WebSocketOptions as body and Websocket as return, Websocket<In, Out, E> defaults (String, String, JsonEncoding), on_upgrade spawned on a tokio LocalSet, CborEncoding, path/query parameters, use_future and use_websocket with status() and send(), and restarting with set().

Method: documentation only; no commands were run.
