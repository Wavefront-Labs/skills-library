---
id: computing-software.database-administration.oracle-database.rac-global-cache-waits-and-interconnect
name: rac-global-cache-waits-and-interconnect
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rac, real-application-clusters, gc-waits, global-cache, cache-fusion, interconnect, gc-buffer-busy, hot-blocks, awr]
level: sme
status: docs-checked
description: "Diagnose Oracle RAC global cache waits: read gc events in AWR and ASH, verify the interconnect, and find hot blocks and the SQL behind them."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/racad/monitoring-performance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RAC global cache waits and the interconnect

Cache Fusion ships blocks between instances over the private interconnect. "gc" waits are time spent getting a
block (or a grant) from the global cache. Most global cache wait events with a high total time in AWR or Statspack
are normal and can be top DB-time consumers without indicating a problem. Start from an ADDM report, then AWR.

## Read the waits
| Event | Meaning (Oracle RAC guide) |
|---|---|
| `gc cr block 2-way / 3-way`, `gc current block 2-way / 3-way` | block shipped without being busy, pinned or needing a log flush; 2-way = from the master (1 message, 1 transfer), 3-way = forwarded to a third node (2 messages, 1 transfer) |
| `gc cr grant 2-way`, `gc current grant 2-way` | block not cached in any instance; a global grant lets you read it from disk (cr grant: lots of disk I/O) or modify it (current grant: inserts that format new blocks) |
| `gc cr block busy`, `gc current block busy` | sending was delayed on a remote instance, e.g. redo for the block's changes not yet written, block pinned or held by sessions |
| `gc buffer busy acquire / release` | local buffer cannot be accessed because a global operation on it is pending: block contention, requests queue |
| `gc cr block congested`, `gc current block congested` | delay in the GCS, usually high load or CPU saturation |
Higher average times on the 2-way/3-way events come from high load (CPU shortage, run queues) or from using the
public instead of the private interconnect. If averages are acceptable and no load or interconnect issue exists,
the time usually comes from a few SQL statements that touch too many blocks. Consider both the average and the
total wait time.

## Interconnect check
```sql
SELECT * FROM v$cluster_interconnects;     -- GV$ for all instances
SELECT * FROM v$configured_interconnects;
```
Both show NAME, IP_ADDRESS, IS_PUBLIC and SOURCE; confirm the interconnect in use is not public. Identify the
cluster's interconnect with `oifcfg getif` (OCR holds it) or `OCRDUMP`. `CLUSTER_INTERCONNECTS` is rarely needed
but can assign a private IP address or NIC. Once the interconnect works you cannot influence its performance
much; adjusting IPC buffer sizes affects protocol efficiency.

## Find the objects and SQL
- `gc buffer busy` is a segment statistic, so the busiest objects show in AWR segment statistics without querying
  `V$SESSION_WAIT`. The object statistics `gc current blocks received` and `gc cr blocks received` identify
  indexes and tables shared by the active instances.
- GCS wait events carry the file number in p1 and the block number in p2 (`V$SESSION_WAIT`).
- ASH traces recent wait events and arguments, which makes it useful for hot block analysis.
- `V$SQLAREA.CLUSTER_WAIT_TIME` is the wait time a statement incurred for global cache events: tune those first.
- Statspack needs level 7 to collect block contention and segment statistics.

## Fixes
- Tune SQL to touch fewer blocks.
- For `congested` events: add CPUs, balance load, move work to another time or add a cluster node.
- For `busy` events caused by a remote log write, look at redo write time on the sending instance.

## Verify
- [ ] The interconnect views show only the private network in use.
- [ ] Average block receive time and gc share of DB time are understood against a known-good baseline.
- [ ] Hot segments and top `CLUSTER_WAIT_TIME` statements are addressed.

## Checked
2026-11-09. Read the 19c Oracle RAC Administration and Deployment Guide "Monitoring Performance" page (verifying
interconnect settings, influencing interconnect processing, GCS statistics and wait-event categories). The second
source (the `tgdba` landing page) was not read and is dropped. Removed because the page does not state them:
the sub-millisecond target, `gc cr block lost`/lost-block diagnosis and MTU/UDP/ethtool advice, the ASH query,
reverse-key/hash-partition/scalable-sequence/sequence-cache fixes, service affinity advice, LMS/`GCS_SERVER_PROCESSES`
tuning and the `gc ... request` row.
Method: documentation only; no commands were run.
