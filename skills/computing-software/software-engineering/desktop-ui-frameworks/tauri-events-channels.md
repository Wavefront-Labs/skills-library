---
id: computing-software.software-engineering.desktop-ui-frameworks.tauri-events-channels
name: tauri-events-channels
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [tauri-events-channels, tauri-commands, tauri, tauri2, rust, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Stream ordered data to the frontend with a Channel passed to a command, and send lifecycle notices with events."
sources:
  - https://v2.tauri.app/develop/calling-frontend/
  - https://v2.tauri.app/concept/inter-process-communication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tauri events and channels

**Goal:** progress and streaming.

```rust
use tauri::{ipc::Channel, AppHandle, Emitter};
#[tauri::command]
fn download(url: String, on_chunk: Channel<u64>, app: AppHandle) {
    for n in 0..10 { on_chunk.send(n * 10).unwrap(); }
    app.emit("done", url).unwrap();
}
// JS: import { invoke, Channel } from '@tauri-apps/api/core'; import { listen } from '@tauri-apps/api/event';
//     const ch = new Channel(); ch.onmessage = (p) => ...;
//     await invoke('download', { url, onChunk: ch });
//     const unlisten = await listen('done', (e) => ...);
```

**Gotcha:** the event system is not designed for low latency or high throughput; payloads are JSON, there is no strong typing and no capability control over event data. Async listeners can process rapid events out of order. Use a `Channel` for ordered, fast streams. `listen` returns a Promise of the unlisten handle: await it, and call `unlisten()` when a component unmounts.

## Verify
- The progress callback receives ordered values.

## Checked
2026-11-03. Confirmed in the Tauri Calling the Frontend and IPC pages: `Emitter::emit`, `tauri::ipc::Channel` with `send`, the JS `Channel` with `onmessage` passed as a command argument, `listen` from `@tauri-apps/api/event` returning an unlisten promise, events being fire-and-forget JSON, the throughput and ordering caveats, and channels being fast and ordered. The camelCase mapping of `on_chunk` to `onChunk` follows the Calling Rust page. Removed: the claim that events are for "fire-and-forget JSON" as the only reason to prefer channels, replaced by the documented caveats.
Method: documentation only; no commands were run.
