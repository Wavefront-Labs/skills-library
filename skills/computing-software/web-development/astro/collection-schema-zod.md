---
id: computing-software.web-development.astro.collection-schema-zod
name: collection-schema-zod
category: computing-software
field: web-development
product: astro
tags: [zod, collection-schema, type-safety, validation]
level: practitioner
status: docs-checked
description: "Validate and type collection entries with a Zod schema imported from astro/zod, including coerced dates, optional fields, and the image() refine limitation."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/content-collections.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Schemas enforce consistent frontmatter or entry data through Zod validation and generate TypeScript types for queries. A violating file produces a helpful error. When you use a schema, every frontmatter or data property must be defined with a Zod type.

Import `z` from `"astro/zod"`, a re-export of Zod supporting all features of Zod 4.

```ts title="src/content.config.ts"
import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob, file } from "astro/loaders";

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/data/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
  }),
});
const dogs = defineCollection({
  loader: file("src/data/dogs.json"),
  schema: z.object({
    id: z.string(),
    breed: z.string(),
    temperament: z.array(z.string()),
  }),
});

export const collections = { blog, dogs };
```

All Zod schema methods (e.g. `.parse()`, `.transform()`) are available with some limitations. Notably, custom validation checks on images using `image().refine()` are unsupported.

You may need to restart the dev server or sync the content layer to define the `astro:content` module after changing a schema.

## Checked

2026-11-04. Confirmed against the Astro content collections guide: astro/zod re-export of Zod 4, schema examples, the image().refine() limitation and the sync/restart note. Nothing removed.

Method: documentation only; no commands were run.
