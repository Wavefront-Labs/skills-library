---
id: computing-software.database-administration.vitess.declarative-online-ddl
name: declarative-online-ddl
category: computing-software
field: database-administration
product: vitess
tags: [online-ddl, declarative, idempotent, create-table, schema-as-code, ddl-strategy]
level: practitioner
status: docs-checked
description: "Use --declarative migrations to state a desired table schema with CREATE or DROP and let Vitess infer an ALTER, with idempotency and revert rules."
sources:
  - https://vitess.io/docs/25.0/user-guides/schema-changes/declarative-migrations/
  - https://vitess.io/docs/25.0/user-guides/schema-changes/postponed-migrations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In a declarative migration you supply the end state: a full `CREATE TABLE` (create it, or alter it to match) or a `DROP TABLE` (make it go). `ALTER` statements are not allowed. The operations are idempotent: submitting the same CREATE twice makes the second a successful no-op, and likewise for DROP.

Enable with the `--declarative` flag on an online strategy, for example:

```sql
set @@ddl_strategy='vitess --declarative';
create table decl_table(id int primary key);
create table decl_table(id int primary key, ts timestamp not null);
```

The second statement is a CREATE but the migration's `ddl_action` shows `alter`, and `message` lists the ALTER options. It can be combined with other flags, for example `vitess --declarative --allow-concurrent --postpone-completion`.

At execution time the scheduler may rewrite the migration:
- `REVERT`: normal revert.
- `ALTER`: rejected, the migration fails.
- `DROP`: successful no-op if the table does not exist, otherwise a normal DROP.
- `CREATE`: normal CREATE if the table is absent; if present, compute a diff, no diff is a successful no-op, a diff becomes an `ALTER` run by the chosen strategy.

Declarative migrations are revertible, but one that turned into an ALTER is revertible only in the `vitess` strategy; a no-op implies a no-op revert. A declarative migration combined with `--postpone-completion` stays `queued` until `ALTER VITESS_MIGRATION ... COMPLETE`, and is only evaluated when scheduled to run.

## Checked

2026-11-08. Read in full: Declarative migrations and Postponed migrations pages (vitess.io docs 25.0, via the website repo markdown). Confirmed: semantics, idempotency, the example and ddl_action alter, flag combination, rewrite rules and revert notes (Declarative page); a declarative migration stays queued with the postpone flag until complete (Postponed page). Removed the unread DDL Strategy Flags citation.

Method: documentation only; no commands were run.
