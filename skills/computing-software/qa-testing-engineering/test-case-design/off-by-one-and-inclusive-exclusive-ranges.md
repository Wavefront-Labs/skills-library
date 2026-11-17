---
id: computing-software.qa-testing-engineering.test-case-design.off-by-one-and-inclusive-exclusive-ranges
name: off-by-one-and-inclusive-exclusive-ranges
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [off-by-one, inclusive-exclusive-ranges, boundary-value-analysis, sql-ranges, code-review]
level: practitioner
status: docs-checked
description: "Find off-by-one defects in code and SQL: inclusive vs exclusive ranges, BETWEEN with timestamps, slicing, loop bounds, pagination and date-range queries."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.postgresql.org/docs/current/functions-comparison.html
  - https://www.postgresql.org/docs/current/rangetypes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding off-by-one defects in code and SQL ranges

**Goal:** catch the most common boundary defect class, in tests and in review.

## Where they live
| Construct | Trap |
|---|---|
| `if x > limit` vs `>=` | spec "up to and including" |
| Loops `for i in range(1, n)` | skips n, or `<= len` overruns |
| Slices `s[0:n]` | check whether the end index is inclusive or exclusive in your language |
| SQL `BETWEEN a AND b` | inclusive both ends; with timestamps `BETWEEN '2024-01-01' AND '2024-01-31'` misses everything after 00:00 on the 31st |
| Date ranges | "end date" stored as midnight vs end of day; time zones shift the day |
| Pagination | `OFFSET page*size` vs `(page-1)*size`; last page empty or duplicated row |
| Counting fence posts | 10 m fence with posts every 1 m needs 11 posts |
| Array index from 1 vs 0 | check the indexing base of each language or API |

## SQL date ranges done right
```sql
-- half-open interval: include the whole of January
WHERE created_at >= '2024-01-01' AND created_at < '2024-02-01'
```
PostgreSQL range types make the convention explicit: `tstzrange(a, b, '[)')`.

## Tests that expose them
- Three-value BVA around each boundary (n-1, n, n+1).
- For date filters: records at 00:00:00, 23:59:59.999, and the next day's 00:00:00 in the zone of the user and of the DB.
- Pagination: total = page_size x k exactly and k +/- 1; walk all pages and assert no duplicates/missing IDs.
- Empty collection, single element, full capacity.

## Review checklist
Every comparison operator against a limit cites the spec's inclusive/exclusive wording; every range in an API documents its convention (prefer half-open `[start, end)`).

## Gotchas
- A test with value n alone passes for both `>` and `>=` mistakes in some cases; use n-1, n, n+1.
- Inclusive end dates in UIs usually need conversion to exclusive in queries.

## Verify
Range tests include both sides of every boundary, and date-range queries use half-open intervals.

## Checked

2026-10-28 Confirmed against: PostgreSQL docs (BETWEEN is inclusive of the endpoints; range types with inclusive and exclusive bounds, `tstzrange`, `'[)'`). The fence-post and BVA arithmetic is derived, not sourced. Removed or generalised: language-specific slicing and indexing claims (Python/JS/Lua/SQL SUBSTRING; not in the fetched pages).

Method: documentation only; no commands were run.
