---
id: computing-software.web-development.bun.sql-transactions-fragments
name: sql-transactions-fragments
category: computing-software
field: web-development
product: bun
tags: [sql-transactions, sql-fragments, sql-savepoint, sql-unsafe]
level: advanced
status: docs-checked
description: "Write transactions, savepoints and dynamic SQL fragments with Bun.SQL: bulk insert, partial update, IN lists, identifiers, and when unsafe or file queries are safe."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/sql.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
await sql.begin(async tx => {
  await tx`INSERT INTO users (name) VALUES (${"Alice"})`;
  await tx.savepoint(async sp => {
    await sp`UPDATE accounts SET balance = balance - 100`;
  });
});

await sql`INSERT INTO users ${sql(user)}`;                          // all keys
await sql`UPDATE users SET ${sql(user, "name", "email")} WHERE id = ${user.id}`;
await sql`INSERT INTO users ${sql(rows)}`;                          // bulk insert
await sql`SELECT * FROM ${sql("public.users")}`;                    // quoted identifier
await sql`SELECT * FROM users WHERE id IN ${sql([1, 2, 3])}`;
```

Rules:
- `begin` sends BEGIN, COMMITs on success, ROLLBACKs and rejects on error. Returning an array of queries pipelines them.
- `tx.savepoint(fn)` rolls back to its checkpoint on error. Run sibling savepoints in sequence, not `Promise.all`.
- Queries on `tx` after it ends reject. Distributed: `beginDistributed(id, fn)`, `commitDistributed(id)`, `rollbackDistributed(id)`.

Gotchas:
- Manual `BEGIN` on a multi-connection pool raises an unsafe-transaction error; use `sql.begin`.
- `sql.unsafe(text, params)` and `sql.file(path, params)` use the database's own placeholders (`$1`, `?`) and do not escape input.
- `sql.array(values, type?)` is PostgreSQL only; `sql.simple()` runs multiple statements but takes no parameters.
- Do not mutate parameter buffers before awaiting.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/sql (relevant sections): sql.begin commit and rollback, pipelining by returning an array of queries, savepoint rollback and sibling savepoints in sequence, beginDistributed/commitDistributed/rollbackDistributed, queries on tx after it ends rejecting, ERR_POSTGRES_UNSAFE_TRANSACTION for manual BEGIN on a multi-connection pool, sql(obj) insert/update helpers, sql(array) bulk insert, sql(identifier) quoting, IN list helper, sql.unsafe and sql.file database-native placeholders, sql.array being PostgreSQL only, .simple() taking no parameters, and the note that parameters are read when the query is sent. Nothing removed.
Method: documentation only; no commands were run.
