---
id: computing-software.database-administration.postgresql.inheritance-partitioning-and-constraint-exclusion
name: inheritance-partitioning-and-constraint-exclusion
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, table-inheritance, constraint-exclusion, legacy-partitioning, check-constraints, partition-migration]
level: practitioner
status: verified
description: "Maintain legacy PostgreSQL inheritance-based partitioning with CHECK constraints, triggers and constraint_exclusion, and migrate it to declarative partitioning."
sources:
  - https://www.postgresql.org/docs/current/ddl-partitioning.html#DDL-PARTITIONING-USING-INHERITANCE
  - https://www.postgresql.org/docs/current/ddl-inherit.html
  - https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-CONSTRAINT-EXCLUSION
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inheritance-based partitioning and constraint exclusion

Before PG10 partitioning was built from table inheritance. You will still meet it in old systems and in cases declarative partitioning does not allow (children with extra columns).

## Structure
```sql
CREATE TABLE measurements (id bigint, logdate date NOT NULL, value numeric);
CREATE TABLE measurements_2026_10 (CHECK (logdate >= '2026-10-01' AND logdate < '2026-11-01')) INHERITS (measurements);
CREATE INDEX ON measurements_2026_10 (logdate);
```
Routing inserts needs a trigger on the parent:
```sql
CREATE FUNCTION measurements_insert() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.logdate >= '2026-10-01' AND NEW.logdate < '2026-11-01' THEN INSERT INTO measurements_2026_10 VALUES (NEW.*);
  ELSE RAISE EXCEPTION 'no partition for %', NEW.logdate; END IF;
  RETURN NULL;
END $$;
CREATE TRIGGER measurements_ins BEFORE INSERT ON measurements FOR EACH ROW EXECUTE FUNCTION measurements_insert();
```

## Constraint exclusion
```sql
SHOW constraint_exclusion;   -- 'partition' (default): applied to inheritance children and UNION ALL subqueries
EXPLAIN SELECT * FROM measurements WHERE logdate = '2026-10-15';
```
The planner skips children whose CHECK contradicts the WHERE clause. Limits: works only with **constants at plan time** (not `now()`, not parameters in generic plans), simple comparisons, and every child is examined at planning, so hundreds of children make planning slow. Declarative partitioning uses partition pruning instead (works at execution time too).

## Gotchas specific to inheritance
- Indexes, unique constraints and foreign keys are per child; no global uniqueness.
- `UPDATE` that changes the partition key does not move the row; it violates the child's CHECK and errors.
- A plain `SELECT FROM measurements` always scans the parent table itself as well as the children that survive exclusion.
- `SELECT FROM ONLY measurements` reads the parent alone; forgetting `ONLY` in maintenance scripts touches all children.

## Migrating to declarative partitioning
1. Create the new partitioned table with identical columns.
2. For each child: `ALTER TABLE child NO INHERIT measurements;` then `ALTER TABLE measurements_new ATTACH PARTITION child FOR VALUES FROM (...) TO (...);` The existing CHECK constraint lets ATTACH skip the validation scan.
3. Drop the trigger and old parent, rename the new table, inside one transaction during a short lock window.
4. Fix views, grants, sequences ownership and foreign keys referencing the old parent.

## Checked
PostgreSQL 17.6: the trigger routes a 2026-10 row to the child and raises for an uncovered date; `constraint_exclusion` defaults to `partition`; a literal date excludes the other child; `= current_date` and a generic-plan parameter (`plan_cache_mode = force_generic_plan`) scan every child, a custom plan with a literal excludes; `UPDATE` moving a row out of its child's CHECK fails with `violates check constraint "measurements_2026_10_logdate_check"`; `NO INHERIT` then `ATTACH PARTITION` logs `partition constraint for table ... is implied by existing constraints` (no validation scan).
