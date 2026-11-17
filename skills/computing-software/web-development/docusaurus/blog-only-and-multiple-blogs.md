---
id: computing-software.web-development.docusaurus.blog-only-and-multiple-blogs
name: blog-only-and-multiple-blogs
category: computing-software
field: web-development
product: docusaurus
tags: [blog-only-mode, multiple-blogs, routebasepath, second-blog, disable-docs]
level: advanced
status: docs-checked
description: "Serve the blog at the site root with docs disabled, or run a second blog by adding another content-blog plugin instance with its own id, path and routeBasePath."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/blog.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Blog-only mode: set `routeBasePath: '/'` so the post list is the index page.

```js title="docusaurus.config.js"
presets: [
  ['@docusaurus/preset-classic', {
    docs: false, // optional
    blog: {routeBasePath: '/'},
  }],
],
```

- Delete `./src/pages/index.js` or two files will map to the same route.
- If you disable docs, remove references to the docs plugin elsewhere in the config, notably docs navbar items.

Multiple blogs: the classic theme assumes one blog, but you can add another `@docusaurus/plugin-content-blog` instance in `plugins`. It needs a unique `id`, a `routeBasePath` different from the first blog (no trailing slash) to avoid path collisions, and a `path` to its directory.

```js
plugins: [
  ['@docusaurus/plugin-content-blog', {
    id: 'second-blog',
    routeBasePath: 'my-second-blog',
    path: './my-second-blog',
  }],
],
```

## Checked

2026-11-04: read the Docusaurus blog page in full. Confirmed blog-only mode, the two warnings, and the multiple-blog plugin options (unique id, routeBasePath without trailing slash, path). Nothing removed.

Method: documentation only; no commands were run.
