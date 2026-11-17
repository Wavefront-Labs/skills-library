---
id: computing-software.web-development.astro.pages-file-types-and-linking
name: pages-file-types-and-linking
category: computing-software
field: web-development
product: astro
tags: [pages, file-based-routing, src-pages, links]
level: intro
status: docs-checked
description: "Create Astro pages in src/pages: supported file types, file-based routing, linking between pages with root-relative URLs, and Markdown pages with layout."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/astro-pages.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pages live in `src/pages/`. Supported file types:

- `.astro`
- `.md`
- `.mdx` (with the MDX integration installed)
- `.html`
- `.js`/`.ts` (as endpoints)

Each file becomes an endpoint based on its file path (file-based routing). A single file can generate many pages via dynamic routing.

Link with standard `<a>` elements and a URL path relative to your root domain, not a relative file path:

```astro title="src/pages/index.astro"
Read more <a href="/authors/sonali/">about Sonali</a>.
```

A page must produce a full HTML document. If not included, Astro adds the `<!DOCTYPE html>` declaration and `<head>` content to any `.astro` component in `src/pages/`; opt out by marking it a partial. Wrap pages in a layout to avoid repeating head/body:

```astro title="src/pages/index.astro"
---
import MySiteLayout from "../layouts/MySiteLayout.astro";
---
<MySiteLayout>
  <p>My page content, wrapped in a layout!</p>
</MySiteLayout>
```

Markdown pages use the `layout` frontmatter property:

```md
---
# Example: src/pages/page.md
layout: ../layouts/MySiteLayout.astro
title: My Markdown page
---
# Title
```

For directories of similar Markdown files such as blog posts, prefer content collections.

## Checked

2026-11-04. Confirmed against the Astro pages page: supported file types, file-based routing, root-relative links, automatic doctype and head, layouts, Markdown layout property, content collections tip. Nothing removed.

Method: documentation only; no commands were run.
