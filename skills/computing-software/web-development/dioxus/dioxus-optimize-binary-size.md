---
id: computing-software.web-development.dioxus.dioxus-optimize-binary-size
name: dioxus-optimize-binary-size
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, optimization, binary-size, dx-build, release, wasm-opt, upx, opt-level, lto]
level: practitioner
status: docs-checked
description: "Shrink Dioxus builds: dx build --release, the stable and unstable Cargo release profile settings, wasm-opt -Oz, UPX for non-web targets, and keeping RSX mostly static."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/tips/optimizing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Optimizing Dioxus builds

Goal: cut WASM or executable size (written mainly for web, mostly applies elsewhere). The page's sample TodoMVC app starts at 2.36mb in release mode; 32mb in debug.

## 1. Release mode

```sh
dx build --release
```

Faster and smaller.

## 2. Cargo profile

Settings in `.cargo/config.toml` override `Cargo.toml`. Stable (2.36mb to 310kb):

```toml
[profile.release]
opt-level = "z"
debug = false
lto = true
codegen-units = 1
panic = "abort"
incremental = false
```

Unstable, nightly (310kb to 234kb) adds:

```toml
[unstable]
build-std = ["std", "panic_abort", "core", "alloc"]
build-std-features = ["panic_immediate_abort"]

[build]
rustflags = ["-Clto", "-Zvirtual-function-elimination", "-Zlocation-detail=none"]
```

(plus `strip = true` in the profile). The missing space in each flag, such as `-Clto`, is intentional.

## 3. wasm-opt

From binaryen. Install a release, then from the package directory:

```
wasm-opt dist/assets/dioxus/APP_NAME_bg.wasm -o dist/assets/dioxus/APP_NAME_bg.wasm -Oz
```

`-Oz` optimizes for size; use `-O4` for speed. The page notes `wasm-opt` is to be supported natively by the CLI in future.

## 4. UPX (not for web)

Download UPX, add it to PATH, then e.g. `upx --best -o target/release/compressed.exe target/release/your-executable.exe`.

## 5. Code and assets

Minimise dynamic parts of `rsx` (such as conditional rendering): unchanged parts are skipped on rerender. Assets included with `asset!` are optimized in release builds (alpha support).

## Gotcha

Some optimizations trade speed for size, or the reverse; pick based on whether your app does heavy graphics or DOM work.

## Checked
Checked 2026-11-07 against the 0.7 Optimizing page (read in full). Confirmed: 2.36mb, 32mb, 310kb and 234kb figures, dx build --release, stable and unstable profile settings, strip in the unstable profile, wasm-opt -Oz and -O4, UPX command, rsx dynamic parts advice, alpha asset optimization. Nothing removed.
Method: documentation only; no commands were run.
