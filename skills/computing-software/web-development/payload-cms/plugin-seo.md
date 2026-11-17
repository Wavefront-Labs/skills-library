---
id: computing-software.web-development.payload-cms.plugin-seo
name: plugin-seo
category: computing-software
field: web-development
product: payload-cms
tags: [seo-plugin, meta-fields, generatetitle, plugin-seo]
level: practitioner
status: docs-checked
description: "Add SEO meta fields and a search preview to collections with @payloadcms/plugin-seo, auto-generating titles and descriptions."
sources:
  - https://payloadcms.com/docs/plugins/seo
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SEO plugin

Goal: manage SEO metadata in the Admin Panel.

```bash
pnpm add @payloadcms/plugin-seo
```

```ts
import { seoPlugin } from '@payloadcms/plugin-seo'

plugins: [
  seoPlugin({
    collections: ['pages'],
    uploadsCollection: 'media',
    generateTitle: ({ doc }) => `Website.com — ${doc.title}`,
    generateDescription: ({ doc }) => doc.excerpt,
  }),
]
```

The plugin adds a `meta` field group to each listed collection or global, with indicators that help write good metadata, an "auto-generate" action that calls your generate functions, and a live search-engine snippet preview. Generate functions receive context such as `doc`, `collectionSlug`, `locale`, `req`.

You can extend the field set with custom fields like `og:title` or `json-ld`.

Verify: edit a page and click auto-generate on the meta title.

## Checked

2026-11-04. Read plugins/seo. Confirmed: install command, the seoPlugin example (collections, uploadsCollection, generateTitle, generateDescription), the meta field group (title, description, image), auto-generate calling your functions, hints and character counters, the real-time search snippet preview, custom fields such as og:title and json-ld, and the generate function arguments (doc, collectionSlug, locale, req among others).
Method: documentation only; no commands were run.
