---
id: computing-software.data-engineering.apache-pinot.apache-pinot-consistent-data-push-and-rollback
name: apache-pinot-consistent-data-push-and-rollback
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, consistent-push, segment-lineage, startreplacesegments, endreplacesegments, revertreplacesegments, rollback, atomic-segment-replacement]
level: advanced
status: docs-checked
description: "Atomic batch refresh with consistent push: segment lineage in ZooKeeper, start, end and revert replace APIs, supported frameworks and the controller and minion timeouts."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/consistent-push-and-rollback.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consistent data push and rollback

Without it, segments are replaced one at a time, so broker queries during an upload can see a mix of old and new data. Consistent push lets you switch atomically between data snapshots and roll back a bad push. The docs say only OFFLINE table REFRESH use cases are supported.

It uses **segment lineage** metadata in ZooKeeper (path `<cluster_name>/PROPERTYSTORE/SEGMENT_LINEAGE/<table_name>`). Each lineage entry holds a segmentsFrom list, a segmentsTo list, a state and a timestamp. The broker routes to segmentsFrom for entries in `IN_PROGRESS` or `REVERTED` state and to segmentsTo for entries in `COMPLETED` state.

Controller APIs:
1. `startReplaceSegments` registers the segments to be replaced and the new ones, persists a lineage entry in IN PROGRESS state and returns its ID.
2. Upload the new segments.
3. `endReplaceSegments` sets the entry to `COMPLETED`, so the new set becomes visible.
4. `revertReplaceSegments` sets the entry to `REVERTED` (rollback).

The docs say users are not typically expected to call these directly: consistent push is built into batch ingestion jobs, currently supported only for the standalone execution framework.

## Enabling it

Set `consistentDataPush: true` under `ingestionConfig.batchIngestionConfig`, with `segmentIngestionType` REFRESH, on an OFFLINE table. The docs advise raising the table storage quota to 2x. A timestamp is injected as a segment name postfix; there is currently no way to disable consistent push in place once enabled (create a new table). If a push job fails, it reverts the uploaded segments.

## Manual rollback

List lineage with the controller `/lineage` REST API to find the entry ID, call `revertReplaceSegments`, then list lineage again to confirm the entry is `REVERTED`.

## Timeouts and retries

`endReplaceSegments` waits synchronously for new segments to be ONLINE in the ExternalView. Controller properties in controller.conf:
- `controller.segment.replace.externalViewMaxWaitMs` default **600000** (10 minutes)
- `controller.segment.replace.externalViewCheckIntervalMs` default **1000**
- `controller.segment.replace.maxRetryAttempts` default **5** (exponential backoff)

The controller can spend roughly externalViewMaxWaitMs times maxRetryAttempts waiting, so set the Minion's `pinot.minion.endReplaceSegments.timeoutMs` high enough to cover it. The Minion defaults for `pinot.minion.startReplaceSegments.timeoutMs` and `pinot.minion.endReplaceSegments.timeoutMs` are both 600000. Minion tasks using the protocol can also set `segmentUploadRequestTimeoutMs` (default 600000) in their `taskTypeConfigsMap.<taskType>` entry; the docs' example uses MergeRollupTask.

## Cleanup

The retention manager cleans up segments and lineage. In `segmentsConfig`: `replacedSegmentsRetentionPeriod` defaults to 1d for REFRESH tables and 4h otherwise (0s deletes replaced segments on the next retention pass); `lineageEntryCleanupRetentionPeriod` defaults to 1d. While a lineage entry is live, the generic segment delete flow is rejected by default; `controller.lineage.exclusive.delete.enabled=false` restores the legacy behaviour.

## Checked

Confirmed against the Pinot docs page "Consistent Push and Rollback": APIs, states, ZooKeeper path, standalone-only support, REFRESH-only scope, timeout and retention properties and defaults. Removed the claim that merge-rollup uses "the same lineage entries" (the page only shows a MergeRollupTask upload timeout) and the "not Spark or Hadoop" wording (page says only standalone).

Method: docs-only read of cited pages, 2026-11-08
