---
id: computing-software.web-development.vitepress.frontmatter-usage-and-access
name: frontmatter-usage-and-access
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, frontmatter, gray-matter, yaml-frontmatter, json-frontmatter, frontmatter-global, custom-frontmatter]
level: practitioner
status: docs-checked
description: "Use YAML or JSON frontmatter, override page options, and read it via $frontmatter, useData() and build-time interpolation."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/frontmatter.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/frontmatter-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VitePress parses frontmatter with gray-matter. It must be at the very top of the file (before anything, including `<script>`), as valid YAML between triple dashes:

```md
---
title: Docs with VitePress
editLink: true
---
```

Many site and theme options have frontmatter equivalents, so you can override behaviour for a single page. You can also add your own keys.

**Reading it**

```md
# {{ $frontmatter.title }}
```

or in `<script setup>`: `const { frontmatter } = useData()`.

`{{ $frontmatter.x }}` property accesses are resolved while the Markdown is rendered, so the value also ends up in the local search index, in `createContentLoader` output, in heading anchors (the heading above gets `id="docs-with-vitepress"`), and in link targets written without spaces around the expression like `[text]({{$frontmatter.link}})`. Other expressions are evaluated by Vue at runtime; wrapping an expression in `v-pre` shows it literally.

**JSON frontmatter** is also accepted: curly-brace JSON between `---` lines.

```json
---
{
  "title": "Blogging Like a Hacker",
  "editLink": true
}
---
```

Core reference keys (all pages): `title`, `titleTemplate`, `description`, `head`, `dir`. Default-theme keys: `layout`, `hero`, `features`, `navbar`, `sidebar`, `aside`, `outline`, `lastUpdated`, `editLink`, `footer`, `pageClass`, `isHome`.

## Checked

2026-11-04. Confirmed against the VitePress frontmatter guide (Usage, Accessing Frontmatter Data, Alternative Frontmatter Formats) and the Frontmatter Config page (core and default-theme keys). Removed: the Verify step.

Method: documentation only; no commands were run.
