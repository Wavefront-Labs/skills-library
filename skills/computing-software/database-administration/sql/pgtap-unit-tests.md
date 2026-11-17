---
id: computing-software.database-administration.sql.pgtap-unit-tests
name: pgtap-unit-tests
category: computing-software
field: database-administration
product: sql
tags: [sql, pgtap-unit-tests]
level: advanced
status: docs-checked
description: "Write pgTAP tests for schemas and functions and run them with pg_prove."
sources: ["https://pgtap.org/documentation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pgTAP database unit tests

- Enable per database as a superuser: `CREATE EXTENSION IF NOT EXISTS pgtap;`. On Debian-family systems the package is `pgtap`; otherwise build it from PGXN with make, make install and make installcheck.
- Test file: `BEGIN; SELECT plan(3); SELECT has_table('orders'); SELECT col_not_null('orders','cid'); SELECT is((SELECT count(*) FROM orders), 0::bigint, 'empty'); SELECT * FROM finish(); ROLLBACK;`
- `plan(n)` declares the count (avoid `no_plan()`); `finish()` reports, and `finish(true)` raises an exception if any test failed. `is(have, want, description)` is preferred over `ok()` because it reports both values on failure.
- `has_table` does not recognise foreign tables (use `has_foreign_table`). `col_not_null` fails with a diagnostic if the table or column is missing, so call `has_column` first.
- Run: `pg_prove -U postgres sql/*.sql`, or `pg_prove -d myapp --runtests` for xUnit-style test functions.
- Wrapping the script in BEGIN and ROLLBACK discards test changes so the database stays clean. Installing only on test databases is sensible practice, not stated by the page.
- Self-check: break a column and confirm the test fails.

## Checked

Date: 2026-11-08

Method: Read the first two-thirds of the pgTAP documentation page (installation, test-script structure, pg_prove, has_table, col_not_null) via WebFetch; the final third was not read, so claims rest only on the parts read.
