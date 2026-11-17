---
id: computing-software.database-administration.oracle-database.common-wait-events
name: common-wait-events
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, awr, ash, log-file-sync, db-file-sequential-read, enq-tx, wait-events, performance-diagnosis]
level: practitioner
status: docs-checked
description: "Interpret the Oracle wait events that dominate AWR top-five lists (log file sync, db file sequential/scattered read, enq TX row lock, latch and buffer busy waits) and what to do."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/descriptions-of-wait-events.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgdba/instance-tuning-using-performance-views.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common wait events

Find what sessions wait on now and historically:
```sql
SELECT event, wait_class, COUNT(*) FROM v$session WHERE state = 'WAITING' AND wait_class <> 'Idle' GROUP BY event, wait_class ORDER BY 3 DESC;
SELECT event, COUNT(*) samples FROM v$active_session_history
WHERE sample_time > SYSDATE - 1/24 AND session_state = 'WAITING' GROUP BY event ORDER BY 2 DESC;   -- Diagnostics Pack
```

## User I/O
- **db file sequential read**: single-block reads, usually index access or table access by rowid.
  High total = lots of index lookups (nested loops on large sets) or slow storage. The wait time is the actual I/O time; compare the average wait with your storage's expected latency in AWR "Foreground Wait Events", and check the SQL ordered by reads.
- **db file scattered read**: multiblock reads into the buffer cache (full scans). Often a
  missing index or stale statistics choosing a full scan.
- **direct path read**: reads that bypass the buffer cache (the session is posted when the asynchronous I/O completes); look for large scans and sorts or hashes spilling to TEMP (`PGA_AGGREGATE_TARGET` too small or bad estimates).

## Commit
- **log file sync**: when a session commits, its redo must be flushed to the redo log; the wait includes writing the log buffer and the post. Compare with
  **log file parallel write** (LGWR writing redo to the log files; not complete until the last I/O is on disk): if similar, redo storage is slow; if log
  file sync is much higher, look at LGWR scheduling, row-by-row commits in loops, or Data Guard SYNC transport latency.

## Concurrency / application
- **enq: TX - row lock contention**: a session waits for a row another transaction locked.
  Find the blocker (`v$session.blocking_session`); application design or uncommitted sessions.
- **enq: TX - index contention**: a transaction inserting a row in an index waits for the end of an index block split done by another transaction. Under heavy inserts consider reverse-key or hash-partitioned indexes and larger sequence caches.
- **library cache: mutex X / cursor: pin S wait on X**: library cache mutexes protect hash buckets in the shared pool and are often associated with high parse activity; `cursor: pin S wait on X` is a session requesting a shared mutex pin while another holds it exclusively on the same cursor. Use bind variables and check version counts.
- **buffer busy waits / read by other session**: a session cannot pin a buffer another session has pinned / requests a buffer currently being read into the cache by another session; identify the object via ASH `current_obj#`.

## Configuration
- **log file switch (checkpoint incomplete)**: LGWR cannot wrap into the next log because the checkpoint for it has not completed. **log file switch (archiving needed)**: the next log has not been archived yet; check the alert log.
- **free buffer waits**: no free buffer was found or the dirty queue is full; look at DBWR throughput, I/O and buffer cache sizing.

## Approach
Use AWR/ASH for the period, identify the top event by DB time, then the SQL and objects that
produce it (ASH `sql_id`, `current_obj#`), fix the cause, not the symptom.

## Verify
After the fix, the event's share of DB time in the next AWR report drops, and the response time
of the affected workload improves.

## Checked
Date 2026-10-22. Oracle Database 19c Database Reference, Descriptions of Wait Events (first 100,000 characters of the page).
Confirmed descriptions: db file sequential/scattered read, direct path read, log file sync, log file parallel write,
enq: TX - row lock contention, enq: TX - index contention, library cache: mutex X, cursor: pin S wait on X, buffer busy
waits, read by other session, log file switch (checkpoint incomplete / archiving needed), free buffer waits.
Corrected: enq: TX - index contention is a wait for an index block split, not specifically a right-hand-index problem.
Removed the latency rule of thumb (the manual gives none). Four event names (direct path read/write temp, enq: TM -
contention, latch: cache buffers chains) were not found in the text read, so their explanations were removed.
Method: documentation only; no commands were run.
