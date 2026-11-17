---
id: computing-software.database-administration.yugabytedb.inspect-data-at-point-in-time
name: inspect-data-at-point-in-time
category: computing-software
field: database-administration
product: yugabytedb
tags: [yb-read-time, inspect-at-pit, pitr, read-only, history-retention, snapshot-too-old]
level: practitioner
status: docs-checked
description: "Read old data without restoring by setting yb_read_time in a YSQL session, and the rules: read-only, no crossing DDL, session scoped, reset with 0."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/backup-restore/point-in-time-recovery/inspect.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inspect data at a point in time

`yb_read_time` makes a YSQL session read data as it was at a past moment, without restoring anything.

```
SET yb_read_time TO 1741886500266607;   -- microseconds since the epoch
SELECT * FROM t1;
SET yb_read_time TO 0;                  -- back to the current time
```

Rules:
- It is per session; other sessions are unaffected.
- Reads only. Write DML and DDL are rejected with a NOTICE that yb_read_time should only be set for read-only queries.
- Do not choose a time earlier than the most recent DDL, including cluster-wide DDL on global objects; the schema is not rewound.
- The time must be inside the history retention window, set by `timestamp_history_retention_interval_sec` together with `timestamp_syscatalog_history_retention_interval_sec` (set both; default 900 seconds). A long-running query that outlives the window fails with Snapshot too old; raising retention cannot recover history already compacted.
- You cannot inspect a time before a database clone was created, and temporary tables and vector indexes are not supported.

Recovery workflow for deleted rows: find the timestamp just before the mistake, `SET yb_read_time`, export the rows with COPY ... TO, reset `yb_read_time` to 0 (or open a new session), and COPY the rows back in.

If the deletion affected many tables, the docs suggest Clone to PIT instead.

## Checked

2026-11-04. Confirmed against the Inspect at PIT page: `SET yb_read_time` in microseconds, 0 to reset, per-session scope, no write DML or DDL (with the NOTICE), no reading before the most recent DDL (including clone), default retention 900 seconds, Snapshot too old, and the COPY recovery example. Changed: the retention paragraph now names both flags the page says to set, and the 'rewind or clone for large damage' line was replaced with the page's actual suggestion (Clone to PIT). The PITR schedule retention claim was not on the page and was removed.

Method: documentation only; no commands were run.
