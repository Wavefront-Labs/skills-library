---
id: computing-software.web-development.prisma.client-select-omit
name: client-select-omit
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-select-omit, prisma, omit-fields-global, default-scalar-fields, select-vs-include]
level: intro
status: docs-checked
description: "Control returned fields with select, include and omit, including the client-level omit option, and know the default result shape."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/select-fields.mdx", "https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/excluding-fields.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# select, include and omit

Default result: all scalar fields of the model, no relations.

- `select: { email: true, name: true }` returns only those. Nest for relations: `select: { email: true, posts: { select: { title: true, published: true } } }`.
- `include: { posts: true }` returns all scalars plus the relation.
- `omit` returns the normal shape minus listed fields: `findUnique({ where: { id: 1 }, omit: { password: true } })`.

Global omit on the client:

```ts
const prisma = new PrismaClient({
  omit: { user: { password: true } },
});
```

Pick `select` for a small subset; pick `omit` when the default is almost right and a few sensitive or noisy fields must go. In Prisma 7 the `PrismaClient` constructor also takes the driver adapter, `new PrismaClient({ adapter, omit: ... })` (see `prisma-client-driver-adapter`).

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-client/queries/select-fields and excluding-fields pages, orm/v7): default result shape, select, include, nested select, per-query and client-level omit, select-versus-omit guidance. Removed an unconfirmed select/include claim and filler text.

Method: documentation only; no commands were run.
