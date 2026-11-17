---
id: computing-software.database-administration.supabase.database-testing-pgtap
name: database-testing-pgtap
category: computing-software
field: database-administration
product: supabase
tags: [testing, pgtap, supabase-test-db, rls-tests, ci]
level: practitioner
status: docs-checked
description: "Test a Supabase database with pgTAP and supabase test db: transactional tests, role and claims setup for RLS, coverage guidance and CI."
sources:
  - https://supabase.com/docs/guides/local-development/testing/overview
  - https://supabase.com/docs/guides/database/postgres/row-level-security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: unit test schema, RLS policies and functions in Postgres.

pgTAP is a unit testing framework for Postgres. It can test structure, RLS policies, functions and procedures, and data integrity. Run with `supabase test db` (start the stack first with `supabase start`).

Practice:
- Wrap each test in begin and rollback so it is isolated and fast.
- Test create, read, update and delete.
- Cover anonymous and authenticated users.
- Include negative cases: actions users must be blocked from.
- Test edge cases and possible security bypasses.

Impersonating users in tests: `set local role authenticated;` and `set local "request.jwt.claims"` to set the role and JWT claims. If RLS tests fail, check that both are set and that policy definitions match the test's assumptions.

Assertion patterns from the RLS guide:
- Assert missing-grant and `with check` denials with `throws_ok` (`42501`).
- A `using` denial raises no error and matches zero rows; assert it with `is_empty` and `returning`, then confirm the row is intact.
- Never prove an allowed write with `lives_ok`, since it passes on zero matched rows; use `returning` and assert the value.

CI: run migrations before tests and run tests on every pull request (the page's workflow file is `.github/workflows/db-tests.yml`: checkout, `supabase/setup-cli`, `supabase start`, `supabase test db`).

## Checked

2026-11-04: Read the Testing Overview page in full, and the RLS guide's pgTAP assertion table (rows for missing grant, `with check`, `using` and the `lives_ok` warning). All claims confirmed; nothing removed.
Method: documentation only; no commands were run.
