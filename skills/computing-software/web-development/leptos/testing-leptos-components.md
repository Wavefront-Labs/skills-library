---
id: computing-software.web-development.leptos.testing-leptos-components
name: testing-leptos-components
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, testing, wasm-bindgen-test, e2e, playwright]
level: practitioner
status: docs-checked
description: "Test a Leptos app by extracting logic into plain Rust tests and covering components with wasm-bindgen-test, Playwright or Cucumber end-to-end tests."
sources: [https://book.leptos.dev/testing.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: choose and set up tests for Leptos code.

## 1. Plain Rust tests for logic

Pull logic out of components into testable types with ordinary `impl` blocks:

```rust
pub struct Todos(Vec<Todo>);
impl Todos {
    pub fn num_remaining(&self) -> usize {
        self.0.iter().filter(|todo| !todo.completed).sum()
    }
}
// in the component:
let num_remaining = move || todos.read().num_remaining();
```

Then add `#[cfg(test)] mod tests` with `#[test]` functions. The less logic lives in components, the easier they are to test.

## 2. End-to-end tests

The Leptos `examples` directory has working setups:

- `wasm-bindgen-test` with the `counter` example, run through `wasm-pack test`. The test mounts the component into a new `<section>` with `mount_to(...)`, clicks a button, then `tick().await` because DOM updates are not synchronous, and compares `outer_html()` or `inner_html()` against a freshly built or freshly mounted expectation (for example `<SimpleCounter initial_value=0 step=1/>`).
- Playwright with `counters` (examples/counters/e2e): tests written in JavaScript using a `CountersPage` helper, such as `await expect(ui.total).toHaveText("3")`.
- Gherkin/Cucumber with `todo_app_sqlite` (examples/todo_app_sqlite/e2e): feature files in natural language, with step definitions in Rust using `#[given]`, `#[when]` and a `world.client`.

## Gotchas

- Any testing tool can be plugged in. The page says to look at the CI setup in the Leptos repository for how these tools run against the example apps.
- The page does not give the exact commands beyond naming `wasm-pack test`.

## Gaps

No flags, browser selection or Cargo setup are stated on the page.

## Checked

2026-11-07: Read in full: testing.md (Todos impl with num_remaining, cfg(test) mod tests, the wasm-bindgen-test counter example run through wasm-pack test with mount_to, tick().await, outer_html and inner_html, the Playwright counters example, the Cucumber todo_app_sqlite example, and the CI note). Two corrections: removed the unsourced instruction to keep the mount_to return value (_dispose) alive, since the page only shows `let _dispose = mount_to(...)`; reworded the Playwright bullet to the page's CountersPage helper wording. The example directories in the Leptos repo were not opened.

Method: documentation only; no commands were run.
