---
id: computing-software.web-development.astro.html-components
name: html-components
category: computing-software
field: web-development
product: astro
tags: [html-components, legacy-html, is-inline, public-assets]
level: practitioner
status: docs-checked
description: "Use plain .html files as Astro components or pages and know which Astro features they lack: frontmatter, imports, expressions, bundled scripts."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/astro-components.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Astro supports importing and using `.html` files as components, or placing them under `src/pages/` as pages. Use them when reusing code from a site built without a framework, or to guarantee a component has no dynamic features.

HTML components must contain only valid HTML, so they lack key Astro features:

- No frontmatter, server-side imports, or dynamic expressions.
- Any `<script>` tags are left unbundled, treated as if they had an `is:inline` directive.
- They can only reference assets that are in the `public/` folder.

A `<slot />` element inside an HTML component works as it would in an Astro component. To use the HTML Web Component Slot element instead, add `is:inline` to your `<slot>` element:

```html
<slot is:inline></slot>
```

## Checked

2026-11-04. Confirmed against the Astro components page: .html components and pages, the three listed limits, slot behaviour and is:inline on slot. Nothing removed.

Method: documentation only; no commands were run.
