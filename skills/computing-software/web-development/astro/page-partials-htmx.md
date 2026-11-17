---
id: computing-software.web-development.astro.page-partials-htmx
name: page-partials-htmx
category: computing-software
field: web-development
product: astro
tags: [partials, htmx, partial-export, html-fragments]
level: advanced
status: docs-checked
description: "Mark pages in src/pages as partials so they emit HTML fragments without doctype or head, for use with htmx and similar libraries; know the style caveat."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/astro-pages.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Partials are page components in `src/pages/` not meant to render as full pages. They do not include `<!DOCTYPE html>` or any `<head>` content such as scoped styles and scripts, but their HTML is served at the URL matching the file path, so a library (htmx, Stimulus, jQuery) can load sections dynamically.

Caution: do not use partials when the component contains scoped styles or scripts, as these are stripped from the output.

Files that can export `partial` (`.astro`, `.mdx`, not `.md`) can be partials:

```astro title="src/pages/partials/clicked.astro"
---
export const partial = true;
---
<div>I was clicked!</div>
```

Point htmx at the partial URL:

```astro title="src/pages/index.astro"
<button hx-post="/partials/clicked/"
  hx-trigger="click"
  hx-target="#parent-div"
  hx-swap="innerHTML"
>
  Click Me!
</button>
```

The partial must exist at the corresponding file path and export `partial = true`. Partials are an alternative to islands and `<script>` tags for dynamic content.

## Checked

2026-11-04. Confirmed against the Astro pages page: partial export, which file types can be partials, no doctype or head, scoped styles and scripts caveat, htmx example, alternative to islands. Nothing removed.

Method: documentation only; no commands were run.
