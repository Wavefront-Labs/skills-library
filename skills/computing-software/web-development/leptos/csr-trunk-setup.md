---
id: computing-software.web-development.leptos.csr-trunk-setup
name: csr-trunk-setup
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, trunk, csr, wasm, setup, getting-started, cargo-generate]
level: practitioner
status: docs-checked
description: "Set up a client-side rendered Leptos project with Trunk and the wasm32 target, or scaffold it from the start-trunk template."
sources: [https://book.leptos.dev/getting_started/, https://book.leptos.dev/view/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Set up a Leptos CSR project with Trunk

Goal: get a client-side rendered (CSR) Leptos app compiling to WebAssembly and live-reloading in the browser.

## Method

1. Install Rust (rust-lang.org install page), then install Trunk:
   `cargo install --locked trunk`
2. Create the project: `cargo init leptos-tutorial`, then `cd leptos-tutorial`.
3. Add Leptos with the CSR feature: `cargo add leptos --features=csr`
4. Add the WASM compile target: `rustup target add wasm32-unknown-unknown`
5. Create `index.html` in the project root (same level as `Cargo.toml`):

```html
<!DOCTYPE html>
<html>
  <head></head>
  <body></body>
</html>
```

6. Put this in `src/main.rs`:

```rust
use leptos::prelude::*;

fn main() {
    leptos::mount::mount_to_body(|| view! { <p>"Hello, world!"</p> })
}
```

7. Run `trunk serve --open` from the project root. Trunk compiles the app and opens the browser; edits to `main.rs` trigger a recompile and live reload.

Expected layout: `src/main.rs`, `Cargo.toml`, `index.html`.

## Alternative: start-trunk template

The book offers a fuller template with routing, `<Title>` and `<Meta>` injection into the page head and a few other basics. It needs Trunk and cargo-generate:

```bash
cargo install trunk
cargo install cargo-generate
cargo generate --git https://github.com/leptos-rs/start-trunk
trunk serve --port 3000 --open
```

Run the last command inside the generated app directory. The bare setup above is enough to follow the tutorial.

## Gotchas

- On Windows, `trunk serve --open` may not work. Use `trunk serve` and open the browser tab manually.
- Under the hood an auto-generated JS snippet loads the WASM bundle, so JavaScript must be enabled on the client for a CSR app to display.

## Related

- Choosing CSR vs SSR: `computing-software.web-development.leptos.choose-csr-or-ssr`
- Next step, a real component: `computing-software.web-development.leptos.first-component-and-view`

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/getting_started/, https://book.leptos.dev/view/) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
