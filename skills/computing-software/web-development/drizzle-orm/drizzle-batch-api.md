---
id: computing-software.web-development.drizzle-orm.drizzle-batch-api
name: drizzle-batch-api
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, batch, neon-http, d1, serverless]
level: advanced
status: docs-checked
description: "Send several Drizzle statements in one round trip with db.batch, with typed tuple results, on drivers that support batching such as Neon HTTP."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/batch-api.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/sqlite/batch-api.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: cut round trips on HTTP drivers.

The PostgreSQL doc states batching is supported with the Neon HTTP driver (the SQLite docs describe the equivalent for D1 and LibSQL).

```ts
const batchResponse = await db.batch([
  db.insert(usersTable).values({ id: 1, name: 'John' }).returning({ id: usersTable.id }),
  db.update(usersTable).set({ name: 'Dan' }).where(eq(usersTable.id, 1)),
  db.query.usersTable.findMany({}),
  db.select().from(usersTable).where(eq(usersTable.id, 1)),
]);
```

The result is a typed tuple matching the statements in order, for example `[{ id: number }[], NeonHttpQueryResult, rows[], rows[]]`.

Builders allowed in `db.batch`: `db.query.<table>.findMany()`, `findFirst()`, `db.select()...`, `db.update()...`, `db.delete()...`, `db.insert()...`.

SQLite builders also allowed in a batch: `db.all()`, `db.get()`, `db.values()`, `db.run()`, `db.execute()`.

Per the SQLite page, with the libSQL client a batch is statements executed in order in an implicit transaction that commits if all succeed and rolls back if any fails; D1 batching sends multiple statements in one call, which can reduce network round-trip latency. The PostgreSQL page says nothing about transaction semantics for Neon HTTP batches, so check the Neon driver docs before relying on atomicity there.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (batch-api.mdx, batch-api.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
