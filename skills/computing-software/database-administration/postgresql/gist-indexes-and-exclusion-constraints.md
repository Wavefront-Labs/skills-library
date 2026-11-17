---
id: computing-software.database-administration.postgresql.gist-indexes-and-exclusion-constraints
name: gist-indexes-and-exclusion-constraints
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-index-types, gist-index, exclusion-constraint, btree-gist, range-types, overlapping-bookings, sp-gist, nearest-neighbour]
level: advanced
status: verified
description: "Use GiST indexes in PostgreSQL for ranges, geometry and nearest-neighbour search, and enforce no-overlap rules (room bookings) with EXCLUDE constraints."
sources:
  - https://www.postgresql.org/docs/current/gist.html
  - https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-EXCLUSION
  - https://www.postgresql.org/docs/current/btree-gist.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GiST indexes and exclusion constraints

**Goal:** index overlap/containment/distance queries, and make the database itself
reject double-bookings.

## GiST use cases
| Data | Operators | Example |
|---|---|---|
| range types (tstzrange, int4range) | `&&` overlap, `@>` contains | availability windows |
| geometric / PostGIS geometry | `&&`, `<->` distance | nearest store |
| inet/cidr (inet_ops) | `<<`, `>>=` | IP in subnet |
| tsvector | `@@` | full text (GIN usually better for static data) |
```sql
CREATE INDEX ON bookings USING gist (during);
SELECT * FROM stores ORDER BY location <-> point(13.4, 52.5) LIMIT 5;  -- KNN uses GiST ordering
```
SP-GiST suits non-balanced partitioning data (quad-trees, prefixes like phone
numbers, inet); try it when GiST is slow on point data.

## Exclusion constraint: no overlapping bookings per room
```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;     -- lets GiST handle '=' on room_id
ALTER TABLE bookings ADD CONSTRAINT no_overlap
  EXCLUDE USING gist (room_id WITH =, during WITH &&);
```
Two rows conflict when **all** operators return true. Inserting an overlap fails with
`conflicting key value violates exclusion constraint "no_overlap"` (SQLSTATE 23P01),
race-free across concurrent transactions, which app-side checks are not.
Add a `WHERE (status <> 'cancelled')` predicate to ignore some rows.

Range bounds: use `'[)'` (inclusive start, exclusive end) so back-to-back
bookings `[10:00,11:00)` and `[11:00,12:00)` do not overlap.

## Gotchas
- Adding an exclusion constraint to a big table scans and locks it
  (`ACCESS EXCLUSIVE` during build); `NOT VALID` is rejected (`EXCLUDE constraints cannot be marked NOT VALID`). Build in a
  maintenance window or create the table with it.
- GiST is lossy for some types: plans show a recheck; that is normal.
- Exclusion constraints cannot be the target of foreign keys (`there is no unique constraint matching given keys for referenced table`) or of `ON CONFLICT DO UPDATE` (`ON CONFLICT DO UPDATE not supported with exclusion constraints`); `ON CONFLICT ON CONSTRAINT name DO NOTHING` works.

## Verify
```sql
SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE contype = 'x';
```
Insert two overlapping rows in two concurrent sessions: the second fails with 23P01.

## Checked
PostgreSQL 17.6 with btree_gist: `EXCLUDE USING gist (room_id WITH =, during WITH &&) WHERE (status <> 'cancelled')` rejects an overlapping booking with `conflicting key value violates exclusion constraint "no_overlap"` (SQLSTATE 23P01 via `\set VERBOSITY sqlstate`), accepts back-to-back `[10:00,11:00)` and `[11:00,12:00)`, a cancelled overlap and the same slot in another room; `pg_get_constraintdef` prints the definition; adding the constraint held ShareLock and AccessExclusiveLock on the table; `NOT VALID`, FK-target and `ON CONFLICT DO UPDATE` errors as quoted. A GiST index on `point` served `ORDER BY location <-> point(...) LIMIT 5` (`Order By:` in the plan); `inet_ops`, tsvector and range GiST indexes build. The concurrent-session race was not run (the constraint is enforced by the index, per the PG docs).
