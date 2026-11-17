---
id: computing-software.web-development.leptos.styling-leptos-apps
name: styling-leptos-apps
category: computing-software
field: web-development
product: leptos
tags: [leptos, rust, styling, css, tailwind, trunk, cargo-leptos]
level: practitioner
status: docs-checked
description: "Choose a styling approach for Leptos: plain CSS via Trunk or cargo-leptos, Tailwind, Stylers, Stylance or Styled, as the framework has no CSS opinion."
sources: [https://book.leptos.dev/interlude_styling.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick and wire up CSS for a Leptos app.

Leptos itself has no opinion on CSS; it provides primitives that styling libraries build on.

## Plain CSS
- CSR with Trunk: declare the file in `index.html`'s `<head>`: `<link data-trunk rel="css" href="./style.css"/>`. Trunk bundles it as an asset.
- SSR with `cargo-leptos`: templates are configured to bundle SASS and output `/pkg/{project_name}.css`. Add more CSS by importing it into `style.scss`, or put files in the `public` directory (`public/foo.css` is served at `/foo.css`). Load stylesheets in a component with `leptos_meta`'s `Stylesheet` component.

## Tailwind
Write utility classes straight in `view!` (`class="bg-sky-600 hover:bg-sky-700 px-5 py-3 text-white rounded-lg"`). Tailwind's CLI scans your Rust files for class names and compiles CSS. Setup is fiddly; the repo has `examples/tailwind_csr` (Trunk) and `examples/tailwind_actix` (cargo-leptos). `cargo-leptos` also has built-in Tailwind support as an alternative to the CLI.

## Scoped CSS libraries
- Stylers: compile-time scoped CSS declared in the component body with `style!`, extracted into CSS files at compile time, so no WASM size cost; use `view! { class = styler_class, ... }`.
- Stylance: CSS lives in `.css`/`.scss` files beside components, imported with `import_style!(style, "app.module.scss")` and used as `class=style::jumbotron`. Edits to CSS do not trigger a Rust recompile and work with live reload.
- Styled: runtime scoped CSS; declare `style!(...)` then use `styled::view! { styles, ... }`.

## Gaps
The page gives no version or install steps for the third-party crates; check their READMEs.

## Checked

2026-11-07: Read in full: interlude_styling.md (Trunk link tags, SASS output at /pkg/{project_name}.css, public directory, Stylesheet component, the Tailwind examples, and the Stylers, Stylance and Styled mentions). Every statement matches. No claims were trimmed. Linked crates were not opened.

Method: documentation only; no commands were run.
