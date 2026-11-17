---
id: computing-software.web-development.dioxus.dioxus-migrate-0-6-to-0-7
name: dioxus-migrate-0-6-to-0-7
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, migration, dioxus-0-7, dioxus-lib, assetoptions, server-function, form-submission, prevent-default]
level: practitioner
status: docs-checked
description: "Upgrade Dioxus 0.6 apps to 0.7: dioxus-lib removed, forms submit by default, AssetOptions::image(), JSON server function codec, ServerFnError type, prelude removals, axum 0.8."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/migration/to_07.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dioxus 0.6 to 0.7 breaking changes

## dioxus-lib removed
Depend on dioxus directly and replace `dioxus_lib` with `dioxus`:
```toml
[dependencies]
dioxus = { version = "0.7", default-features = false, features = ["lib"] }
```
```rust
use dioxus::prelude::*;
```

## Form submission
Before 0.7, form submissions were prevented by default (and calling `prevent_default` inverted that). In 0.7 forms submit by default; call `prevent_default` to stop it. The desktop renderer separately prevents all page navigation including form submissions.
```rust
form {
    onsubmit: |e| e.prevent_default(),
    input { name: "username", type: "text" },
    button { type: "submit", "Submit" }
}
```

## Asset options
The builder is unified: `AssetOptions::image()` replaces `ImageAssetOptions::new()`.
```rust
pub const RESIZED_PNG_ASSET: Asset =
    asset!("/assets/image.png", AssetOptions::image().with_size(ImageSize::Manual { width: 52, height: 52 }));
pub const AVIF_ASSET: Asset = asset!("/assets/image.png", AssetOptions::image().with_format(ImageFormat::Avif));
```

## Server functions
- `ServerFnError` is now a Dioxus-specific type convertible to `dioxus::Error`; the name is unchanged but imports may need updating.
- The default codec changed from URL-encoded form data to JSON (the old encoding could not represent empty or nested structures). The page says to either update to the JSON codec or explicitly set the protocol to `Http<PostUrl, Json>`; its 0.7 example uses `#[server(protocol = Http<GetUrl, Json>)]` for the former `#[server]` function. Plain `#[server]` now uses JSON. Third-party integrations relying on form encoding must be updated.

## Prelude removals
These now need explicit imports: `use_drop`, `Runtime`, `queue_effect`, `provide_root_context`.

## Dependency bumps
Wry 0.52, Axum 0.8, server_fn 0.7. Custom renderers: html event handlers now accept `SuperInto<ListenerCallback<$data>, __Marker>` instead of `SuperInto<EventHandler<Event<$data>>, __Marker>`.

## Checked
Checked 2026-11-07 against the 0.7 migration page (read in full). Confirmed: dioxus-lib removal, form submission default, AssetOptions::image(), ServerFnError change, JSON codec and Http<PostUrl, Json> protocol, prelude removals, Wry, Axum and server_fn versions, owned listener type for custom renderers. Nothing removed.
Method: documentation only; no commands were run.
