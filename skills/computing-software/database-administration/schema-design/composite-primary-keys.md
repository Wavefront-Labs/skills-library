---
id: computing-software.database-administration.schema-design.composite-primary-keys
name: composite-primary-keys
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, composite-primary-key, compound-key, junction-tables, keys-normalisation, foreign-keys]
level: practitioner
status: verified
description: "Decide when a composite primary key fits (junction tables, weak entities, partitioned or multi-tenant tables), order its columns for queries, and handle FKs and ORMs."
sources:
  - https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-index-types.html
  - https://use-the-index-luke.com/sql/where-clause/the-equals-operator/concatenated-keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composite primary keys

## Good fits
- **Junction tables**: `PRIMARY KEY (user_id, role_id)` enforces "no duplicate assignment" with no extra id.
- **Weak entities** identified within a parent: `order_lines (order_id, line_no)`.
- **Multi-tenant**: `(tenant_id, id)` keeps tenant data clustered (InnoDB clusters on the PK) and makes every FK tenant-scoped, preventing cross-tenant references.
- **Partitioned tables**: PostgreSQL requires the partition key in every PK/UNIQUE constraint (`PRIMARY KEY (id)` on a table partitioned by `created_at` fails with "unique constraint on partitioned table must include all partitioning columns"): use `PRIMARY KEY (created_at, id)` or `(tenant_id, id)`.
- **Time series**: `(device_id, ts)`.

## Column order matters
The PK creates an index ordered by its columns. Put the column used alone in queries first:
```sql
CREATE TABLE user_roles (user_id bigint, role_id int, granted_at timestamptz,
  PRIMARY KEY (user_id, role_id));
CREATE INDEX ON user_roles (role_id);         -- for "who has role X" queries
```
The PK index serves `WHERE user_id = ?` and `WHERE user_id = ? AND role_id = ?`, not `WHERE role_id = ?`.

## Foreign keys referencing composites
```sql
CREATE TABLE line_discounts (
  order_id bigint, line_no int, discount_id int,
  PRIMARY KEY (order_id, line_no, discount_id),
  FOREIGN KEY (order_id, line_no) REFERENCES order_lines (order_id, line_no) ON DELETE CASCADE);
```
Child tables inherit all key columns: deep hierarchies get wide keys and wide indexes. If a composite-keyed table is referenced by many children, consider a surrogate key plus UNIQUE on the composite.

## Costs
- InnoDB: each secondary index record contains the primary key columns, so a long (wide composite) PK makes every secondary index larger (MySQL manual: "it is advantageous to have a short primary key"). Check SQL Server's clustered-index docs for the same effect there.
- ORMs: some handle composite keys poorly. Django added `CompositePrimaryKey` in 5.2 (earlier versions lack it); Rails 7.1 added composite primary key support and `query_constraints`; check your ORM's docs.
- URLs/APIs: exposing two-part identifiers is clumsier.

## Changing key values
Composite natural keys sometimes change (line renumbering); avoid using mutable values in keys, or use `ON UPDATE CASCADE` deliberately.

## Verify
Check plans for the main lookups use the PK index prefix; `pg_relation_size` of secondary indexes reasonable on clustered engines.
