---
id: computing-software.web-development.vitepress.create-content-loader
name: create-content-loader
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, createcontentloader, content-loader, blog-index, posts-data, excerpt, transform, rss-feed]
level: advanced
status: docs-checked
description: "Build blog or API index pages with createContentLoader: glob a content folder, include src/html/excerpt, transform and sort."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/data-loading.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For archive or index pages that list a content collection, use the helper instead of writing a loader by hand:

```js
// posts.data.js
import { createContentLoader } from 'vitepress'
export default createContentLoader('posts/*.md', /* options */)
```

The glob is relative to the **source directory**. The helper returns a `{ watch, load }` object, caches by file modified time for dev speed, and only handles Markdown files (others are skipped). The data is `ContentData[]`:

```ts
interface ContentData {
  url: string                       // e.g. /posts/hello.html (does not include base)
  frontmatter: Record<string, any>
  src?: string                      // only with includeSrc
  html?: string                     // only with render
  excerpt?: string                  // only with excerpt
}
```

By default only `url` and `frontmatter` are returned, because the data is inlined into the client bundle. Opt in with options:

```js
export default createContentLoader('posts/*.md', {
  includeSrc: true,   // raw markdown source
  render: true,       // rendered full page HTML
  excerpt: true,      // content above the first `---` (string separator or function also accepted)
  transform(raw) {
    return raw
      .sort((a, b) => +new Date(b.frontmatter.date) - +new Date(a.frontmatter.date))
      .map((p) => ({ url: p.url, title: p.frontmatter.title }))
  }
})
```

Use it in a page: `import { data as posts } from './posts.data.js'` and `v-for` over `posts`.

It also works inside build hooks to generate files such as an RSS feed:

```js
async buildEnd() {
  const posts = await createContentLoader('posts/*.md').load()
}
```

Note `url` omits `base`, so normalize paths yourself; content-loader URLs stay site-absolute under relocatable builds. Use `transform` to trim fields, because the loaded data is inlined into the client bundle.

## Checked

2026-11-04. Confirmed against the VitePress data-loading guide (createContentLoader, ContentData, ContentOptions, buildEnd usage) and the deploy guide (content-loader URLs stay site-absolute in relocatable builds). Removed: the Verify step.

Method: documentation only; no commands were run.
