---
id: computing-software.web-development.dioxus.dioxus-assets-and-stylesheet
name: dioxus-assets-and-stylesheet
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, asset-macro, assetoptions, document-stylesheet, css, avif, content-hash, hot-reload]
level: practitioner
status: docs-checked
description: "Include CSS and images in a Dioxus app with the asset! macro and document::Stylesheet; static vs URL images, content-hashed names and AssetOptions::image().with_avif()."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/tutorial/assets.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/migration/to_07.md
  - https://github.com/DioxusLabs/docsite/blob/main/packages/docs-router/src/doc_examples/guide_assets.rs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Styling and assets with asset!()

Goal: ship CSS and images with the app bundle and load them.

## CSS
Dioxus styles with HTML and CSS. The bare-bones template already includes a base `main.css` in the `assets` folder.
```rust
static CSS: Asset = asset!("/assets/main.css");

fn App() -> Element {
    rsx! {
        document::Stylesheet { href: CSS }
    }
}
```
`document::Stylesheet` is equivalent to the `<link>` element but also ensures the CSS is pre-loaded during server-side rendering. Unlike `include_str!()`, `asset!()` does not embed the file contents in the executable; it generates a unique path so the asset loads at runtime (assets load in parallel HTTP requests on web). The generated name will not exactly match the input, which prevents collisions and improves caching.

All assets take part in hot-reloading: edit `main.css` while `dx serve` runs and changes propagate live.

## Images
Two ways: dynamically via URL, or statically with `asset!()`. URL images do not download when the app is offline.
```rust
rsx! { img { src: "https://images.dog.ceo/breeds/pitbull/dog-3981540_1280.jpg" } }

static ICON: Asset = asset!("/assets/icon.png");
rsx! { img { src: ICON } }
```

## Optimization
By default `asset!()` lightly optimizes CSS, JavaScript, JSON and images, and adds a content hash to the name:
```rust
// would output main-j1238nask123.css
asset!("/assets/main.css").to_string();
// outputs icon-j1238jd2.avif
asset!("/assets/icon.png", AssetOptions::image().with_avif());
```
The docs say asset optimization is for many apps the most effective way to improve load times (oversized images are easy to overlook).

## Related 0.7 change
Asset options were unified: write `AssetOptions::image()` where 0.6 used `ImageAssetOptions::new()`, for example `.with_size(ImageSize::Manual { width: 52, height: 52 })` or `.with_format(ImageFormat::Avif)`.

## Checked
Checked 2026-11-07 against the 0.7 Styling and Assets tutorial page, the guide_assets.rs snippet file and the 0.7 migration page (all read in full). Confirmed: asset! and document::Stylesheet behaviour, URL vs static images, content hash, AssetOptions::image().with_avif(), and the 0.6 to 0.7 AssetOptions change. Removed: the unsupported claim that assets may sit in any folder (the page says the template ships main.css in assets).
Method: documentation only; no commands were run.
