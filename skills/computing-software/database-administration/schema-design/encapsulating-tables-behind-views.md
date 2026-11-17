---
id: computing-software.database-administration.schema-design.encapsulating-tables-behind-views
name: encapsulating-tables-behind-views
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, encapsulate-table-with-view, views, database-refactoring, api-layer, schema-migrations]
level: practitioner
status: verified
description: "Encapsulate tables behind views so applications depend on a stable interface while the physical schema is refactored, including updatable views and permissions."
sources:
  - https://databaserefactoring.com/EncapsulateTableWithView.html
  - https://www.postgresql.org/docs/current/sql-createview.html
  - https://www.postgresql.org/docs/current/rules-views.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encapsulating tables behind views during refactoring

**Goal:** applications (and reports) query a view that presents the expected shape; the DBA can rename, split or merge underlying tables while the view keeps the contract.

## Pattern
```sql
CREATE SCHEMA api;
ALTER TABLE customers SET SCHEMA core;
CREATE VIEW api.customers AS
SELECT id, given_name AS first_name, family_name AS last_name, email
FROM core.customers;
GRANT SELECT, INSERT, UPDATE, DELETE ON api.customers TO app_role;
REVOKE ALL ON core.customers FROM app_role;
ALTER ROLE app_role SET search_path = api;
```
Later, splitting `core.customers` into two tables only requires redefining the view (join), not changing the app.

## Updatable views
- Simple single-table views without aggregates/DISTINCT/GROUP BY are automatically updatable in PostgreSQL (9.3+; the insert and update through `api.customers` above was run on 18). Other engines have their own rules: check their docs.
- `WITH CHECK OPTION` prevents writes that would fall outside the view's WHERE.
- Multi-table views need `INSTEAD OF` triggers (or rules) in PostgreSQL to route writes (9.3 release notes).
```sql
CREATE VIEW api.customers_v AS SELECT ... FROM core.customers c JOIN core.customer_profiles p USING (customer_id);
CREATE TRIGGER customers_v_upd INSTEAD OF UPDATE ON api.customers_v FOR EACH ROW EXECUTE FUNCTION api.customers_v_update();
```

## Performance
Views are inlined by the optimiser; a plain projection costs nothing. Watch views that join tables the query does not need (join elimination works only with FK/unique guarantees) and views stacked on views.

## Security bonus
Views limit columns (hide PII) and rows. PostgreSQL views run with owner privileges by default; use `security_invoker = true` (15+) when row-level security of the caller must apply.

## Gotchas
- `SELECT *` in a view freezes the column list at creation; adding columns to the table does not appear until the view is recreated (checked).
- Dependencies block `ALTER TABLE ... ALTER COLUMN TYPE` on referenced columns (PostgreSQL: "cannot alter type of a column used by a view or rule"); drop/recreate views in the migration.
- ORMs may need primary key hints for views.

## Verify
Application test suite passes against the view after each physical refactoring step; `pg_depend` (PostgreSQL) shows applications' objects depend only on the api schema.
