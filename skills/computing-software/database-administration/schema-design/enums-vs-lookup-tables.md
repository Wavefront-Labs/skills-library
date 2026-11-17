---
id: computing-software.database-administration.schema-design.enums-vs-lookup-tables
name: enums-vs-lookup-tables
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, data-type-selection, enum-vs-lookup-table, enum-type, check-constraint, reference-table, status-codes, alter-type-add-value]
level: practitioner
status: verified
description: "Choose between native ENUM types, CHECK-constrained text and lookup (reference) tables for status-like columns, weighing change cost, metadata, ordering and portability."
sources:
  - https://www.postgresql.org/docs/current/datatype-enum.html
  - https://dev.mysql.com/doc/refman/8.4/en/enum.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enums vs lookup tables

**Goal:** a constrained set of values (order status, country, plan tier) that is
valid, cheap to evolve, and self-describing.

## Options
| Option | Validity | Adding a value | Removing/renaming | Extra metadata | Portability |
|---|---|---|---|---|---|
| Native ENUM (PostgreSQL `CREATE TYPE`, MySQL `ENUM(...)`) | yes | PG: `ALTER TYPE ... ADD VALUE`; MySQL: ALTER TABLE (check the Online DDL docs for when it is instant) | PG: rename only (`RENAME VALUE`); `DROP VALUE` fails with "dropping an enum value is not implemented", so remove = recreate type | no | low |
| text/varchar + CHECK (`status IN ('new','paid','shipped')`) | yes | drop/re-add constraint (`NOT VALID` + `VALIDATE` in PG) | same | no | high |
| Lookup table + FK (`order_status(code PK, label, sort_order, is_terminal)`) | yes | INSERT a row | UPDATE/soft-retire a row | yes (labels, ordering, flags, i18n) | high |
| Plain text, no constraint | no | free | free | no | high |

## Guidance
- **Stable, small, purely technical sets** (e.g. `direction: in/out`): enum or CHECK.
- **Business-owned sets that change** or need attributes (display name, sort order,
  "is final state", per-tenant values): lookup table. The FK also documents meaning.
- Use the code (`'paid'`) as the lookup table PK rather than a surrogate int:
  readable rows, no join needed for most queries.
- Avoid MySQL ENUM ordering surprises: it sorts by index position, not by text (`'b'` before `'a'` for `ENUM('b','a')`), and stores invalid values as `''` (numeric 0) unless strict SQL mode is on (MySQL manual).

## PostgreSQL enum specifics
- `ALTER TYPE status ADD VALUE 'refunded' AFTER 'paid';` can run in a transaction block from PG12 (earlier it could not unless the type was created in the same transaction), but the new value can't be used until that transaction commits (PG12 release notes; `unsafe use of new value` error reproduced on 18, including when a later statement in the same implicit transaction uses it).
- Comparisons follow declaration order (`'new' < 'paid'`), handy for workflow stages.
- PostgreSQL enums are 4 bytes (`pg_column_size` returned 4); text codes with a FK are small too: storage is rarely the deciding factor.

## Gotchas
- ORMs map enums differently; a DB-level enum change may need an app deploy in lockstep.
- Removing a value used by historical rows breaks history: retire it (flag in the lookup table) instead.

## Verify
Inserting an invalid value fails at the database (not only in app validation);
adding a value is a documented, tested migration.
