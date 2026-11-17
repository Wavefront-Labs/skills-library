---
id: computing-software.database-administration.sql.junction-tables-many-to-many
name: junction-tables-many-to-many
category: computing-software
field: database-administration
product: sql
tags: [sql, junction-tables-many-to-many]
level: intro
status: docs-checked
description: "Model many-to-many relationships with a junction table and composite key."
sources: ["https://www.postgresql.org/docs/current/ddl-constraints.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Many-to-many junction tables

- `CREATE TABLE student_course (student_id int REFERENCES student, course_id int REFERENCES course, PRIMARY KEY (student_id, course_id));` Without a column list, `REFERENCES` points at the referenced table's primary key. PostgreSQL documents this as how foreign keys implement many-to-many relationships; the primary key overlaps the foreign keys.
- The primary key creates a unique B-tree index on `(student_id, course_id)` and marks both columns `NOT NULL`. That serves lookups by `student_id`.
- A foreign key does not create an index on the referencing columns. Deleting or updating a referenced row scans the referencing table, so index the other direction too, for example `(course_id, student_id)`.
- Attributes of the relationship (grade, enrolled_at) live in the junction table.
- Prefer one junction row per pair over a comma-separated id column, so each pair can carry its own foreign keys and attributes.
- Self-check: inserting the same pair twice fails with a unique violation.

## Checked

2026-11-08. Confirmed on the PostgreSQL constraints page: composite primary keys, the `REFERENCES table` shorthand using the primary key, the many-to-many order_items example, the automatic unique index and `NOT NULL` of a primary key, and the advice to index referencing columns. Removed the generic SQLite syntax-index source, which does not cover the claims.
Method: documentation only; no commands were run.
