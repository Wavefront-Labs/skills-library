---
id: computing-software.web-development.leptos.wasm-binary-size
name: wasm-binary-size
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, wasm, binary-size, cargo-leptos, optimization]
level: practitioner
status: docs-checked
description: "Shrink a Leptos WASM bundle with a size-optimized wasm-release profile, compression, nightly build-std, alternate Resource encodings and avoiding heavy crates."
sources: [https://book.leptos.dev/deployment/binary_size.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reduce Leptos WASM binary size

Goal: ship the smallest WASM so the app becomes interactive sooner.

## Steps

1. Make sure you are looking at a release build; debug builds are much, much larger.
2. Add a size-optimized profile (cargo-leptos):

```toml
[profile.wasm-release]
inherits = "release"
opt-level = 'z'
lto = true
codegen-units = 1

[package.metadata.leptos]
lib-profile-release = "wasm-release"
```

This optimizes WASM for size while the server stays optimized for speed. For a pure CSR app use these settings as `[profile.release]`.

3. Serve compressed WASM in production (typically under 50% of original size; easy to enable in Actix or Axum static serving).
4. Nightly only: rebuild std with `.cargo/config.toml`:

```toml
[unstable]
build-std = ["std", "panic_abort", "core", "alloc"]
build-std-features = ["panic_immediate_abort"]
```

With SSR the same profile applies to the server, so set `[build] target = "x86_64-unknown-linux-gnu"` (or yours); if builds fail on `has_std`, add `rustflags = ["--cfg=has_std"]`; add `panic = "abort"` to `[profile.release]`. This also applies to the server binary, which may be undesirable; the page says further exploration is needed.
5. serde code adds size. `leptos_server` features add alternative Resource encodings: `miniserde` gives `Resource::new_miniserde()`, `serde-lite` gives `new_serde_lite`. They implement subsets of serde but favor size.

## Avoid

- `regex` with default features (about 500kb of Unicode tables); consider browser regex APIs (as `leptos_router` does).
- Heavy use of generics: monomorphization copies code per type. Use a concrete inner function in big generic components.

Next step: computing-software.web-development.leptos.wasm-code-splitting. For a smaller baseline, see computing-software.web-development.leptos.islands-setup.

## Checked

2026-11-07: Read in full: deployment/binary_size.md (release build advice, wasm-release profile with opt-level z, lto and codegen-units, compression under 50 percent, nightly build-std with panic_immediate_abort, has_std rustflags, panic abort, miniserde and serde-lite Resource encodings, regex about 500kb, monomorphization). One wording correction: step 1 now matches the page ('make sure you are looking at a release build'). No other claims trimmed. No build was run and no sizes were measured.

Method: documentation only; no commands were run.
