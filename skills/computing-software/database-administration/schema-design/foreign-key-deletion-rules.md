---
id: computing-software.database-administration.schema-design.foreign-key-deletion-rules
name: foreign-key-deletion-rules
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, normalisation, on-delete-cascade, on-delete-restrict, set-null, referential-integrity, foreign-keys]
level: practitioner
status: verified
description: "Choose foreign key deletion rules per relationship (CASCADE, RESTRICT/NO ACTION, SET NULL, SET DEFAULT), avoid cascade surprises, and index child keys."
sources:
  - https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK
  - https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/tables/primary-and-foreign-key-constraints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Foreign key deletion rules

"Database Design for Mere Mortals" calls these relationship **deletion rules**: what happens to
child rows when a parent row is deleted. Decide per relationship from the business meaning.

| Rule | Effect | Use when |
|---|---|---|
| `RESTRICT` / `NO ACTION` (default) | delete fails while children exist | children have independent value (invoices of a customer, audit records) |
| `CASCADE` | children deleted too | children are **part of** the parent (order lines of an order, a post's attachments) |
| `SET NULL` | child FK set to NULL | optional association (ticket's assignee leaves; ticket stays) |
| `SET DEFAULT` | child FK set to column default | rare: a placeholder parent like "unassigned" |
`RESTRICT` vs `NO ACTION` in PostgreSQL: NO ACTION checks at end of statement (or at commit if the constraint is deferred), RESTRICT immediately and cannot be deferred (checked: a deferred NO ACTION FK let a parent and child be deleted in one transaction, a RESTRICT FK raised an error). In MySQL InnoDB they are equivalent and both reject immediately.

```sql
CREATE TABLE order_lines (
  order_id bigint NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id bigint NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
  ...
);
CREATE TABLE tickets (
  assignee_id bigint REFERENCES users(id) ON DELETE SET NULL
);
```
PostgreSQL 15+: `ON DELETE SET NULL (col)` limits which columns are nulled in a composite FK (checked: `FOREIGN KEY (a,b) REFERENCES pa ON DELETE SET NULL (b)` left `a` intact).

## Cascade surprises
- Chains: deleting one customer cascades to orders, then lines, then shipments... a single
  `DELETE` can remove millions of rows, hold locks for minutes and generate huge WAL/binlog.
  Delete large hierarchies in batches from the leaves up instead.
- Accidental deletes become catastrophic. For important data prefer RESTRICT plus explicit
  application deletes, or soft delete.
- MySQL: "Cascaded foreign key actions do not activate triggers" (MySQL manual).
- SQL Server restricts multiple cascade paths to the same table; check its docs and restructure or use triggers if it rejects your design.

## ON UPDATE
Primary keys should not change; with surrogate keys `ON UPDATE` rules rarely matter. With
natural keys that can change, `ON UPDATE CASCADE` propagates the new value.

## Index the child column
Every FK check on parent delete/update looks up children by the FK column. Without an index, each
parent delete scans the child table, and some engines take broader locks. MySQL InnoDB creates the index automatically ("created on the referencing table automatically if it does not exist"); PostgreSQL does not (checked: `pg_indexes` showed no index on the FK column). Check Oracle's and SQL Server's docs for their behaviour.

## Verify
In a test, delete a parent with children for each relationship and confirm the expected outcome
(error, cascade, null), and that EXPLAIN of the FK check uses an index on the child column.
