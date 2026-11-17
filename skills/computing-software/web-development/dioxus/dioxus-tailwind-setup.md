---
id: computing-software.web-development.dioxus.dioxus-tailwind-setup
name: dioxus-tailwind-setup
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, tailwind, tailwind-css, tailwind-input, tailwind-output, dx-serve, theme, vscode]
level: practitioner
status: docs-checked
description: "Use Tailwind CSS in Dioxus 0.7: root tailwind.css, auto-started watcher, generated assets/tailwind.css, @theme tokens, VSCode regex settings."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/styling.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/hotreload.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tailwind with Dioxus

Goal: get Tailwind classes compiled and hot-reloaded in a Dioxus app.

## How it is wired

As of Dioxus 0.7, `dx` downloads and starts the Tailwind CLI watcher for you when you build or `serve`. It detects Tailwind by finding a file named `tailwind.css` at the project root, then collects classes and writes `assets/tailwind.css`.

## Steps

1. Create `tailwind.css` in the project root:

```css
@import "tailwindcss";
@source "./src/**/*.{rs,html,css}";
```

The `@source` line makes the watcher scan Rust files.

2. Add the generated stylesheet to your app:

```rust
fn app() -> Element {
    rsx! {
        document::Stylesheet { href: asset!("/assets/tailwind.css") }
    }
}
```

3. Use classes in RSX. Multiple `class` attributes work with Tailwind:

```rust
div {
    class: "bg-white rounded-lg shadow-md p-6 m-4",
    class: if is_hovered() { "shadow-xl transform -translate-y-1" },
    class: "transition-all duration-200",
}
```

## Customising

- Theme variables go in `tailwind.css`, for example:

```css
@theme {
    --color-dxblue: #00A8D6;
    --font-sans: "Inter var", sans-serif;
}
```

- Change input and output locations with the `tailwind_input` and `tailwind_output` fields in `Dioxus.toml`.
- VSCode IntelliSense: install the Tailwind CSS IntelliSense extension and set

```json
{
    "tailwindCSS.experimental.classRegex": ["class: \"(.*)\""],
    "tailwindCSS.includeLanguages": { "rust": "html" }
}
```

## Checked

2026-11-09. Confirmed against the Dioxus 0.7 pages styling.md and hotreload.md: automatic Tailwind watcher start, detection of tailwind.css at the project root, the @import and @source lines, the generated assets/tailwind.css and the Stylesheet snippet, @theme variables, multiple class attributes, tailwind_input and tailwind_output in Dioxus.toml, and the VSCode settings. Removed the formatted-string gotcha, which neither page states.

Method: documentation only; no commands were run.
