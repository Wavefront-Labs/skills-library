---
id: computing-software.database-administration.scylladb.kb-count-all-rows-timeout
name: kb-count-all-rows-timeout
category: computing-software
field: database-administration
product: scylladb
tags: [count, full-scan, using-timeout, readtimeout, tablestats]
level: practitioner
status: docs-checked
description: "Why SELECT COUNT(1) on a large ScyllaDB table times out, raising the query timeout with USING TIMEOUT, and estimating partition counts with nodetool tablestats."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/count-all-rows.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Counting all rows is slow

```
SELECT COUNT(1) FROM ks.table;
```
may fail with a `ReadTimeout` error. `COUNT()` runs a full scan on all nodes, which can take longer than the ScyllaDB query timeout.

Options:
1. Raise the timeout for that one query with the `USING TIMEOUT` directive:
```
SELECT COUNT(1) FROM ks.table USING TIMEOUT 120s;
```
2. Get an estimate of the number of partitions (not rows) from `nodetool tablestats`.

## Checked

2026-11-04. Confirmed against kb/count-all-rows.rst: ReadTimeout cause, USING TIMEOUT 120s example and nodetool tablestats partition estimate. Removed the guidance bullets (cluster-wide timeouts, off-peak, counter table), which the page does not state.

Method: documentation only; no commands were run.
