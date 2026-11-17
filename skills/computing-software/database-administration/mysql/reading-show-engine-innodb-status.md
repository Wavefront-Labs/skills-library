---
id: computing-software.database-administration.mysql.reading-show-engine-innodb-status
name: reading-show-engine-innodb-status
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, innodb, innodb-status, innodb-monitor, latest-detected-deadlock, semaphores, troubleshooting]
level: advanced
status: docs-checked
description: "Read SHOW ENGINE INNODB STATUS section by section: semaphores, latest deadlock, transactions, file I/O, buffer pool and log checkpoint age."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-standard-monitor.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-enabling-monitors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading SHOW ENGINE INNODB STATUS

```sql
SHOW ENGINE INNODB STATUS\G
```
Values are averages over the interval printed at the top (`Per second averages calculated
from the last 23 seconds`); an interval of a few seconds makes rates noisy.

## Sections
**SEMAPHORES**
`OS WAIT ARRAY INFO` and lines like `--Thread 1403 has waited at btr0sea.cc line 1215 for 241 seconds the semaphore`.
Many threads waiting on `btr0sea` latches indicate adaptive hash index contention: add partitions or disable it with `innodb_adaptive_hash_index=OFF`.

**LATEST DETECTED DEADLOCK**
Both transactions, the statements, `HOLDS THE LOCK(S)` and `WAITING FOR THIS LOCK`, the index
and lock mode (`lock_mode X locks rec but not gap`, `locks gap before rec`, `insert intention`),
and `WE ROLL BACK TRANSACTION (2)`. Only the last deadlock is kept: set
`innodb_print_all_deadlocks = ON` to log all of them to the error log.

**TRANSACTIONS**
- `Trx id counter`, `Purge done for trx's n:o < X undo n:o < 0`, **`History list length N`**:
  growing HLL = purge lag from long-running transactions or read views.
- Per transaction: `ACTIVE 3600 sec`, `MySQL thread id 123`, `n lock struct(s), heap size,
  n row lock(s), undo log entries` - find the one that has been open for an hour.

**FILE I/O**
Pending reads/writes and fsync rates.

**INSERT BUFFER AND ADAPTIVE HASH INDEX**
Change buffer size and merges; AHI `hash searches/s` vs `non-hash searches/s`.

**LOG**
```
Log sequence number          123456789012
Log flushed up to            123456789000
Last checkpoint at           123400000000
```
Checkpoint age = LSN - last checkpoint. A growing gap means flushing is not keeping up with redo generation; review `innodb_redo_log_capacity` and `innodb_io_capacity`.

**BUFFER POOL AND MEMORY**
`Buffer pool size`, `Free buffers`, `Database pages`, `Modified db pages` (dirty), hit rate
`Buffer pool hit rate 999 / 1000`, `pages made young/not young`, `evicted without access`.
Low hit rate with free buffers = 0 means the working set does not fit.

**ROW OPERATIONS**
`n queries inside InnoDB, n queries in queue`, reads/inserts/updates/deletes per second.

## Capture over time
`innodb_status_output = ON` enables periodic output of the standard InnoDB Monitor (turn off afterwards). Take repeated manual captures during an incident to compare.

## Verify
Cross-check findings with `sys.innodb_lock_waits`, `information_schema.innodb_trx` and
`SHOW GLOBAL STATUS LIKE 'Innodb_%'` counters.

## Checked

2026-11-01. Confirmed against MySQL 8.4 manual pages innodb-standard-monitor (report sections and sample lines), innodb-deadlocks, innodb-parameters (innodb_print_all_deadlocks, innodb_status_output, innodb_adaptive_hash_index), innodb-adaptive-hash (btr0sea latch advice). Removed unconfirmed semaphore time-out, checkpoint threshold, hot-spot list, 15-second interval and third-party tool claims.

Method: documentation only; no commands were run.
