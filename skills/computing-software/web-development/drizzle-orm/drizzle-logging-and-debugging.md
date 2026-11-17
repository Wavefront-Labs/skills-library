---
id: computing-software.web-development.drizzle-orm.drizzle-logging-and-debugging
name: drizzle-logging-and-debugging
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, logging, tosql, mock-driver, debugging]
level: intro
status: docs-checked
description: "Debug Drizzle queries: logger option, custom log writers, toSQL(), db.execute raw SQL, and drizzle.mock for tests without a database."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/goodies.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: see what Drizzle sends.

Logging: `drizzle(process.env.DB_URL, { logger: true })`. Redirect output with a `DefaultLogger` and a custom `LogWriter`:

```ts
import { DefaultLogger, type LogWriter } from "drizzle-orm/logger";
class MyLogWriter implements LogWriter { write(message: string) { /* file, stdout */ } }
const db = drizzle(url, { logger: new DefaultLogger({ writer: new MyLogWriter() }) });
```

Or a fully custom logger: `class MyLogger implements Logger { logQuery(query: string, params: unknown[]) { console.log({ query, params }); } }`.

Print generated SQL with `.toSQL()`, for example `db.select({ id: users.id, name: users.name }).from(users).groupBy(users.id).toSQL()`. A standalone `new QueryBuilder()` from `drizzle-orm/pg-core` builds queries without a db instance, and `.toSQL()` on it gives `{ sql, params }`.

Raw parametrized SQL: `await db.execute(sql`select * from ${users} where ${users.id} = ${userId}`)`.

Typed db object without a real PostgreSQL connection: `drizzle.mock({ relations })`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (goodies.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
