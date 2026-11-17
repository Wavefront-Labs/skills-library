---
id: computing-software.web-development.vitepress.head-config-merging-and-recipes
name: head-config-merging-and-recipes
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, head, head-config, favicon, google-fonts, service-worker, google-analytics, meta-tags, transformhead]
level: advanced
status: docs-checked
description: "Add head tags in site config or frontmatter, understand how entries merge and dedupe, and apply recipes for favicon, fonts and analytics."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/frontmatter-config.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/deploy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`head` is an array of `[tag, attributes]` or `[tag, attributes, innerText]` tuples rendered before the closing `</head>`, after VitePress's own tags.

```ts
type HeadConfig =
  | [string, Record<string, string>]
  | [string, Record<string, string>, string]
```

**Merge order:** site config, locale config, directory config, page frontmatter, then `transformHead`. A later entry replaces an earlier one with the same key instead of being appended:
- any element with an `id` is keyed by its `id`;
- a `meta` without `id` is keyed by its first attribute other than `content` (for example `name`, `property`, `http-equiv`) plus its value.

Other elements are never deduplicated. To output several metas that would collide (multiple `<meta name="author">`), give each a unique `id`.

**Recipes**

```ts
head: [['link', { rel: 'icon', href: '/favicon.ico' }]]   // file in public/; with a base use /base/favicon.ico

head: [
  ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
  ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
  ['link', { href: 'https://fonts.googleapis.com/css2?family=Roboto&display=swap', rel: 'stylesheet' }]
]

head: [['script', { id: 'register-sw' }, `;(() => { if ('serviceWorker' in navigator) { navigator.serviceWorker.register('/sw.js') } })()`]]

head: [
  ['script', { async: '', src: 'https://www.googletagmanager.com/gtag/js?id=TAG_ID' }],
  ['script', {}, `window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'TAG_ID');`]
]
```

Per page, frontmatter takes YAML list-of-lists (`- - meta` then `- name: ...`). Beware root-absolute paths with `base: './'` (head entries are emitted verbatim).

Verify: view-source shows each tag once.

## Checked

2026-11-08. Read the VitePress docs source pages site-config (head and the example recipes), frontmatter-config (head) and deploy (relocatable builds). Confirmed the HeadConfig type, placement after VitePress tags, the merge order and keying rules, the favicon, fonts, service worker and analytics recipes, the frontmatter YAML form, and the verbatim-emission warning for base ./. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
