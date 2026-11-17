---
id: computing-software.web-development.dioxus.dioxus-logging-tracing
name: dioxus-logging-tracing
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, logging, tracing, dioxus-logger, launch, logcat, initialize-default, oslog]
level: practitioner
status: docs-checked
description: "Log from Dioxus apps with tracing macros; dioxus::launch sets a default logger, dioxus::logger::init overrides the level, and Android/iOS logs are read from logcat/oslog."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/utilities/logging.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/migration/to_06.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Logging in Dioxus

Goal: emit and view logs across web, desktop and mobile.

## Default logger
`dioxus::launch` sets up a tracing subscriber that integrates with the Dioxus CLI and with Web and Mobile. In dev mode the `Debug` level is set; in release only `Info`.
```rust
use dioxus::prelude::*;

fn main() {
    dioxus::launch(|| {
        // Will only log in "dev" mode
        tracing::debug!("Rendering app!");
        // Will log in dev and release
        tracing::info!("Rendering app!");
        rsx! {}
    })
}
```

## Override the level
Initialize before `launch`:
```rs
use tracing::Level;

fn main() {
    dioxus::logger::init(Level::INFO).expect("failed to init logger");
    dioxus::launch(|| rsx! {})
}
```
The 0.6 migration page also exposes `dioxus::logger::initialize_default();` for extra logging before `launch`. Since 0.6 the `dioxus-logger` crate is part of dioxus itself, so the old `dioxus_logger::init(Level::INFO)` call and Cargo dependency are no longer needed.

## Tracing macros
Lowest to highest severity: `tracing::trace!`, `debug!`, `info!`, `warn!`, `error!`. Using the tracing crate is not required, but without it you will not receive logs from the Dioxus library.

## Platform notes
- Web: tracing-wasm. Desktop and server targets: tracing-subscriber's `FmtSubscriber`.
- Android logs go to logcat: `adb -d logcat` (the device needs developer options / USB debugging enabled).
- iOS logs go to oslog.

## Checked
Checked 2026-11-07 against the 0.7 Logging page and the Logging section of the 0.6 migration page (both read in full). Confirmed: launch logger with Debug in dev and Info in release, dioxus::logger::init, initialize_default, dioxus-logger folded into dioxus, tracing macro order, tracing-wasm and FmtSubscriber, adb -d logcat, oslog. Nothing removed.
Method: documentation only; no commands were run.
