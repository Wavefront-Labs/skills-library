---
id: computing-software.web-development.leptos.ssr-hydration-bugs-and-fixes
name: ssr-hydration-bugs-and-fixes
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, ssr, hydration, debugging, effect, cfg]
level: practitioner
status: docs-checked
description: "Diagnose Leptos hydration errors from invalid HTML, table without tbody, and server or client-only code, and fix them with Effect, cfg and optional deps."
sources: [https://book.leptos.dev/ssr/24_hydration_bugs.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find and fix bugs that appear only when SSR output is hydrated.

## Mental model
The app runs on the server (also once at startup to extract the route tree) and again in the browser. A `logging::log!` in `<App/>` therefore prints in both places.

## Mismatched server and client output
Using `cfg!(target_arch = "wasm32")` to produce different views on each side leaves the browser looking for elements the HTML lacks; the page shows a panic in tachys (`called Option::unwrap() on a None value`). Run the same logic on both sides. If you did not cause it, the page suggests a `<Suspense/>` bug and filing a GitHub issue.

## HTML vs DOM mismatches
Hydration (0.7+) walks the DOM directly, so the browser-parsed DOM must equal the view tree.
- Invalid HTML: a `<div>` inside a `<p>` makes the browser close the `<p>`, producing `<p></p><div>..</div><p></p>`; the error reads "A hydration error occurred ... expected a text node". Fix the markup; run output through the W3C validator.
- `<table>` without `<tbody>`: browsers insert `<tbody>`. Add `<tbody>` yourself.
- Debugging: right-click the element named in the message to see where it was first noticed, then compare that DOM and above against your view for extra or missing elements.

## Client-only code on the server
A browser crate such as `gloo-net` panics with `cannot call wasm-bindgen imported functions on non-wasm targets`. Options: (1) use crates working on both sides (`reqwest`); (2) gate separate libraries with `#[cfg]`; (3) wrap browser-only code in `Effect::new`, which runs only on the client:

```rust
Effect::new(move |_| {
    let storage = gloo_storage::LocalStorage::raw();
    log!("{storage:?}");
});
```

## Server-only code on the client
Errors about the crate `mio` or missing things from `core` are generally a sign that something that cannot be compiled to WASM is being compiled to WASM. Mark server-only dependencies `optional = true` and enable them in the `ssr` feature (see template `Cargo.toml`). Server-only logic belongs in server functions.

Lifecycle background: `computing-software.web-development.leptos.ssr-page-load-lifecycle`.

## Checked

2026-11-07: Read in full: ssr/24_hydration_bugs.md (thought experiment, mismatch example with cfg!(target_arch = "wasm32"), invalid HTML div in p, table without tbody, General Advice, gloo-net panic and the three solutions, mio and optional = true). Confirmed the tachys unwrap-on-None panic text, the 0.7 hydration change, the Effect::new localStorage example and the reqwest suggestion. One softening: the mio and core errors are 'generally a sign' on the page, not a certainty. Not opened: the hackernews example linked for #[cfg] gating.

Method: documentation only; no commands were run.
