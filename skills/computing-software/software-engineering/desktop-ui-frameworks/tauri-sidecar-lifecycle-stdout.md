---
id: computing-software.software-engineering.desktop-ui-frameworks.tauri-sidecar-lifecycle-stdout
name: tauri-sidecar-lifecycle-stdout
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [tauri-sidecar-lifecycle-stdout, tauri-sidecar, tauri, tauri2, sidecar, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Read sidecar stdout through CommandEvent in a spawned task and forward lines to the frontend as events."
sources:
  - https://v2.tauri.app/develop/sidecar/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tauri sidecar output

**Goal:** read what a sidecar prints and forward it.

```rust
use tauri::Emitter;
use tauri_plugin_shell::{process::CommandEvent, ShellExt};

let (mut rx, mut child) = app.shell().sidecar("my-sidecar").unwrap().spawn().expect("Failed to spawn sidecar");
tauri::async_runtime::spawn(async move {
    while let Some(event) = rx.recv().await {
        if let CommandEvent::Stdout(line_bytes) = event {
            let line = String::from_utf8_lossy(&line_bytes);
            app.emit("message", Some(format!("'{}'", line))).expect("failed to emit event");
            child.write("message from Rust\n".as_bytes()).unwrap(); // write to the sidecar stdin
        }
    }
});
```

**Gotcha:** `spawn()` returns the event receiver and the child handle; the receiver must be drained in a task or output is not seen. The docs do not describe lifecycle handling: whether the child is killed when the app closes needs testing on each platform. The shell plugin has a `shell:allow-kill` permission if the frontend kills a child.

## Verify
- Stdout lines from the sidecar arrive as `message` events in the frontend.

## Checked
2026-11-03. Confirmed in the Tauri sidecar page and shell plugin permission table: `spawn()` returning `(rx, child)`, `CommandEvent::Stdout`, `tauri::async_runtime::spawn`, `app.emit`, `child.write`, and the `shell:allow-kill` permission. Removed: the `child.kill()` in a `CloseRequested` handler, the claim that sidecars survive an app crash, and the heartbeat / parent-pid advice (none are stated in the pages read), so the description no longer promises orphan cleanup.
Method: documentation only; no commands were run.
