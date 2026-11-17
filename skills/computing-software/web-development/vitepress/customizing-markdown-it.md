---
id: computing-software.web-development.vitepress.customizing-markdown-it
name: customizing-markdown-it
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, markdown-it, markdown-config, anchor-plugin, mdit-plugin, toc-options, markdown-headers]
level: sme
status: docs-checked
description: "Customize the markdown-it instance with markdown.config(md), anchor and toc options, and enable page.headers collection."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/markdown.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VitePress renders Markdown with markdown-it, and many extensions are plugins. The `markdown` option lets you change them:

```js
import { defineConfig } from 'vitepress'
import { headerLink } from '@mdit/plugin-anchor'
import markdownItFoo from 'markdown-it-foo'

export default defineConfig({
  markdown: {
    // options for @mdit/plugin-anchor
    anchor: { permalink: headerLink() },
    // options for @mdit-vue/plugin-toc
    toc: { level: [1, 2] },
    config: (md) => {
      md.use(markdownItFoo)     // use more markdown-it plugins
    }
  }
})
```

- `anchor`: forwards to `@mdit/plugin-anchor`.
- `toc`: forwards to `@mdit-vue/plugin-toc`; it controls `[[toc]]`.
- `config(md)`: receive the markdown-it instance to register extra plugins or rules.
- `headers`: set `true` (or pass `@mdit-vue/plugin-headers` options) to collect headings into `useData().page.headers`. It is off by default; the default theme's outline reads rendered headings from the page content, so it works without it. Enable it if your own layout needs the heading tree.

Related options in the same block: `lineNumbers`, `math`, `image.lazyLoad`, `container` labels and `customContainers`, `include`, `snippet`, `codeCopyButton` strings per locale.

Because the renderer is created once for the whole site, per-locale markdown strings can only be declared in the main config.

## Checked

2026-11-04. Confirmed against the VitePress Markdown guide (Advanced Configuration, Image Lazy Loading, Math, Markdown File Inclusion options), the site-config page (markdown option and markdown.headers), the runtime-api page (page.headers only populated with markdown.headers; outline reads rendered headings) and the i18n guide (per-locale markdown strings, renderer created once, main config only). Removed: the Verify step.

Method: documentation only; no commands were run.
