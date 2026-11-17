---
id: computing-software.web-development.astro.live-content-collections
name: live-content-collections
category: computing-software
field: web-development
product: astro
tags: [live-collections, live-config, getlivecollection, getliveentry, live-loader]
level: advanced
status: docs-checked
description: "Define request-time live collections in src/live.config.ts, query them with getLiveCollection and getLiveEntry, and know their limits versus build-time collections."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/content-collections.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Live collections fetch data at request time; an adapter for on-demand rendering is required. Differences from build-time: config in `src/live.config.ts`, `defineLiveCollection()`, loader implements `loadCollection` and `loadEntry`, data is returned not stored, and you use `getLiveCollection()`/`getLiveEntry()`.

Limits: no MDX support, no image optimization, data fetched on each request (unless cached), no data store persistence. There are no built-in live loaders; write or install one.

```ts title="src/live.config.ts"
import { defineLiveCollection } from 'astro:content';
import { storeLoader } from '@mystore/astro-loader';

const products = defineLiveCollection({
  loader: storeLoader({
    apiKey: process.env.STORE_API_KEY,
    endpoint: 'https://api.mystore.com/v1',
  }),
});

export const collections = { products };
```

Query with loader-specific filters:

```astro
---
export const prerender = false; // Not needed in 'server' mode
import { getLiveCollection, getLiveEntry } from "astro:content";

const { entries: draftArticles } = await getLiveCollection("articles", {
  status: "draft",
  author: "john-doe",
});

const { entry: product } = await getLiveEntry("products", Astro.params.slug);
---
```

If the loader returns a `rendered` property you can use `render()` and `<Content />`. An optional Zod `schema` takes precedence over the loader's types.

## Checked

2026-11-04. Confirmed against the Astro content collections guide: src/live.config.ts, defineLiveCollection, loadCollection and loadEntry, the listed limits, getLiveCollection and getLiveEntry, and rendered. Nothing removed.

Method: documentation only; no commands were run.
