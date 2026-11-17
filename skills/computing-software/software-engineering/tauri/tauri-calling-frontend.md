---
id: computing-software.software-engineering.tauri.tauri-calling-frontend
name: tauri-calling-frontend
category: computing-software
field: software-engineering
product: tauri
tags: [calling-frontend, tauri]
level: practitioner
status: docs-checked
description: "Send data from Tauri Rust code to the frontend with events, channels or eval, and listen and unlisten correctly in JavaScript and Rust."
sources:
  - "https://v2.tauri.app/develop/calling-frontend/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling the frontend from Rust

Goal: push data from Rust to the webview using events, channels or JavaScript evaluation.

## Events

Meant for small amounts of data or multi producer / multi consumer patterns; not for low latency or high throughput. Events have no strong typing, payloads are JSON strings, and the capabilities system does not control them. `AppHandle` and `WebviewWindow` implement `Emitter` and `Listener`.

- Global (all listeners): `app.emit("download-started", &url).unwrap();`
- One webview: `app.emit_to("login", "login-result", result).unwrap();`
- Several webviews: `app.emit_filter("open-file", path, |target| match target { EventTarget::WebviewWindow { label } => label == "main" || label == "file-viewer", _ => false })`
- Payloads can be any serializable type that is also `Clone`; use `#[derive(Clone, Serialize)]` and `#[serde(rename_all = "camelCase")]`.
- Webview-specific events do not reach regular global listeners; use `listen_any` in Rust to catch all.

## Listening in the frontend

`listen('download-started', (event) => ...)` from `@tauri-apps/api/event` stays registered for the app's lifetime; it returns a Promise resolving to an `unlisten` function. Use `await listen(...)` before calling `unlisten()`. Call `unlisten` when a component unmounts (in React, `unlisten.then((fn) => fn())` in the `useEffect` cleanup; likewise in Vue `onUnmounted` and Svelte `$effect`). Reloading or navigating unregisters listeners automatically, but not in an SPA router. `once('ready', ...)` listens once; `getCurrentWebviewWindow().listen(...)` listens to webview-specific events. Listeners run in registration order, but async listeners can process rapid events out of order.

In Rust, `app.listen("download-started", |event| ...)` (needs `use tauri::Listener`) returns an id; stop with `app.unlisten(id)`; `app.once("ready", ...)` fires once.

## Channels

Fast, ordered, used internally for download progress, child process output and WebSocket messages. A command takes `on_event: tauri::ipc::Channel<DownloadEvent>` and calls `on_event.send(...)`. In JavaScript:

```ts
import { invoke, Channel } from '@tauri-apps/api/core';
const onEvent = new Channel<DownloadEvent>();
onEvent.onmessage = (message) => { console.log(message.event); };
await invoke('download', { url: '...', onEvent });
```

## Evaluating JavaScript

`app.get_webview_window("main").unwrap().eval("console.log('hello from Rust')")?;` For scripts needing Rust input, the page recommends the `serialize-to-javascript` crate.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/develop/calling-frontend/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
