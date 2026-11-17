---
id: computing-software.web-development.docusaurus.seo-metadata-and-robots
name: seo-metadata-and-robots
category: computing-software
field: web-development
product: docusaurus
tags: [seo, metadata, headtags, robots-txt, noindex]
level: practitioner
status: docs-checked
description: "Make a Docusaurus site search-engine friendly: global metadata and headTags, per-page front matter and Head, robots.txt versus noIndex, sitemap and structured data."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/seo.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global metadata: `themeConfig.metadata` declares `<meta>` tags; the top-level `headTags` injects arbitrary tags (links, JSON-LD):

```js title="docusaurus.config.js"
themeConfig: {
  metadata: [{name: 'keywords', content: 'cooking, blog'}],
},
headTags: [
  {tagName: 'link', attributes: {rel: 'preconnect', href: 'https://example.com'}},
  {tagName: 'script', attributes: {type: 'application/ld+json'},
   innerHTML: JSON.stringify({'@context': 'https://schema.org/', '@type': 'Organization', name: 'Example'})},
],
```

With i18n configured you get `hreflang` alternate links automatically.

Per page, prefer front matter, which sets both `description` and `og:description`:

```md
---
title: Title for search engines
description: A short description of this page
image: thumbnail for social cards
keywords: [keywords, describing, the main topics]
---
```

Official plugins all support `title`, `description`, `keywords` and `image`. Markdown can also use a `<head>` tag. In React pages use `<Head>` from `@docusaurus/Head`, or pass `title` and `description` props to `<Layout>`.

Docusaurus generates static HTML per route, and blogs get rich search results data from post date, authors and image.

Robots: `static/robots.txt` does not stop HTML pages being indexed. To block the whole site use the `noIndex` site config (or an `X-Robots-Tag: noindex` header if the host allows; GitHub Pages does not). For one page use `<meta name="robots" content="noindex">`.

The sitemap plugin (in `preset-classic`) writes `sitemap.xml` at build and filters pages with a `noindex` robots meta directive.

Use slugs for human-readable URLs, and alt text on images.

## Checked

2026-11-04. Read in full against the Docusaurus SEO page (seo.mdx): themeConfig.metadata and headTags, hreflang with i18n, front matter fields and the og:description tip, official plugins supporting title/description/keywords/image, Head and Layout props, noIndex and the GitHub Pages X-Robots-Tag note, robots.txt not preventing indexing, sitemap plugin in preset-classic and its noindex filtering, slugs and alt text all match. Nothing removed.

Method: documentation only; no commands were run.
