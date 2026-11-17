---
id: computing-software.database-administration.schema-design.relationship-types-and-junction-tables
name: relationship-types-and-junction-tables
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, normalisation, primary-key, junction-table, many-to-many, one-to-one, cardinality]
level: practitioner
status: draft
description: "Model one-to-one, one-to-many and many-to-many relationships correctly: where the foreign key goes, junction tables with their own attributes, keys and indexes."
sources:
  - https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK
  - https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Relationship types and junction tables

## One-to-many
FK on the "many" side:
```sql
CREATE TABLE customers (id bigint PRIMARY KEY, name text NOT NULL);
CREATE TABLE orders (
  id bigint PRIMARY KEY,
  customer_id bigint NOT NULL REFERENCES customers(id),   -- NOT NULL = every order has a customer (mandatory participation)
  placed_at timestamptz NOT NULL
);
CREATE INDEX ON orders (customer_id);
```
Nullable FK = optional participation.

## One-to-one
FK with a UNIQUE constraint, usually on the dependent/optional side, or share the primary key:
```sql
CREATE TABLE user_profiles (
  user_id bigint PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,   -- PK = FK enforces 1:1
  bio text, avatar_url text
);
```
Reasons to split 1:1: optional rarely-used columns, different access/security, very wide rows.
Otherwise keep the columns in one table.

## Many-to-many: junction (associative) table
```sql
CREATE TABLE students (id bigint PRIMARY KEY, ...);
CREATE TABLE courses  (id bigint PRIMARY KEY, ...);
CREATE TABLE enrollments (
  student_id bigint NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  course_id  bigint NOT NULL REFERENCES courses(id)  ON DELETE RESTRICT,
  enrolled_at timestamptz NOT NULL DEFAULT now(),
  grade text,
  PRIMARY KEY (student_id, course_id)
);
CREATE INDEX ON enrollments (course_id, student_id);   -- the PK covers lookups by student; this covers by course
```
- The composite PK prevents duplicates and serves one direction; add the reverse index for the other.
- Attributes of the relationship itself (enrolled_at, grade, role, quantity) belong on the
  junction table. Once it has a life of its own (e.g. it is referenced by other tables), consider
  a surrogate `id` PK plus a UNIQUE (student_id, course_id).
- If the same pair can legitimately occur multiple times (repeat enrollments per term), include
  the distinguishing column (`term`) in the key.

## Anti-patterns
- Comma-separated ids in a column ("jaywalking") instead of a junction table.
- `tag1, tag2, tag3` columns (multicolumn attributes).
- Arrays/JSON of ids without FK integrity, unless deliberately trading integrity for read speed.

## Self-referencing and hierarchies
`employees.manager_id REFERENCES employees(id)` is a one-to-many on the same table; many-to-many
on the same table (friendships) uses a junction with two FKs to the same table and a
`CHECK (user_a < user_b)` to avoid duplicates in symmetric relationships.

## Verify
Every relationship in the ER model maps to a FK (with NOT NULL/UNIQUE expressing cardinality),
duplicate pairs are rejected by the junction PK, and both lookup directions use an index.
