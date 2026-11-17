---
id: computing-software.web-development.dioxus.dioxus-translate-html-to-rsx
name: dioxus-translate-html-to-rsx
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, dx-translate, rsx, html-to-rsx, raw, file, output, component]
level: intro
status: docs-checked
description: "Convert HTML into Dioxus RSX with dx translate: --raw for strings, --file for files, --output to write a file, --component to wrap in a function."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/tools/translate.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Translate HTML to RSX with dx translate

Goal: turn pasted or existing HTML into `rsx!` markup instead of rewriting it by hand.

## Commands
```sh
dx translate --file index.html                                   # translate a file
dx translate --raw "<div>Hello world</div>"                      # translate a string
dx translate --raw "<div>Hello world</div>" --output index.rs    # write to a file
dx translate --raw "<div>Hello world</div>" --component          # wrap in a component
dx translate --help                                              # all flags
```
Without `--output` the RSX goes to stdout.

The `--file` and `--raw` forms of the example above both output:
```rs
div { "Hello world" }
```
With `--component` the output is:
```rs
fn component() -> Element {
   rsx! {
      div { "Hello world" }
   }
}
```

## What the conversion does (from the docs example)
- `class="..."` becomes `class: "..."`, text nodes become quoted strings, nested elements become nested blocks.
- Attributes with dashes become underscored identifiers, for example `data-dioxus-id` becomes `data_dioxus_id` and `dioxus-prevent-default` becomes `dioxus_prevent_default`.
- `<span>Text</span>` becomes `span { "Text" }`.

## Gotchas
- RSX is a custom, more concise format than HTML; the docs present translate as the way to avoid hand-converting large HTML chunks.
- In the docs example the image paths in the shown output differ from the input (`static/...` became `/assets/static/...`), so review the result before pasting.

## Checked

2026-11-08. Confirmed against the dx translate page (read in full): --file, --raw, --output, --component, --help, stdout default, dash-to-underscore attribute names, and the changed image paths in the documented output.

Method: documentation only; no commands were run.
