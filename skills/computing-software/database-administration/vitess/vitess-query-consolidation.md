---
id: computing-software.database-administration.vitess.vitess-query-consolidation
name: vitess-query-consolidation
category: computing-software
field: database-administration
product: vitess
tags: [query-consolidation, vttablet, consolidator, overload, read-after-write]
level: practitioner
status: docs-checked
description: "Configure VTTablet query consolidation: how identical queries share one result, the waiter cap and reject-on-cap flags, proto3 caching, and the read-after-write caveat."
sources:
  - https://vitess.io/docs/25.0/user-guides/configuration-advanced/query-consolidation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Query consolidation protects the database from QPS spikes on a single query. When vttablet receives a query identical to one already executing (same text including literals and bind variables), it waits and shares the first result.

Flags: `--enable-consolidator` (default true); `--enable-consolidator-replicas` (consolidate only on non-primary tablets); `--consolidator-query-waiter-cap` (max waiting clients per query, unlimited by default); `--consolidator-cache-proto3-rows` (default false; the leader encodes the result once instead of each waiter encoding it, which matters for large results with many waiters: a 100MB result with 50 waiters is about 5GB transient allocation otherwise); `--consolidator-reject-on-cap` (default false; needs a non-zero waiter cap).

Waiter cap: with cap 10 and 15 identical queries, query 1 runs, 2 to 11 wait, and 12 to 15 run independently by default. With `--consolidator-reject-on-cap`, 12 to 15 fail with `RESOURCE_EXHAUSTED`, making overload visible so clients can back off.

Consistency: read-after-write can be lost. If user1 reads, user2 writes, then user2 issues the identical read while user1's is still running, user2 receives user1's older result. If the application is sensitive, disable it on the primary with `--enable-consolidator=false` and `--enable-consolidator-replicas=true`.

## Checked

2026-11-04. Flags, waiter-cap example, memory figures and the consistency workaround confirmed on the Query Consolidation page.

Method: documentation only; no commands were run.
