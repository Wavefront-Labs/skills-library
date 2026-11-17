---
id: computing-software.devops-ci-cd.deployment-strategies.online-schema-change-for-large-tables
name: online-schema-change-for-large-tables
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, database-change-management, online-schema-change, gh-ost, pt-online-schema-change, mysql, postgresql, create-index-concurrently, lock-timeout, not-valid-constraint, pgroll, zero-downtime-migrations]
level: advanced
status: draft
description: "Alter huge production tables without downtime: gh-ost and pt-online-schema-change for MySQL, Postgres concurrent indexes, NOT VALID constraints, lock_timeout, and batched backfills."
sources: ["https://github.com/github/gh-ost/blob/master/doc/command-line-flags.md", "https://docs.percona.com/percona-toolkit/pt-online-schema-change.html", "https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY", "https://www.postgresql.org/docs/current/sql-altertable.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Online schema change for large tables

A plain `ALTER TABLE` on a 500 GB table can lock writes for hours or saturate
replication. Use tools/patterns that copy or validate in the background.

## MySQL: gh-ost (triggerless, binlog-based)
```bash
gh-ost \
  --host=replica.db --database=shop --table=orders \
  --alter="ADD COLUMN status_v2 VARCHAR(32) NULL, ADD INDEX idx_status_v2 (status_v2)" \
  --user=ghost --password="$PW" \
  --assume-rbr --allow-on-master=false \
  --chunk-size=1000 --max-load=Threads_running=40 --critical-load=Threads_running=200 \
  --max-lag-millis=1500 --throttle-control-replicas=replica2.db \
  --postpone-cut-over-flag-file=/tmp/ghost.postpone \
  --exact-rowcount --verbose --execute
```
- Creates `_orders_gho`, copies rows in chunks, applies ongoing changes from the binlog
  (needs `binlog_format=ROW`, `binlog_row_image=FULL`).
- Without `--execute` it's a dry run (no-op migration on the ghost table).
- Cut-over (atomic rename) is postponed while the flag file exists; delete it during a
  quiet window. Interactive control via `--serve-socket-file` (`echo throttle | nc -U ...`).
- Doesn't support tables with foreign keys (child or parent) or triggers.

## MySQL: pt-online-schema-change (trigger-based)
```bash
pt-online-schema-change --alter "ADD COLUMN status_v2 VARCHAR(32)" \
  D=shop,t=orders --max-load Threads_running=50 --critical-load Threads_running=200 \
  --chunk-time 0.5 --alter-foreign-keys-method auto --dry-run   # then --execute
```
Handles foreign keys, but triggers add write overhead on hot tables. Native MySQL 8
`ALGORITHM=INSTANT` covers adding a column at the end and some others: try
`ALTER TABLE ... , ALGORITHM=INSTANT` first; it errors instead of silently copying.

## PostgreSQL patterns
```sql
SET lock_timeout = '3s';                       -- fail fast instead of queueing traffic
CREATE INDEX CONCURRENTLY idx_orders_status ON orders (status);   -- not in a transaction
-- invalid index left after failure: DROP INDEX CONCURRENTLY idx_orders_status; retry
ALTER TABLE orders ADD COLUMN status_v2 text;  -- instant (no default rewrite)
ALTER TABLE orders ADD COLUMN flag boolean DEFAULT false;  -- instant since PG11 (non-volatile default)
ALTER TABLE orders ADD CONSTRAINT orders_status_chk CHECK (status_v2 IS NOT NULL) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_status_chk;  -- scans without blocking writes
-- SET NOT NULL then uses the validated check (PG12+) and skips the full scan
```
- Changing a column type usually rewrites: add a new column, backfill, swap in app.
- Tools: `pgroll`, `reshape` automate expand/contract with views.

## Backfills
Batch by primary key range (`UPDATE ... WHERE id BETWEEN $a AND $b`), 1k-10k rows per
batch, sleep between, watch replica lag; make it resumable and idempotent. Never one
giant `UPDATE`.

## In the pipeline
Long online migrations run **out of band** (a dedicated job/runbook with operator
control), not inside the 15-minute deploy job. The app change that depends on the new
column ships after the migration finishes (expand/contract).

## Verify
During the run, p99 write latency and replica lag stay within SLO; gh-ost status shows
`Copy: X/Y rows; ETA`; after cut-over `SHOW CREATE TABLE` has the change and the `_gho`
/`_del` tables are cleaned up.
