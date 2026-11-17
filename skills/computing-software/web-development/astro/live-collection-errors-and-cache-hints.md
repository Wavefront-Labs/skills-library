---
id: computing-software.web-development.astro.live-collection-errors-and-cache-hints
name: live-collection-errors-and-cache-hints
category: computing-software
field: web-development
product: astro
tags: [live-errors, cachehint, astro-cache, invalidate]
level: sme
status: docs-checked
description: "Handle live collection error types and apply loader cache hints with Astro.cache.set and cache.invalidate for entries and collections."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/content-collections.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`getLiveCollection()` and `getLiveEntry()` return an `error` that is one of: the loader's own error type, `LiveEntryNotFoundError`, `LiveCollectionValidationError` (data does not match schema), `LiveCollectionCacheHintError` (invalid cache hint), or `LiveCollectionError` (other, e.g. uncaught loader errors).

```astro
---
export const prerender = false; // Not needed in 'server' mode

import { LiveEntryNotFoundError } from "astro/content/runtime";
import { getLiveEntry } from "astro:content";

const { entry, error } = await getLiveEntry("products", Astro.params.id);

if (error) {
  if (error instanceof LiveEntryNotFoundError) {
    console.error(`Product not found: ${error.message}`);
    Astro.response.status = 404;
  } else {
    console.error(`Error loading product: ${error.message}`);
    return Astro.redirect("/500");
  }
}
---
```

When loaders provide cache hints, results include a `cacheHint` (tags for invalidation, `lastModified`). Apply it with `Astro.cache.set()` and add your own options:

```astro
---
const { entry, error, cacheHint } = await getLiveEntry('products', Astro.params.id);
if (cacheHint) {
  Astro.cache.set(cacheHint);
}
Astro.cache.set({ maxAge: 300 });
---
```

You can also pass the entry itself: `Astro.cache.set(entry);`. For a collection, hints merge: tags accumulate and the most recent `lastModified` wins.

Invalidate a specific entry:

```ts
await context.cache.invalidate(entry);
```

## Checked

2026-11-04. Confirmed against the Astro content collections guide: the five error types, cacheHint with Astro.cache.set, merged collection hints, and cache.invalidate. Nothing removed.

Method: documentation only; no commands were run.
