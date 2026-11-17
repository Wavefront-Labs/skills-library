---
id: computing-software.web-development.docusaurus.docs-only-mode
name: docs-only-mode
category: computing-software
field: web-development
product: docusaurus
tags: [docs-only-mode, routebasepath, homepage, slug, disable-blog]
level: practitioner
status: docs-checked
description: "Serve Docusaurus docs at the site root with routeBasePath, make a doc the homepage with slug, and avoid the duplicate-route trap with src/pages/index.js."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/docs/docs-introduction.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Docs are organised at four levels, lowest to highest: pages, sidebars, versions, plugin instances.

By default docs are served under `/docs`. For a docs-only site, serve them at the root:

```js title="docusaurus.config.js"
presets: [
  ['@docusaurus/preset-classic', {
    docs: {
      routeBasePath: '/', // docs at the site root
    },
    blog: false, // optional
  }],
],
```

`routeBasePath: '/'` only changes where docs live (`https://example.com/some-doc`). The blog, if still enabled, remains at its `blog/` subroute, so you need not give up other plugins.

Put a page at the root with front matter:

```md title="docs/intro.md"
---
slug: /
---
```

If you do this, delete the existing homepage at `./src/pages/index.js`, otherwise two files map to the same route.

A blog-only mode works the same way (see the blog guide).

## Checked

2026-11-04. Read in full against the Docusaurus Docs Introduction page (docs-introduction.mdx), Docs-only mode section: four organisation levels, routeBasePath: '/', blog: false as optional, blog remaining at blog/, slug: / front matter, deleting src/pages/index.js and blog-only mode pointer all match. Nothing removed.

Method: documentation only; no commands were run.
