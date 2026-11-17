---
id: computing-software.web-development.prisma.client-transaction-conflicts-retry
name: client-transaction-conflicts-retry
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-transaction-retry, prisma, p2034-write-conflict, serializable-retry, deadlock-retry]
level: advanced
status: docs-checked
description: "Prevent write conflicts and deadlocks between concurrent transactions with Serializable isolation and a retry loop on error code P2034."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/transactions.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Write conflicts and retries (P2034)

At `ReadCommitted` (default on PostgreSQL and SQL Server), concurrent transactions can conflict. The docs' example: transactions A and B both run `deleteMany` then `createMany`; B creates and commits first, then A creates rows that collide with B's, for instance by violating a unique constraint.

Fix in two parts:

1. Set `isolationLevel: Prisma.TransactionIsolationLevel.Serializable` on that transaction. It overrides the database default for that transaction only and makes concurrent transactions behave as if run serially. A transaction that loses a conflict or deadlock fails with error `P2034`.
2. Retry on `P2034`:

```ts
const MAX_RETRIES = 5;
let retries = 0;
while (retries < MAX_RETRIES) {
  try {
    result = await prisma.$transaction(
      [prisma.user.deleteMany({ where: {} }), prisma.post.createMany({ data })],
      { isolationLevel: Prisma.TransactionIsolationLevel.Serializable },
    );
    break;
  } catch (error) {
    if (error.code === "P2034") { retries++; continue; }
    throw error;
  }
}
```

Anything other than `P2034` is rethrown. The retry count of 5 is the docs' example value.

Not applicable to MongoDB (no isolation levels) or to CockroachDB and SQLite (they only offer Serializable, so the timing issue described does not arise).

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-client/queries/transactions pages, orm/v7): ReadCommitted conflict scenario, Serializable override per transaction, P2034 error, the retry loop with MAX_RETRIES 5, MongoDB/CockroachDB/SQLite exclusions.

Method: documentation only; no commands were run.
