---
id: computing-software.web-development.prisma.client-interactive-transactions
name: client-interactive-transactions
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-interactive-transactions, prisma, transaction-timeout-maxwait, isolation-level-option, promise-all-in-transaction]
level: practitioner
status: docs-checked
description: "Run interactive transactions with the tx client, tune maxWait (2000 ms) and timeout (5000 ms), set isolationLevel, and avoid Promise.all inside them."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/transactions.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Interactive transactions

Pass an async function; the argument is a transaction-bound client. Everything called on `tx` commits together; a thrown error rolls back automatically.

```ts
await prisma.$transaction(async (tx) => {
  const sender = await tx.account.update({
    data: { balance: { decrement: 100 } },
    where: { email: "alice@prisma.io" },
  });
  if (sender.balance < 0) throw new Error("Insufficient funds");
  return tx.account.update({
    data: { balance: { increment: 100 } },
    where: { email: "bob@prisma.io" },
  });
});
```

Options (second argument):
- `maxWait`: longest wait to get a transaction, default 2000 ms.
- `timeout`: longest transaction run time, default 5000 ms.
- `isolationLevel`: for example `Prisma.TransactionIsolationLevel.Serializable`; default is whatever the database is configured with.

Keep them short. Docs warn that long transactions hurt performance and can deadlock; avoid network calls and slow queries inside.

`Promise.all` inside a `$transaction` does not parallelise: a transaction owns one connection, a connection runs one query at a time, so the queries run one after another.

Supported isolation levels (when the database has them): `ReadUncommitted`, `ReadCommitted`, `RepeatableRead`, `Snapshot`, `Serializable`. Not available on MongoDB.

| Database | Levels supported | Default |
| --- | --- | --- |
| PostgreSQL | all but Snapshot | ReadCommitted |
| MySQL | all but Snapshot | RepeatableRead |
| SQL Server | all five | ReadCommitted |
| CockroachDB | Serializable only | Serializable |
| SQLite | Serializable only | Serializable |

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-client/queries/transactions pages, orm/v7): maxWait 2000 ms and timeout 5000 ms defaults, isolationLevel option, Promise.all serialising queries, the isolation-level support and default tables, MongoDB exclusion, the keep-transactions-short warning.

Method: documentation only; no commands were run.
