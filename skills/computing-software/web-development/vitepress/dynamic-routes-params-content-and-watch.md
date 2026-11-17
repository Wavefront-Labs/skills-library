---
id: computing-software.web-development.vitepress.dynamic-routes-params-content-and-watch
name: dynamic-routes-params-content-and-watch
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, dynamic-routes, defineroutes, watch, params, content, raw-content, transformpagedata]
level: sme
status: docs-checked
description: "Use params in pages, pass heavy content via the content property, type loaders with defineRoutes, and watch files for HMR."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Reading params.** In the template, use the `$params` global, or `useData().params` (a Vue ref) in script or components:

```md
- package name: {{ $params.pkg }}
- version: {{ $params.version }}
```

**Raw content.** Params are serialized into the client JS payload, so never put raw Markdown/HTML from a CMS in them. Put it on the path object's `content` property instead and render it with the special marker in the template:

```js
return posts.map((post) => ({
  params: { id: post.id },
  content: post.content   // raw Markdown or HTML
}))
```

```md
<!-- @content -->
```

**`defineRoutes`** (TypeScript) types hooks such as `paths`, `watch`, `transformPageData`:

```ts
import { defineRoutes } from 'vitepress'
export default defineRoutes({
  watch: ['../data/**/*.json'],
  async paths() { return [{ params: { pkg: 'foo' } }] },
  async transformPageData(pageData) { pageData.title = `${pageData.title} - Packages` }
})
```

**`watch`.** Glob patterns (fast-glob syntax), relative to the `.paths.js` file; the matched absolute paths are passed to `paths(watchedFiles)`. In dev, changes to watched files regenerate pages with HMR; in production all pages are generated once regardless.

```js
export default {
  watch: ['./templates/**/*.njk', '../data/**/*.json'],
  paths(files) {
    return files.filter(f => f.endsWith('.json')).map(f => {
      const data = JSON.parse(fs.readFileSync(f, 'utf-8'))
      return { params: { slug: data.slug }, content: render(data) }
    })
  }
}
```

## Checked

2026-11-04. Confirmed against the VitePress routing guide (Accessing Params in Page, Rendering Raw Content, Type-safe loader with defineRoutes, Watching Template and Data Files). Removed: the Verify step.

Method: documentation only; no commands were run.
