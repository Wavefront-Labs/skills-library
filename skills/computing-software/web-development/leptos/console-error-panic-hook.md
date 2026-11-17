---
id: computing-software.web-development.leptos.console-error-panic-hook
name: console-error-panic-hook
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, console-error-panic-hook, debugging, wasm, panic, developer-experience]
level: practitioner
status: docs-checked
description: "Enable readable Rust panic messages in the browser console for a Leptos WASM app using console_error_panic_hook."
sources: [https://book.leptos.dev/getting_started/leptos_dx.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Get readable panics in the browser with console_error_panic_hook

Goal: replace the unhelpful browser error for a WASM panic with a real Rust message pointing at your source line.

By default a panic in WASM running in the browser throws a message like `Unreachable executed` with a stack trace into the WASM binary. With `console_error_panic_hook` you get a Rust stack trace including a line in your Rust source.

## Method

1. In the project run `cargo add console_error_panic_hook`.
2. In `main`, call `console_error_panic_hook::set_once();`:

```rust
use leptos::prelude::*;

fn main() {
    console_error_panic_hook::set_once();
    leptos::mount::mount_to_body(App);
}
```

The page says to add the call in your main function; the placement before mounting is only this skill's example. With it in place the book says you should get much better panic messages in the browser console.

The book links the counter example in the Leptos repo (examples/counter/src/main.rs) for a worked `main`.

## Related

- Project setup: `computing-software.web-development.leptos.csr-trunk-setup`
- Other DX tweaks: `computing-software.web-development.leptos.rust-analyzer-config`, `computing-software.web-development.leptos.erase-components-compile-speed`

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/getting_started/leptos_dx.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
