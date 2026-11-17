---
id: computing-software.web-development.drizzle-orm.drizzle-define-relations-v2
name: drizzle-define-relations-v2
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, relations, definerelations, one-to-many, many-to-many]
level: practitioner
status: docs-checked
description: "Declare relations once with defineRelations (RQB v2): one, many, from/to, through for many-to-many, optional, alias and parts."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/rqb.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/relations-v1-v2.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set up the relations that power db.query.

Relational Queries v2 has one dedicated place for the relations of all tables (the v1 to v2 guide targets `drizzle-orm@rc`). Define them in one place:

```ts
import { defineRelations } from 'drizzle-orm';
import * as schema from './schema';

export const relations = defineRelations(schema, (r) => ({
  users: {
    invitee: r.one.users({ from: r.users.invitedBy, to: r.users.id }),
    posts: r.many.posts(),
    groups: r.many.groups({
      from: r.users.id.through(r.usersToGroups.userId),
      to: r.groups.id.through(r.usersToGroups.groupId),
    }),
  },
  posts: { author: r.one.users({ from: r.posts.authorId, to: r.users.id }) },
}));
```

Then pass it to the client: `const db = drizzle(process.env.DATABASE_URL, { relations })`. The `r` parameter autocompletes tables plus `one`, `many` and `through`.

Details from the v1 to v2 guide:
- `fields` became `from`, `references` became `to`; both accept a single value or an array.
- `through` handles many-to-many without querying the junction table manually.
- `r.many.posts({ from: r.users.id, to: r.posts.authorId })` can define the many side alone, no mirror `one` needed (v1 required the `one` side on the other end).
- `optional: false` removes `null` from the related value's inferred type; it does not create a database constraint, so only use it when the related row always exists.
- `relationName` became `alias`, used to disambiguate several relations between the same two tables.
- Split definitions with `defineRelationsPart` and merge: `drizzle(url, { relations: { ...relations, ...part } })`.

Query the result with `db.query.users.findMany({ with: { posts: true } })`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (rqb.mdx, relations-v1-v2.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
