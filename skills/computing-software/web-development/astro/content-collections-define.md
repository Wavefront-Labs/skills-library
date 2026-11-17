---
id: computing-software.web-development.astro.content-collections-define
name: content-collections-define
category: computing-software
field: web-development
product: astro
tags: [content-collections, define-collection, content-config, loader, schema]
level: intro
status: docs-checked
description: "Define build-time content collections in src/content.config.ts with defineCollection, a loader and an optional Zod schema, and decide when a collection is the right tool."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/content-collections.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A collection is a set of structurally identical entries stored locally (files) or fetched remotely. Each collection needs a `loader` (required) and may have a `schema` (optional, highly recommended). Build-time collections go in `src/content.config.ts` (`.js` and `.mjs` also supported); export a single `collections` object.

```ts title="src/content.config.ts"
import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
  }),
});

export const collections = { blog };
```

Use build-time collections for static data, build-time optimization, MDX and image optimization. Skip collections when you have only a few pages (use page components), when displaying unprocessed files like PDFs (use `public/`), or when your data source's SDK has no loader and you prefer it directly.

If you changed tsconfig to `base`, add to `compilerOptions`: `"strictNullChecks": true` and `"allowJs": true` (not needed for `strict` or `strictest`). After a new or updated schema, you may need to restart the dev server or sync the content layer.

## Checked

2026-11-04. Confirmed against the Astro content collections guide: src/content.config.ts, loader and schema, tsconfig compilerOptions, and when not to use a collection. Fixed the function name to defineCollection (was lowercased throughout).

Method: documentation only; no commands were run.
