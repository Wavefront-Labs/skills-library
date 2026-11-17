---
id: computing-software.database-administration.postgresql.multixact-wraparound
name: multixact-wraparound
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, vacuum, autovacuum, multixact, wraparound, foreign-keys, select-for-share]
level: advanced
status: docs-checked
description: "Monitor and prevent multixact ID wraparound and members-space exhaustion caused by row-sharing locks (FK checks, FOR SHARE) and fix with targeted vacuum freezes."
sources:
  - https://www.postgresql.org/docs/current/routine-vacuuming.html#VACUUM-FOR-MULTIXACT-WRAPAROUND
  - https://www.postgresql.org/docs/current/runtime-config-autovacuum.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multixact wraparound

## What multixacts are
When more than one transaction locks the same row (e.g. many inserts into child tables
take `FOR KEY SHARE` on the same parent row via foreign key checks, or `SELECT ... FOR SHARE`),
PostgreSQL stores a **multixact ID** in the row's xmax. Multixact IDs are 32-bit like XIDs
and wrap around; they also use a separate "members" storage area (`pg_multixact/members`)
that can run out before the IDs do.

## Failure
If autovacuum fails to clear old multixact IDs, the system starts emitting warnings when the database's oldest MXIDs are forty million from the wraparound point, and refuses to generate new MXIDs once fewer than three million remain. MXID exhaustion blocks only the statements that need new multixacts, not every write as XID exhaustion does, but it is still an outage for affected workloads.

## Monitor
```sql
SELECT datname, mxid_age(datminmxid) AS mxid_age FROM pg_database ORDER BY 2 DESC;
SELECT c.oid::regclass, mxid_age(c.relminmxid) AS mxid_age,
       pg_size_pretty(pg_total_relation_size(c.oid))
FROM pg_class c WHERE c.relkind IN ('r','m','t')
ORDER BY 2 DESC LIMIT 10;
-- inspect one multixact: SELECT * FROM pg_get_multixact_members('<multixid>'::xid);
-- size of members storage: du -sh $PGDATA/pg_multixact/members
```
Alert when `mxid_age` climbs well above its normal plateau toward `autovacuum_multixact_freeze_max_age` (default 400 million), or when the members storage nears the documented ~10GB point (see below).

## Tuning
| Setting | Default | Meaning |
|---|---|---|
| `autovacuum_multixact_freeze_max_age` | 400,000,000 | forces an anti-wraparound (aggressive) vacuum of a table, even if autovacuum is off; server-start setting, reducible per table with storage parameters |
| `vacuum_multixact_freeze_table_age` | 150,000,000 | `relminmxid` age at which VACUUM does an aggressive scan |
| `vacuum_multixact_freeze_min_age` | 5,000,000 | age at which VACUUM replaces multixact IDs it encounters (effectively capped at half of `autovacuum_multixact_freeze_max_age`) |
If the members storage exceeds about 10GB, aggressive vacuum scans happen more often for all tables, oldest multixact-age first; the members area can grow to about 20GB before wraparound. Reducing `autovacuum_multixact_freeze_max_age` (globally or per table) makes aggressive vacuums happen earlier on foreign-key-heavy workloads.

## Fix when close to the limit
```sql
-- worst tables first, no cost delay, during a quiet window
VACUUM (FREEZE, VERBOSE) public.parent_table;
```
Aggressive vacuums are guaranteed to be able to advance a table's `relminmxid`. When recovering from exhaustion the docs say to follow the XID-exhaustion steps with differences: running and prepared transactions can be ignored if they cannot appear in a multixact; replication slots do not directly hold back multixact cleanup, so dropping stale slots is not usually relevant; MXID information is not visible in `pg_stat_activity`, but looking for old XIDs still helps find the transactions causing the problem.

## Reduce multixact generation
- Avoid `SELECT ... FOR SHARE` where `FOR KEY SHARE` or no lock is enough.
- High-fanout FKs onto a hot parent row (one tenant row referenced by millions of inserts)
  are the classic source; batch inserts or reconsider the FK on append-only logs.

## Verify
After VACUUM, `mxid_age(relminmxid)` for the table drops to near
`vacuum_multixact_freeze_min_age`, and `datminmxid` age for the database falls.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): "Multixacts and Wraparound" (what multixacts are and the separate 32-bit members counter, `pg_get_multixact_members(multixid)`, `mxid_age()` on `relminmxid`, aggressive vacuum triggers, about 10GB members threshold and about 20GB wraparound, warning at forty million and refusal below three million, recovery differences from XID exhaustion), and the defaults of `autovacuum_multixact_freeze_max_age` (400 million), `vacuum_multixact_freeze_table_age` (150 million) and `vacuum_multixact_freeze_min_age` (5 million, capped at half the max age). Corrected: the members threshold is about 10GB, not 50% of a limit; `pg_get_multixact_members` takes a multixact id and is not a PG17 feature; replication slots do not directly hold back multixact cleanup. Removed the quoted warning and error texts and the 200M example, which the documentation does not give.
Method: documentation only; no commands were run.
