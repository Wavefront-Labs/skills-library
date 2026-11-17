---
id: computing-software.web-development.prisma.schema-location-multi-file
name: schema-location-multi-file
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-location, prisma, multi-file-schema, schema-flag, prisma-folder]
level: practitioner
status: docs-checked
description: "Where the Prisma CLI looks for the schema, and how to run a multi-file schema folder with config schema key, a main generator file and migrations beside it."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/overview/location.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Schema location and multi-file schemas

The CLI resolves the schema in this order:

1. the `--schema` flag (available for introspect, generate, migrate and studio commands), for example `prisma generate --schema=./alternative/schema.prisma`
2. the `schema` property in `prisma.config.ts`
3. defaults `./prisma/schema.prisma`, then `./schema.prisma`

The CLI prints which schema it loaded (for example "Prisma Schema loaded from prisma/schema.prisma").

Multi-file layout:

```
prisma/
├── migrations
├── models
│   ├── posts.prisma
│   └── users.prisma
└── schema.prisma
```

You must always name the directory explicitly: `prisma migrate dev --schema ./prisma` or, recommended for v7, in config:

```ts
export default defineConfig({
  schema: "prisma/",
  migrations: { path: "prisma/migrations", seed: "tsx prisma/seed.ts" },
  datasource: { url: env("DATABASE_URL") },
});
```

Rules and traps:

- The `schema.prisma` file with the `generator` block must sit directly in the configured directory. With `schema: 'prisma'` it must be `prisma/schema.prisma`, not `prisma/models/schema.prisma`.
- `migrations` must be at the same level as that `schema.prisma`.
- With files in `prisma/`, commands work without extra configuration because `./prisma/schema.prisma` is a default location.

Docs tips: organise by domain (`user.prisma`, `post.prisma`), keep names short and clear, and have one obvious main file for the generator block (`main.prisma`, `schema.prisma` or `base.prisma`).

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/overview/location pages, orm/v7): CLI schema lookup order, printed schema path, multi-file layout, explicit directory rule, schema.prisma and migrations placement, tips.

Method: documentation only; no commands were run.
