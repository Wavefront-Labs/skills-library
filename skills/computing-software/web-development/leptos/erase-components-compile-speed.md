---
id: computing-software.web-development.leptos.erase-components-compile-speed
name: erase-components-compile-speed
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, erase-components, compile-time, rustflags, cargo-leptos, trunk, performance]
level: practitioner
status: docs-checked
description: "Speed up Leptos 0.7 development builds by passing --cfg erase_components via RUSTFLAGS or .cargo/config.toml."
sources: [https://book.leptos.dev/getting_started/leptos_dx.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Faster dev compiles with --cfg=erase_components

Goal: cut compile times on larger Leptos projects during development.

Leptos 0.7 relies more heavily on the type system in the renderer, which can slow compiles on bigger projects. The custom flag `--cfg=erase_components` erases some type information, reducing compiler work and emitted debug info. The trade-off is a larger binary and some runtime cost, so do not use it in release mode.

## Method

- With cargo-leptos v0.2.40 or newer it is enabled automatically in development mode.
- If you use Trunk without cargo-leptos, or want it for non-dev uses, set it on the command line:

```bash
RUSTFLAGS="--cfg erase_components" trunk serve
RUSTFLAGS="--cfg erase_components" cargo leptos watch
```

- Or set it permanently in `.cargo/config.toml`:

```toml
# use your own native target
[target.aarch64-apple-darwin]
rustflags = [
  "--cfg",
  "erase_components",
]

[target.wasm32-unknown-unknown]
rustflags = [
   "--cfg",
   "erase_components",
]
```

Replace the first target with your own native target triple (the book's example uses aarch64-apple-darwin).

## Gotchas

- Best not to leave it on for release builds (bigger binary, runtime cost).

## Related

- `computing-software.web-development.leptos.csr-trunk-setup`

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/getting_started/leptos_dx.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
