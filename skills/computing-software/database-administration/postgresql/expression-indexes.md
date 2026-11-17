---
id: computing-software.database-administration.postgresql.expression-indexes
name: expression-indexes
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-index-types, expression-index, functional-index, lower-email, immutable-function, case-insensitive-search, citext]
level: practitioner
status: verified
description: "Index computed values in PostgreSQL (lower(email), date_trunc, jsonb keys) so queries on expressions use an index, and avoid the immutability and matching traps."
sources:
  - https://www.postgresql.org/docs/current/indexes-expressional.html
  - https://www.postgresql.org/docs/current/xfunc-volatility.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expression indexes

**Goal:** `WHERE lower(email) = $1` or `WHERE (payload->>'customer_id') = $1`
becomes an index scan.

## Create
```sql
CREATE UNIQUE INDEX users_email_lower_uq ON users (lower(email));   -- also enforces case-insensitive uniqueness
CREATE INDEX ON events ((payload->>'customer_id'));                  -- note the extra parentheses
CREATE INDEX ON orders ((created_at::date));                         -- only if created_at is timestamp (not timestamptz)
```
After creating, run `ANALYZE` on the table: PostgreSQL gathers statistics on the
expression itself, which also fixes bad row estimates for that expression.

## The query must match the expression exactly
```sql
WHERE lower(email) = lower($1)        -- uses users_email_lower_uq
WHERE email ILIKE $1                  -- does not
WHERE upper(email) = ...              -- does not
```
Make the app (or a view) use the same expression text.

## Immutability requirement
Index expressions must be `IMMUTABLE`. Common failures:
- `created_at::date` on `timestamptz` depends on the TimeZone setting:
  `functions in index expression must be marked IMMUTABLE`. Use
  `(created_at AT TIME ZONE 'UTC')::date`.
- `to_char`, `now()`, anything reading tables or settings.
Wrapping a non-immutable function in your own function marked IMMUTABLE compiles,
but gives a silently wrong index when the hidden dependency changes. Do not.

## Alternatives
- `citext` column type for case-insensitive text everywhere.
- Nondeterministic ICU collation (`CREATE COLLATION ci (provider=icu, locale='und-u-ks-level2', deterministic=false)`)
  for case-insensitive equality (but not LIKE before PG18).
- Generated stored column plus a plain index: easier to see and reuse.

## Gotchas
- Every insert/update evaluates the expression: expensive functions slow writes.
- HOT updates are blocked if an indexed expression's inputs change (PG
  checks column membership, not expression values).

## Verify
`EXPLAIN SELECT * FROM users WHERE lower(email) = 'a@b.com';` shows
`Index Scan using users_email_lower_uq`. `SELECT * FROM pg_stats WHERE tablename = 'users_email_lower_uq';` shows expression stats.

## Checked
- PostgreSQL 17.6 with 20,000-row tables: all three create statements work (`created_at::date` only on `timestamp`); `timestamptz::date`, `to_char` and `now()` fail with `functions in index expression must be marked IMMUTABLE`; `(created_at AT TIME ZONE 'UTC')::date` works; `lower(email) = ...` uses `users_email_lower_uq` while `ILIKE` and `upper()` do not; the unique index rejects `X@Y.IO` after `x@y.io`; `pg_stats` shows the expression's statistics under the index name; wrapping `current_date` in an `IMMUTABLE` function is accepted (the silent trap). Nondeterministic ICU collation and PG18 LIKE notes verified in the nondeterministic-collations skill.
HOT updates: with `fillfactor=50` and an index on `lower(a)`, updating only `b` (50 rows) gave `n_tup_hot_upd` = 50 while updating `a` (50 rows) gave no HOT updates.
