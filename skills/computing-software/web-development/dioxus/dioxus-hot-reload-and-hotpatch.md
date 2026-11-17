---
id: computing-software.web-development.dioxus.dioxus-hot-reload-and-hotpatch
name: dioxus-hot-reload-and-hotpatch
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, hot-reload, hotpatch, subsecond, dx-serve, rsx-hot-reload, asset-hot-reload, scss]
level: practitioner
status: docs-checked
description: "What Dioxus 0.7 hot-reloads (RSX, assets, CSS/SCSS), what forces a rebuild, and how to enable experimental Rust hot-patching with dx serve --hotpatch."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/essentials/ui/hotreload.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hot-reloading in Dioxus 0.7

Goal: know which edits apply instantly and when to use hot-patching.

Three kinds exist: element (RSX), asset, and experimental Rust hot-patching.

## RSX hot-reload

Works without recompiling: adding, removing or modifying elements in an `rsx!` block, all string-based attributes, moving existing expressions between formatted strings (`"Count: {count}"` to `"Increment ({count})"`), and literal props on components (a single token such as `enabled: true`, `count: 123`, `text: "Click me"`). It also works inside conditional blocks, loops and component children, but only for markup and elements, not interior expressions.

## Needs a rebuild (or a hot-patch)

- new variables or expressions not in the last compilation
- logic changes outside RSX (function bodies, hooks)
- component signatures (adding or removing props)
- import statements and module structure
- complex attribute expressions involving function calls

## Rust hot-patching (Subsecond)

```bash
dx serve --hotpatch
```

The flag is required while the feature is experimental. With it, `dx` patches the app's assembly in place and rarely needs a full rebuild; press `r` in the `dx` TUI to force one.

Limits:
- new globals can be added but their destructors never run
- renaming a global is seen as a new global
- changes to static initializers are not observed
- only the "tip" crate is tracked; edits in dependencies (even workspace crates) are not registered, although RSX hot-reload does work across a workspace

## Assets

CSS is watched and applied instantly when included with `asset!`, for example `Stylesheet { href: asset!("/assets/main.css") }`. SCSS is recompiled and the generated CSS reloaded. Images such as `img { src: asset!("/assets/logo.png") }` also update live.

## Tailwind

If a `tailwind.css` exists in the project root, `dx serve` downloads and runs the Tailwind CLI watcher over your Rust code; the input and output files are configurable via `tailwind_input` and `tailwind_output` in `Dioxus.toml`.

## Checked
Checked 2026-11-07 against the 0.7 Hot-Reloading Reference (read in full). Confirmed: RSX hot-reload scope and literal props, rebuild list, --hotpatch limits and r key, tip-crate limit, CSS, SCSS and image hot-reload, Tailwind detection and tailwind_input and tailwind_output. Nothing removed.
Method: documentation only; no commands were run.
