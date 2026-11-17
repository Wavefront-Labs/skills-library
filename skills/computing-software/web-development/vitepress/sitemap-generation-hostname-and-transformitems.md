---
id: computing-software.web-development.vitepress.sitemap-generation-hostname-and-transformitems
name: sitemap-generation-hostname-and-transformitems
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, sitemap, sitemap-xml, hostname, transformitems, lastmod, seo, sitemapstream]
level: practitioner
status: docs-checked
description: "Generate sitemap.xml with the sitemap option: hostname with base, lastmod via lastUpdated, SitemapStream options and transformItems."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/sitemap-generation.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-last-updated.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VitePress generates `sitemap.xml` out of the box once `sitemap.hostname` is set:

```ts
export default {
  sitemap: { hostname: 'https://example.com' }
}
```

**lastmod.** To emit `<lastmod>` tags, enable the site-level `lastUpdated` option. It reads git history, so CI needs a full clone (`fetch-depth: 0`), or every page gets the same date.

**Options.** The feature is powered by the `sitemap` npm module and the object is passed straight to its `SitemapStream` constructor, so any of its documented options work:

```ts
sitemap: { hostname: 'https://example.com', lastmodDateOnly: false }
```

**Base path.** If you use `base`, append it to the hostname:

```ts
export default {
  base: '/my-site/',
  sitemap: { hostname: 'https://example.com/my-site/' }
}
```

**transformItems.** Receives the array of sitemap items before they are written and must return an array. Use it to add, edit or filter entries:

```ts
sitemap: {
  hostname: 'https://example.com',
  transformItems: (items) => {
    items.push({ url: '/extra-page', changefreq: 'monthly', priority: 0.8 })
    return items
  }
}
```


Verify: after `vitepress build`, open the generated `sitemap.xml` in the build output and check urls and lastmod.

## Checked

2026-11-08. Read the VitePress docs source pages sitemap-generation and default-theme-last-updated. Confirmed the hostname option, lastmod via lastUpdated, the shallow-clone and fetch-depth 0 advice, pass-through to the sitemap module SitemapStream, appending base to hostname, and the transformItems hook. Loosened the output path in the verify step because the pages do not state it.

Method: docs-only read of cited pages, 2026-11-08
