---
id: computing-software.database-administration.duckdb.duckdb-constraints
name: duckdb-constraints
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, constraints, primary-key, unique, foreign-key, check, not-null, art-index]
level: practitioner
status: docs-checked
description: "Declare CHECK, NOT NULL, PRIMARY KEY, UNIQUE and FOREIGN KEY constraints in DuckDB, with the error each raises and the ART index and performance cost."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/constraints.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enforce data rules at insert time in DuckDB tables.

Constraints are given in `CREATE TABLE` (see `duckdb-create-table`); some can be added later with `ALTER TABLE`, but not all. They slow loading and updates and speed up some queries.

```sql
-- CHECK: any Boolean expression; rows failing it are rejected
CREATE TABLE students (name VARCHAR CHECK (NOT contains(name, ' ')));
INSERT INTO students VALUES ('this name contains spaces');
-- Constraint Error: CHECK constraint failed on table students with expression CHECK((NOT contains("name", ' ')))

-- NOT NULL: columns are nullable by default
CREATE TABLE students (name VARCHAR NOT NULL);
INSERT INTO students VALUES (NULL);
-- Constraint Error: NOT NULL constraint failed: students.name

-- PRIMARY KEY (single or composite) and UNIQUE
CREATE TABLE students (id INTEGER PRIMARY KEY, name VARCHAR, email VARCHAR UNIQUE);
CREATE TABLE integers (i INTEGER, j INTEGER, k INTEGER, UNIQUE (i, j));
CREATE TABLE s2 (id INTEGER, name VARCHAR, PRIMARY KEY (id, name));
-- Constraint Error: Duplicate key "id: 1" violates primary key constraint
-- Constraint Error: Duplicate key "email: student1@uni.com" violates unique constraint.

-- FOREIGN KEY: must reference a primary key or unique column of another table
CREATE TABLE subjects (id INTEGER PRIMARY KEY, name VARCHAR);
CREATE TABLE exams (
    exam_id INTEGER PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects(id),
    student_id INTEGER REFERENCES students(id),
    grade INTEGER);
-- Constraint Error: Violates foreign key constraint because key "id: 2" does not exist in the referenced table
```

Rules:
- A table has at most one PRIMARY KEY but many UNIQUE constraints. A primary key also forbids NULL (inserting without the id fails with `NOT NULL constraint failed: students.id`).
- Each primary key, unique and foreign key constraint automatically creates an ART index.
- Index limitations can make a uniqueness check fire too eagerly (spurious `violates primary key constraint`); see `duckdb-insert-on-conflict-upsert` for ON CONFLICT handling and the indexes page for the limits.

## Checked

2026-11-07. Read the Constraints page in full and confirmed CHECK, NOT NULL, PRIMARY KEY (single and composite), UNIQUE and FOREIGN KEY examples with their quoted error texts, the one-primary-key rule, NULL handling, automatic ART indexes, the eager-evaluation index warning, the ALTER TABLE caveat and the performance warning. Removed the Verify step.

Method: documentation only; no commands were run.
