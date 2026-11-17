---
id: computing-software.web-development.drizzle-orm.drizzle-prepared-statements-performance
name: drizzle-prepared-statements-performance
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, prepared-statements, placeholder, serverless, performance]
level: advanced
status: docs-checked
description: "Speed up hot queries with prepare() and sql.placeholder, and reuse connections and prepared statements in serverless functions but not edge functions."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/perf-queries.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/perf-serverless.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: remove per-call SQL building cost.

Without preparation, each query concatenates the builder configuration into a SQL string, sends it and the params to the driver, and the driver compiles it to a binary executable format. With a prepared statement you concatenate once on the Drizzle side and the driver can reuse the precompiled SQL; the docs say this has extreme performance benefits on large SQL queries.

```ts
const prepared = db.select().from(customers).prepare("statement_name");
const res1 = await prepared.execute();
```

Placeholders carry runtime values:

```ts
const p1 = db.select().from(customers).where(eq(customers.id, sql.placeholder('id'))).prepare("p1");
await p1.execute({ id: 10 });
const p2 = db.select().from(customers)
  .where(sql`lower(${customers.name}) like ${sql.placeholder('name')}`).prepare("p2");
await p2.execute({ name: '%an%' });
```

Serverless: functions like AWS Lambda or Vercel Server Functions can live up to 15 minutes and reuse connections and prepared statements, if you declare them outside the handler:

```ts
const db = drizzle({ client: databaseConnection });
const prepared = db.select().from(users).prepare();
export const handler = async () => prepared.execute();
```

Edge functions tend to clean up straight after they are invoked, which leads to little to no performance benefit.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (perf-queries.mdx, perf-serverless.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
