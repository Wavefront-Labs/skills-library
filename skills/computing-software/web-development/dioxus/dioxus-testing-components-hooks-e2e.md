---
id: computing-software.web-development.dioxus.dioxus-testing-components-hooks-e2e
name: dioxus-testing-components-hooks-e2e
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, testing, dioxus-ssr, pretty-assertions, virtualdom, playwright, cargo-test, debugging]
level: practitioner
status: docs-checked
description: "Test Dioxus apps: cargo test units, rsx comparison with dioxus-ssr and pretty_assertions, VirtualDom hook tests, Playwright e2e with dx serve."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/testing/index.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/testing/web.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/testing/debugging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Testing Dioxus apps

Goal: pick the right test layer.

## Unit tests

Plain Rust: mark functions with `#[test]` and run `cargo test`.

## Component tests

Render two RSX snippets with `dioxus-ssr` and compare the strings with `pretty-assertions`:

```rust
#[test]
fn test() {
    assert_rsx_eq(
        rsx! { div { "Hello world" } div { "Hello world" } },
        rsx! { for _ in 0..2 { div { "Hello world" } } },
    )
}

fn assert_rsx_eq(first: Element, second: Element) {
    let first = dioxus_ssr::render_element(first);
    let second = dioxus_ssr::render_element(second);
    pretty_assertions::assert_str_eq!(first, second);
}
```

## Hook tests

There is no full hook-testing library yet. Build a bespoke harness by driving the virtual dom manually. The docs example creates `VirtualDom::new_with_props(mock_app, ...)`, calls `vdom.rebuild_in_place()`, then loops `while vdom.wait_for_work().now_or_never().is_some() { vdom.render_immediate(&mut NoOpMutations); }`. A `MockProxy` reads `dioxus::core::generation()` and schedules reruns with `dioxus::core::schedule_update()`, so each render's `generation` lets the test assert hook values step by step (for example setting a `use_signal(|| 0)` to 1, then 2).

## End to end

Use Playwright. In `playwright.config.js` run `dx serve` (or cargo run) as the web server instead of the default build command:

```js
webServer: [
    {
        cwd: path.join(process.cwd(), 'playwright-tests', 'web'),
        command: 'dx serve',
        port: 8080,
        timeout: 10 * 60 * 1000,
        reuseExistingServer: !process.env.CI,
        stdout: "pipe",
    },
],
```

Example projects exist for web, liveview and fullstack under packages/playwright-tests in the dioxus repo.

## Debugging wasm

Debugging WebAssembly needs a Chrome extension that understands the DWARF debugging format.

## Checked

2026-11-09. Confirmed against the Dioxus 0.7 testing guides (index, web, debugging) and the component_test.rs and hook_test.rs examples: cargo test and #[test], the dioxus-ssr plus pretty-assertions comparison, the absence of a full hook testing library, the VirtualDom harness steps and MockProxy, the Playwright webServer snippet, the three example projects, and the DWARF extension requirement. Nothing removed.

Method: documentation only; no commands were run.
