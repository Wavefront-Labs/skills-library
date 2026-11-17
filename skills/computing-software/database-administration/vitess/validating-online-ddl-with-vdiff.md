---
id: computing-software.database-administration.vitess.validating-online-ddl-with-vdiff
name: validating-online-ddl-with-vdiff
category: computing-software
field: database-administration
product: vitess
tags: [online-ddl, vdiff, validation, postpone-completion, ready-to-complete]
level: advanced
status: docs-checked
description: "Validate an in-flight Vitess online migration with VDiff: needs --postpone-completion, ready_to_complete 1, and the migration UUID as workflow name."
sources:
  - https://vitess.io/docs/25.0/user-guides/schema-changes/validating-migrations/
  - https://vitess.io/docs/25.0/user-guides/schema-changes/postponed-migrations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A vitess-strategy migration is itself a VReplication workflow, so VDiff can check that the shadow table and the original are in sync. Constraints and steps from the page:

1. VDiff works only on migrations created with `--postpone-completion`. Start one, for example:

```
vtctldclient ApplySchema --ddl-strategy vitess --postpone-completion --sql "alter table t1 add column extra1 int not null default 0" customer
```

This returns the migration UUID.
2. Confirm `ready_to_complete` is `1` in `show vitess_migrations like '<uuid>'`. Run VDiff only once it is.
3. Create the VDiff using the migration UUID as the workflow name:

```
vtctldclient VDiff --target-keyspace customer --workflow <uuid> Create
```

4. Monitor with the VDiff show action; expect `State: completed`, a RowsCompared count and `HasMismatch: false`. A mismatch would indicate a Vitess bug, which the page asks you to report on Slack or GitHub.
5. Then release the migration with `alter vitess_migration '<uuid>' complete`, as described on the Postponed Migrations page.

The target keyspace for VDiff is the keyspace the table lives in (customer in the example).

## Checked

2026-11-08. Read in full: Validating schema migrations using VDiff page and Postponed migrations page (vitess.io docs 25.0, via the website repo markdown). Confirmed: VDiff only on --postpone-completion migrations, ready_to_complete 1, workflow name equal to the migration UUID, the commands and expected output (Validating page); the complete statement (Postponed page). Fixed: step 5 is now sourced rather than inferred.

Method: documentation only; no commands were run.
