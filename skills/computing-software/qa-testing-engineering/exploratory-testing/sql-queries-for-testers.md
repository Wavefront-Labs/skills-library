---
id: computing-software.qa-testing-engineering.exploratory-testing.sql-queries-for-testers
name: sql-queries-for-testers
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [sql-for-testers, sql, database-testing, test-oracle, bug-investigation]
level: practitioner
status: draft
description: "Query the database to confirm application state: read-only access, finding records, joins, aggregates for reconciliation, timestamps and safe practices for testers."
sources:
  - https://www.postgresql.org/docs/current/tutorial-sql.html
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SQL for testers: querying the database to confirm state

**Goal:** verify what the application really stored, rather than trusting the UI, and gather precise evidence for bugs.

## Safety first
- Use a **read-only** account; never run UPDATE/DELETE on shared environments without agreement.
- Always add `LIMIT` when exploring big tables; avoid unindexed full scans on production replicas during business hours.
- Production data access only if approved, and never copy personal data into bug reports.

## Core queries
```sql
-- Find the record created by the test
SELECT * FROM orders WHERE customer_email = 'qa+1234@example.com' ORDER BY created_at DESC LIMIT 5;

-- Join to verify related data
SELECT o.id, o.status, oi.sku, oi.qty, oi.price
FROM orders o JOIN order_items oi ON oi.order_id = o.id
WHERE o.id = 98123;

-- Orphans (children without parent)
SELECT oi.* FROM order_items oi LEFT JOIN orders o ON o.id = oi.order_id WHERE o.id IS NULL;

-- Duplicates
SELECT client_ref, COUNT(*) FROM payments GROUP BY client_ref HAVING COUNT(*) > 1;

-- Reconcile a report total
SELECT date_trunc('day', created_at AT TIME ZONE 'UTC') d, SUM(total) FROM orders
WHERE created_at >= '2026-10-01' AND created_at < '2026-11-01' GROUP BY 1 ORDER BY 1;
```

## Things to check
- Values exactly as entered (trailing spaces, case, unicode), correct types and precision.
- Timestamps in UTC vs local; `updated_at` changed on update; audit/history rows written.
- Soft-delete flags vs actual deletes; status transitions recorded.
- NULL vs empty string (`WHERE col IS NULL` vs `= ''`).

## Evidence
Paste the query and result (masked) into the bug so developers can rerun it.

## Verify
For each tested write operation, a query confirms the stored values, related rows and audit fields, and bug reports include the query used.
