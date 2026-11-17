---
id: computing-software.database-administration.cassandra.twcs-time-series
name: twcs-time-series
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, time-window-compaction, twcs-window, ttl-expiry, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "TWCS for TTL time series"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/twcs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TimeWindowCompactionStrategy

Goal: configure TWCS correctly.
- `{'class':'TimeWindowCompactionStrategy','compaction_window_unit':'DAYS','compaction_window_size':1}`; the defaults are days and 1. Pick a unit and size giving roughly 20-30 windows over the TTL (for a 90 day TTL, 3 days).
- TWCS drops whole SSTables when they expire. Out-of-order data (mixing old and new in the write path, or read repairs pulling old data into the current memtable) defeats that; avoid `USING TIMESTAMP` and run frequent repairs.
- Enabling TWCS on existing data: consider a major compaction first. Shrinking the window does not split existing SSTables.
- `unsafe_aggressive_sstable_expiration` drops expired SSTables without checking whether they shadow others and also needs a JVM option; it is risky.
Verify: expired SSTables vanish without compaction churn.

## Checked

2026-11-02. Checked against the TWCS page (options and defaults, 20-30 windows, 90 day TTL example, out-of-order data causes, USING TIMESTAMP advice, changing options, unsafe_aggressive_sstable_expiration). Removed: 'one TTL' and 'deletes overlap windows' wording (not stated).

Method: documentation only; no commands were run.
