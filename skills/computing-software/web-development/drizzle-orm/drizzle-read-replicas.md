---
id: computing-software.web-development.drizzle-orm.drizzle-read-replicas
name: drizzle-read-replicas
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, read-replicas, withreplicas, scaling, postgres]
level: advanced
status: docs-checked
description: "Route reads to replicas and writes to the primary with withReplicas, force primary reads with $primary, and add weighted replica selection."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/read-replicas.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: scale reads without changing call sites.

```ts
import { withReplicas } from 'drizzle-orm/pg-core';
const primaryDb = drizzle("postgres://user:password@host:port/primary_db");
const read1 = drizzle("postgres://user:password@host:port/read_replica_1");
const read2 = drizzle("postgres://user:password@host:port/read_replica_2");
const db = withReplicas(primaryDb, [read1, read2]);
```

Use `db` as before: Drizzle chooses between a read replica and the primary automatically. Selects go to either the `read1` or `read2` connection; create, update and delete operations go to the primary (the docs show a delete).

Force the primary for a read: `await db.$primary.select().from(usersTable)`.

Custom selection logic is a third argument that receives the replica array and returns one replica. The docs' example gives the first replica a 70% chance and the second 30%, and note that you can implement any kind of random selection:

```ts
const db = withReplicas(primaryDb, [read1, read2], (replicas) => {
  const weight = [0.7, 0.3];
  let cumulative = 0; const rand = Math.random();
  for (const [i, replica] of replicas.entries()) {
    cumulative += weight[i]!;
    if (rand < cumulative) return replica;
  }
  return replicas[0]!;
});
```

Keep real connection strings in your environment; the page uses placeholder URLs.

## Checked

Date: 2026-11-07

Confirmed against `pg/read-replicas.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 67 lines): `withReplicas` import from `drizzle-orm/pg-core`, the setup, automatic routing, the delete-on-primary example, `$primary`, and the weighted selection function.

Removed: the claim that the default choice is random when no function is given and that replicas lag the primary (neither stated), and the invented Verify step.

Method: documentation only; no commands were run.
