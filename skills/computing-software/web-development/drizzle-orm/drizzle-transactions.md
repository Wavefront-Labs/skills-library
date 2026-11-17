---
id: computing-software.web-development.drizzle-orm.drizzle-transactions
name: drizzle-transactions
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, transactions, savepoints, rollback, isolation-level]
level: practitioner
status: docs-checked
description: "Run Drizzle transactions with db.transaction: commit, tx.rollback(), nested savepoints, return values and PostgreSQL isolation settings."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/transactions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: group statements atomically.

A SQL transaction groups statements that commit as one logical unit or roll back as one:

```ts
await db.transaction(async (tx) => {
  await tx.update(accounts).set({ balance: sql`${accounts.balance} - 100.00` }).where(eq(users.name, 'Dan'));
  await tx.update(accounts).set({ balance: sql`${accounts.balance} + 100.00` }).where(eq(users.name, 'Andrew'));
});
```

- Rollback on a business rule: `tx.rollback()` throws an exception that rolls back the transaction (the docs call it after checking `account.balance < 100`).
- Return values: `const newBalance: number = await db.transaction(async (tx) => { ...; return account.balance; })`.
- Savepoints: Drizzle supports them through the nested transaction API, `await tx.transaction(async (tx2) => {...})`.
- Relational queries work inside: `tx.query.users.findMany({ with: { accounts: true } })`.
- Dialect-specific configuration is the second argument; for PostgreSQL:

```ts
await db.transaction(async (tx) => { /* ... */ }, {
  isolationLevel: "read committed",   // read uncommitted | read committed | repeatable read | serializable
  accessMode: "read write",           // read only | read write
  deferrable: true,
});
```

The page types this as `PgTransactionConfig { isolationLevel?; accessMode?; deferrable?: boolean }`.

## Checked

Date: 2026-11-07

Confirmed against `pg/transactions.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 101 lines): the basic transaction, savepoints, `tx.rollback()`, returned values, relational queries inside a transaction, and the `PgTransactionConfig` options and values.

Removed: the claims that any thrown error rolls back and that using `db` inside the callback escapes the transaction (neither stated), the invented account columns in the example (replaced with the page's example), the pointer to the batch API and the invented Verify step.

Method: documentation only; no commands were run.
