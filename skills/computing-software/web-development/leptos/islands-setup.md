---
id: computing-software.web-development.leptos.islands-setup
name: islands-setup
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, islands, hydration, cargo-leptos, wasm]
level: practitioner
status: docs-checked
description: "Enable Leptos islands mode: add the islands feature, call hydrate_islands, set islands=true on HydrationScripts, and mark interactive components with #[island]."
sources: [https://book.leptos.dev/islands.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Turn on islands mode and make a component interactive

Goal: ship plain server HTML by default and hydrate only small interactive islands (WASM size grows with interactivity, not app size).

## Steps (start from `cargo leptos new --git leptos-rs/start-axum`)

1. In Cargo.toml add the feature on the `leptos` crate only:

```toml
leptos = { version = "0.7", features = ["islands"] }
```

2. In `src/lib.rs` `hydrate`, replace `leptos::mount::hydrate_body(App)` with:

```rust
leptos::mount::hydrate_islands();
```

3. In the `shell` function in `app.rs`:

```rust
<HydrationScripts options islands=true/>
```

4. Run `cargo leptos watch`. Initially clicking does nothing: the app is now inert HTML by default and interactivity is opt-in.
5. Change `#[component]` to `#[island]` on components that need client behavior. `#[island]` otherwise works like `#[component]`.

```rust
#[island]
fn Counter() -> impl IntoView {
    let (count, set_count) = signal(0);
    let on_click = move |_| *set_count.write() += 1;
    view! { <button on:click=on_click>"Click Me: " {count}</button> }
}
```

In the HTML an island renders as `<leptos-island data-component="...">`; only code inside it is compiled to WASM and hydrated.

## Keep islands small

Split a page into a normal `#[component]` (static `<h1>`, other content) and a tiny `#[island]` for the interactive part. Demo release sizes quoted: about 24kb static, 166kb with one island, 274kb non-islands hello world.

## Gotchas

- Keep `use app::*;` in `hydrate()` even though `App` is unused in islands mode: in a workspace, `wasm-bindgen` may not generate bindings correctly if the frontend crate never uses the `app` crate (issue 2083).
- Code in `#[component]` bodies now runs only on the server unless the component is used inside an island (then it is compiled into WASM too).

Next: computing-software.web-development.leptos.islands-server-children-and-context.

## Checked

2026-11-07: every claim, snippet and step above was compared with the full text of the cited Leptos book pages (https://book.leptos.dev/islands.html) and the book source on GitHub. Statements the pages do not state were removed or trimmed.

Method: documentation only; no commands were run.
