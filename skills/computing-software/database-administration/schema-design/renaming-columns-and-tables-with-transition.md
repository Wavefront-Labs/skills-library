---
id: computing-software.database-administration.schema-design.renaming-columns-and-tables-with-transition
name: renaming-columns-and-tables-with-transition
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, rename-column, rename-table, expand-contract, transition-period, schema-migrations]
level: practitioner
status: draft
description: "Rename a column or table in a live system without breaking deployed code: expand/contract with a transition period, views or synonyms, dual writes, and cleanup."
sources:
  - https://databaserefactoring.com/RenameColumn.html
  - https://databaserefactoring.com/RenameTable.html
  - https://www.postgresql.org/docs/current/sql-altertable.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Renaming a column or table with a transition period

`ALTER TABLE ... RENAME COLUMN` is instant, but every running application instance, report and ETL job using the old name breaks the moment it runs. Refactoring Databases (Ambler and Sadalage) prescribes a **transition period** where both names work.

## Column rename (expand/contract)
1. **Expand**: add the new column, keep both in sync.
```sql
ALTER TABLE customers ADD COLUMN family_name text;
UPDATE customers SET family_name = last_name WHERE family_name IS NULL;   -- batch on big tables
CREATE FUNCTION sync_family_name() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    NEW.family_name := coalesce(NEW.family_name, NEW.last_name);
    NEW.last_name   := coalesce(NEW.last_name, NEW.family_name);
  ELSIF NEW.family_name IS DISTINCT FROM OLD.family_name THEN
    NEW.last_name := NEW.family_name;
  ELSIF NEW.last_name IS DISTINCT FROM OLD.last_name THEN
    NEW.family_name := NEW.last_name;
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER customers_sync BEFORE INSERT OR UPDATE ON customers FOR EACH ROW EXECUTE FUNCTION sync_family_name();
```
2. **Migrate consumers**: deploy code reading/writing `family_name`; update reports and ETL.
3. **Contract** (after the agreed transition, e.g. two releases or a date): drop trigger, function and `last_name`.

## Table rename
1. `ALTER TABLE cust RENAME TO customers;`
2. Create a compatibility view in the same step: `CREATE VIEW cust AS SELECT * FROM customers;` (simple views are updatable in PostgreSQL, MySQL, SQL Server). Oracle/SQL Server synonyms (`CREATE SYNONYM cust FOR customers`) also work.
3. Remove the view after the transition period, once query logs or `pg_stat_statements` show no statements still referencing the old name.

## Shortcut for small teams
If one application owns the database and deploys atomically with migrations, a plain rename plus coordinated deploy (stop old instances first) is acceptable. Rolling deployments with old and new code running together need the transition period.

## ORMs
ORM attribute renames can map a new code name to the old column (`db_column`, `@Column(name=...)`) as a zero-DDL first step.

## Verify
During the transition, writes through either name are visible through the other (test inserts and updates); before contract, query logs show no remaining use of the old name.
