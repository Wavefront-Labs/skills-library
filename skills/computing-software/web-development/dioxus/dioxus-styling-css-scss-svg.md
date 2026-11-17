---
id: computing-software.web-development.dioxus.dioxus-styling-css-scss-svg
name: dioxus-styling-css-scss-svg
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, styling, css, scss, asset-macro, document-stylesheet, svg, dangerous-inner-html, custom-properties]
level: practitioner
status: docs-checked
description: "Style a Dioxus app with inline style, snake_case CSS attributes, document::Stylesheet, asset!, repeated class, SCSS, CSS variables and inline SVG."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/styling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Styling with CSS, SCSS and SVG

Goal: apply standard HTML/CSS styling in Dioxus.

## Inline

Use the `style` string, or give each CSS property as its own attribute in snake_case; values can be dynamic Rust expressions:

```rust
div {
    background_color: if is_dark() { "black" } else { "white" },
    color: if is_dark() { "white" } else { "black" },
    padding: "20px",
    onclick: move |_| is_dark.toggle(),
    "Click to toggle theme"
}
```

## Stylesheets

Put CSS in your assets directory and include it with `asset!()`:

```rust
static MAIN_CSS: Asset = asset!("/assets/main.css");

fn App() -> Element {
    rsx! {
        document::Stylesheet { href: MAIN_CSS }
        div { class: "my-component", "Hello, styled world!" }
    }
}
```

`document::Link` and `document::Stylesheet` are the two document elements. A plain `link { href: asset!("/assets/main.css") }` also works but is not marked pre-loadable with server-side rendering.

## Conditional classes

`class` can be repeated: `class: "btn", class: if is_active() { "btn-active" }, class: if is_large() { "btn-large" }`.

## Theming and SCSS

CSS custom properties (`:root { --color-primary: #3b82f6; }` used via `var(--color-primary)`) are preferred over Rust variables, since dynamic string formatting is less efficient and harder to optimize. SCSS works out of the box: `static STYLES: Asset = asset!("/assets/styles.scss");`.

## Icons and SVG

Inline SVG goes directly in RSX (`svg { width: "16", height: "16", viewBox: "0 0 24 24", fill: "currentColor", path { d: "..." } }`). Larger files: `img { src: asset!("/assets/logo.svg"), alt: "Logo" }`. Crates: dioxus-free-icons, dioxus-material-icons, dioxus-heroicons. Raw markup: `svg { dangerous_inner_html: r#"<path d="M256 352 128 160h256z" />"# }`.

## Gotcha

Dioxus converts CSS to native widget properties when applicable, but the docs note that some cases need platform-specific code to get the intended look.

## Checked

2026-11-08. Confirmed against the Dioxus 0.7 styling page (read in full): inline style and snake_case attributes, asset! with document::Stylesheet, plain link caveat for SSR preloading, repeated class, CSS custom properties, SCSS via asset!, inline SVG, SVG assets, icon crates, and dangerous_inner_html. Reworded the final gotcha to what the page states.

Method: documentation only; no commands were run.
