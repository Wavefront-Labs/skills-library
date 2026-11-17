---
id: computing-software.web-development.astro.custom-404-and-500-pages
name: custom-404-and-500-pages
category: computing-software
field: web-development
product: astro
tags: [error-pages, not-found-page, custom-500, error-prop]
level: practitioner
status: docs-checked
description: "Add custom 404 and 500 error pages in Astro, use the error prop on 500.astro safely, and know which pages apply to on-demand rendering."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/astro-pages.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
404: create `src/pages/404.astro` or `404.md`. It builds to a `404.html` page, which most deploy services find and use.

500: create `src/pages/500.astro` for pages rendered on demand. It is not available for prerendered pages. If an error occurs rendering this page, your host's default 500 page is shown.

In development with a `500.astro`, the runtime error is logged in your terminal instead of the error overlay.

`500.astro` is automatically passed an `error` prop for any error thrown during rendering (page, middleware, etc.). Its type can be anything:

```astro title="src/pages/500.astro"
---
interface Props {
  error: unknown;
}

const { error } = Astro.props;
---
<div>{error instanceof Error ? error.message : "Unknown error"}</div>
```

To avoid leaking sensitive information, evaluate the error first and return appropriate content. Do not display the error's stack, since it reveals how your server code is structured.

For static redirect pages, see the experimental redirect page feature.

## Checked

2026-11-04. Confirmed against the Astro pages page: 404.astro/404.md building to 404.html, 500.astro for on-demand pages only, host default on render error, dev logging in the terminal, the error prop and its unknown type, the stack warning, redirect page pointer. Nothing removed.

Method: documentation only; no commands were run.
