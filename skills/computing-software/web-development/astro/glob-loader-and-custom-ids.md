---
id: computing-software.web-development.astro.glob-loader-and-custom-ids
name: glob-loader-and-custom-ids
category: computing-software
field: web-development
product: astro
tags: [glob-loader, entry-id, slug-frontmatter, generateid]
level: practitioner
status: docs-checked
description: "Load directories of Markdown, MDX, JSON, YAML or TOML with the glob() loader, and override entry ids with a slug property or generateId."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/content-collections.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`glob()` fetches entries from directories of Markdown, MDX, Markdoc, JSON, YAML or TOML files anywhere on the filesystem. It requires a `pattern` (micromatch globs) and a `base` path.

```ts title="src/content.config.ts"
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/data/blog" }),
});

export const collections = { blog };
```

Each entry `id` is generated in URL-friendly form from its filename. Override one entry with a `slug` property in frontmatter (or the data object for JSON):

```md title="src/blog/1.md"
---
title: My Blog Post
slug: my-custom-id/supports/slashes
---
Your blog post content here.
```

Or adjust generation for the whole collection with `generateId`, e.g. to keep uppercase letters instead of the default lowercase conversion:

```js
const authors = defineCollection({
  loader: glob({
    pattern: "**/*.json",
    base: "./src/data/authors",
    generateId: ({ entry }) => entry.replace(/\.json$/, ""),
  }),
});
```

## Checked

2026-11-04. Confirmed against the Astro content collections guide: glob() pattern and base, slug override, and generateId. Nothing removed.

Method: documentation only; no commands were run.
