---
id: computing-software.cloud-infrastructure-engineering.cortex.troubleshoot-cortex-read-and-storage-path
name: troubleshoot-cortex-read-and-storage-path
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [troubleshooting, queries, store-gateway, compactor, wal]
level: practitioner
status: docs-checked
description: "Diagnose slow queries, missing old data, unshipped blocks, WAL corruption and a lagging compactor in Cortex."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/operations/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Queries time out at the frontend: open the reads and slow-queries dashboards. If the queue is full (`CortexFrontendQueriesStuck` or `CortexSchedulerQueriesStuck`) there are too few queriers or they are blocked downstream, so check querier CPU, then ingester and store-gateway latency. If the queue is empty but queries are slow, the bottleneck is in the querier or below; look at chunks fetched and bytes scanned, since an expensive query may need heavy-query protections.

Partial or no data for old ranges: check `CortexStoreGatewayHasNotSyncTheBucket` (a stale store-gateway misses new blocks), `CortexBucketIndexNotUpdated` (the compactor maintains the index) and `CortexQuerierHighRefetchRate` (store-gateways missing blocks the querier expected).

Incorrect results: `CortexQueriesIncorrect` fires when query-tee shows two backends disagreeing; use the Query Auditor to bisect.

Ingester not shipping blocks: causes are bad object-store credentials (403 or AccessDenied in logs), no block cut yet (default every 2h), or disk pressure (`cortex_ingester_tsdb_*`).

TSDB head compaction or WAL errors (`CortexIngesterTSDBHeadCompactionFailed`, `CortexIngesterTSDBWALCorrupted`, `CortexIngesterTSDBWALWritesFailed`): treat the ingester as failed, cordon it and let traffic shift to other replicas. Do not restart in place if the WAL is corrupt, or you lose the in-memory series.

Compactor behind (`CortexCompactorHasNotSuccessfullyRunCompaction`): check CPU and memory headroom (compaction is CPU-bound), object-store latency, and per-tenant progress on the compactor dashboard.

## Checked

2026-11-04. Claims were read against the Cortex docs page: Troubleshooting Cortex (Read path, Storage path) (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
