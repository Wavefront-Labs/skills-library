---
id: computing-software.web-development.astro.collection-references
name: collection-references
category: computing-software
field: web-development
product: astro
tags: [reference, getentry, getentries, related-entries]
level: practitioner
status: docs-checked
description: "Link collection entries with reference() in a schema and resolve them with getEntry and getEntries, e.g. post authors and related posts."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/content-collections.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`reference()` defines a schema property as an entry of another collection:

```ts title="src/content.config.ts"
import { defineCollection, reference } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const blog = defineCollection({
  loader: glob({ base: "./src/content/blog", pattern: "**/*.{md,mdx}" }),
  schema: z.object({
    title: z.string(),
    // Reference a single author from the `authors` collection by `id`
    author: reference("authors"),
    // Reference an array of related posts from the `blog` collection by `id`
    relatedPosts: z.array(reference("blog")),
  }),
});
```

Frontmatter supplies ids:

```yaml
---
title: "Welcome to my blog"
author: ben-holmes # references `src/data/authors/ben-holmes.json` 
relatedPosts:
- about-me # references `src/content/blog/about-me.md`
---
```

References become objects with `collection` and `id` keys. Resolve them with `getEntry()` (one) or `getEntries()` (many):

```astro
---
import { getEntry, getEntries } from "astro:content";

const blogPost = await getEntry("blog", "Adventures in Space");
const author = await getEntry(blogPost.data.author);
const relatedPosts = await getEntries(blogPost.data.relatedPosts);
---
```

## Checked

2026-11-04. Confirmed against the Astro content collections guide: reference(), frontmatter ids, collection and id objects, getEntry and getEntries. Nothing removed.

Method: documentation only; no commands were run.
