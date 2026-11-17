---
id: computing-software.database-administration.mysql.throttling-online-schema-migrations
name: throttling-online-schema-migrations
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, online-schema-change, migration-throttling, gh-ost, pt-online-schema-change, replica-lag, max-load]
level: practitioner
status: docs-checked
description: "Keep gh-ost and pt-online-schema-change from hurting production: throttle on replica lag and Threads_running, chunk sizing, and pausing a running migration."
sources:
  - https://github.com/github/gh-ost/blob/master/doc/throttle.md
  - https://github.com/github/gh-ost/blob/master/doc/interactive-commands.md
  - https://docs.percona.com/percona-toolkit/pt-online-schema-change.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Throttling online schema migrations

Online migration tools copy the table in chunks while tracking changes. The copy is extra
write load that replicates; unthrottled, it causes replica lag and latency spikes.

## gh-ost
```bash
gh-ost --host=replica1 --database=shop --table=orders \
  --alter="ADD COLUMN source varchar(32)" \
  --chunk-size=1000 \
  --max-lag-millis=1500 \
  --throttle-control-replicas="replica1,replica2,replica3" \
  --max-load="Threads_running=50" --critical-load="Threads_running=200" \
  --nice-ratio=0.5 \
  --throttle-flag-file=/tmp/ghost.throttle \
  --postpone-cut-over-flag-file=/tmp/ghost.postpone \
  --execute
```
- `--max-lag-millis`: pause copying when any control replica lags more (lag measured via
  gh-ost's heartbeat table, so accurate to sub-second).
- `--max-load`: pause when a status variable exceeds the threshold on the source;
  `--critical-load` **aborts** the migration.
- `--nice-ratio`: sleep that fraction of each chunk's copy time.
- Interactive: `echo throttle | nc -U /tmp/gh-ost.shop.orders.sock`, `no-throttle`,
  `status`, `chunk-size=500`, `max-lag-millis=3000` adjust a running migration.

## pt-online-schema-change
```bash
pt-online-schema-change --alter "ADD COLUMN source varchar(32)" D=shop,t=orders \
  --chunk-time=0.5 \
  --max-lag=2 --check-interval=1 --recursion-method=dsn=D=percona,t=dsns \
  --max-load Threads_running=50 --critical-load Threads_running=200 \
  --pause-file=/tmp/ptosc.pause \
  --execute
```
- `--chunk-time` auto-sizes chunks to take ~0.5 s each.
- `--max-lag` checks replicas found via `--recursion-method` (processlist, hosts, or a DSN table).
- Triggers on the original table add write overhead for the whole run; avoid peak hours.

## Choosing thresholds
- Lag threshold below what your read replicas and failover tolerate (1-5 s typical).
- `Threads_running` threshold around 2-3x normal peak.
- Run during low traffic; expect the copy to take longer than the naive estimate because of
  throttling. Plan for hours or days on TB tables.

## Gotchas
- Throttling only on replicas you list: an unlisted DR replica can still fall behind.
- Group Replication and Galera have their own flow control and failure detection; watch group health while a migration runs.
- Long throttled migrations grow the binlog and (pt-osc) trigger overhead; watch disk.

## Verify
During the run, replica lag stays under the threshold (`SHOW REPLICA STATUS`, heartbeat),
`status` output shows periodic throttling reasons, and p99 latency of the app is stable.

## Checked

2026-10-31: confirmed gh-ost flags (`--max-lag-millis`, `--max-load`, `--critical-load` which panics and bails out, `--nice-ratio`, `--throttle-flag-file`, `--postpone-cut-over-flag-file`, interactive `throttle`/`no-throttle`/`chunk-size=`/`max-lag-millis=`) on the gh-ost command-line-flags and interactive-commands docs, and pt-online-schema-change `--chunk-time` (0.5 s default), `--max-lag`, `--check-interval`, `--recursion-method`, `--pause-file` on the Percona reference. Reworded the Group Replication sentence (gh-ost Group-Replication-specific checks unconfirmed).
Method: documentation only; no commands were run.
