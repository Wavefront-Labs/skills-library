---
id: computing-software.web-development.dioxus.dioxus-migrate-0-5-to-0-6
name: dioxus-migrate-0-5-to-0-6
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, migration, dioxus-0-6, element, prevent-default, asset-macro, launch, document-eval, fullstack]
level: practitioner
status: docs-checked
description: "Upgrade Dioxus 0.5 apps to 0.6: Element is a Result, prevent_default on events, asset! signature, built-in logger, dioxus::launch, document::eval, server feature and fullstack."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/migration/to_06.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/migration.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dioxus 0.5 to 0.6 breaking changes

## Element
`Element` changed from `Option<VNode>` to `Result<VNode, RenderError>`, enabling `?` in components but removing `return None`. Return `VNode::empty()` or an empty `rsx! {}` instead.

## Prevent default
The `prevent_default: "onclick"` attribute is deprecated. Call it inside the handler:
```rust
a { href: "https://dioxuslabs.com", onclick: move |event| event.prevent_default(), "Don't navigate" }
```
In Liveview handlers run on the server, so the method does not prevent default there; use `"onclick": "event.preventDefault()"` (JavaScript string attribute).

## Assets
`asset!` takes the path first and options as an optional second argument; only absolute paths, resolved from the crate root, are accepted:
```rust
img { src: asset!("/assets/static/bundle.png", ImageAssetOptions::new().with_size(ImageSize::Manual { width: 100, height: 100 })) }
```

## Logging, launch, eval
- The logger is built in: `dioxus-logger` no longer needs adding to Cargo.toml, just call `dioxus::launch(app)` (Debug in dev, Info in release). For extra logging before launch use `dioxus::logger::initialize_default();`.
- `launch` was removed from the prelude: write `dioxus::launch(app);`.
- `eval` moved to the document module: `document::eval("console.log(1)")`. `Eval::recv`/`join` now return any `DeserializeOwned`, `send` accepts any `Serialize`.

## Fullstack
- Feature `dioxus/axum` renamed to `dioxus/server`: `server = ["dioxus/server"]`.
- `fullstack::Config` removed; pass platform configs to `LaunchBuilder::new().with_cfg(server_only! {..}).with_cfg(web! {..}).with_cfg(desktop! {..}).launch(app)`.
- With a custom axum server, bind to `dioxus_cli_config::fullstack_address_or_localhost()` because the CLI proxies fullstack apps.
- `serve_dioxus_application` accepts a component; `register_server_fns` is now `register_server_functions`; `ServeConfigBuilder::build` returns a result; `dioxus_fullstack::Config::addr` is removed in favour of the `PORT` and `IP` env vars.

## Router, props, state
- `Routable` no longer accepts fields missing from `route("/route")` when the web feature is on; `ToRouteSegments` takes `&self`.
- `#[props(into)]` is ignored on String props; props starting with an uppercase letter are no longer accepted.
- `use_coroutine` takes `impl FnMut`; `Signal::global_memo` requires `T: PartialEq`; use `resolve` instead of `signal`/`memo` on globals.

Custom renderers must move from `dioxus-hot-reload` to `dioxus_devtools` and implement new trait methods such as `file_size` and `convert_resize_data`.

## Checked
Checked 2026-11-07 against the 0.7 docsite 0.6 migration page and the migration.rs snippet file (both read in full). Confirmed: Element as Result, prevent_default and the Liveview note, asset! signature, launch and eval changes, fullstack feature and config changes, router, props and state notes, custom renderer notes. Reworded: the logger line, which said to remove the dioxus-logger dependency; the page only shows it no longer being needed.
Method: documentation only; no commands were run.
