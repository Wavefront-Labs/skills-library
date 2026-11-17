---
id: computing-software.data-engineering.databricks.auto-loader-rate-limiting-and-backfill
name: auto-loader-rate-limiting-and-backfill
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, autoloader, autoloader-rate-limiting, cleansource, backfillinterval, maxfilespertrigger, maxbytespertrigger, availablenow]
level: advanced
status: docs-checked
description: "Tune Auto Loader for backlogs and long-running streams: per-trigger limits, availableNow batches, backfillInterval and cleanSource archiving."
sources:
  - https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/options.html
  - https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/production.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto Loader rate limiting, backfill and cleanSource

**Goal:** Auto Loader handles a 10-million-file initial backlog and years of operation without OOM, missed files or ever-growing landing zones.

## Rate limits
```python
(spark.readStream.format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.schemaLocation", "/Volumes/chk/orders/_schema")
  .option("cloudFiles.maxFilesPerTrigger", 5000)        # default 1000
  .option("cloudFiles.maxBytesPerTrigger", "20g")        # soft cap; whichever hits first
  .load("s3://landing/orders/")
  .writeStream
  .option("checkpointLocation", "/Volumes/chk/orders")
  .trigger(availableNow=True)                             # drains backlog in rate-limited batches, then stops
  .toTable("bronze.orders"))
```
- `Trigger.AvailableNow` processes all files that arrived before the query started, discovering files asynchronously and working through them in rate-limited micro-batches; files that arrive later wait for the next run. Auto Loader processes at most 1000 files per micro-batch by default.
- The file limit is hard; the byte limit is soft (more bytes can be processed). With both set, a batch ends when either limit is reached.
- Size the limits so each batch finishes comfortably on the cluster; watch `numFilesOutstanding` and `numBytesOutstanding` in the streaming query progress metrics to see the backlog.
- Databricks recommends Auto Loader in Lakeflow pipelines for production; scheduled `Trigger.AvailableNow` batch jobs suit workloads without low-latency needs.

## Initial backlog
- `cloudFiles.includeExistingFiles` defaults to `true`, so existing files are processed on first run.
- Directory listing of very large directories is costly, especially with continuous triggers such as `ProcessingTime`. Databricks recommends Auto Loader with file events for low latency and simplicity, and classic file notification mode (`cloudFiles.useNotifications`, default `false`) for very latency-sensitive streams.
- If you use file events, run the stream at least every 7 days so discovery stays incremental.

## backfillInterval
A backfill is an asynchronous directory listing that catches files discovery missed (cloud notification events are delivered at least once, but a file can still be missed):
```python
.option("cloudFiles.backfillInterval", "1 day")
```
- No default; in directory listing and classic notification modes backfills run only when you set it.
- Time-based, tracked in the checkpoint; already-ingested files are skipped, so only missed files are added.
- Each backfill is a full listing (LIST costs scale with file count), so pick the longest interval that meets your completeness SLA.
- Not supported with file events, which backfill automatically (about every 24 hours).

## cleanSource (archive or delete processed files)
Requires Databricks Runtime 16.4 LTS or above.
```python
.option("cloudFiles.cleanSource", "MOVE")                         # or DELETE; OFF is the default
.option("cloudFiles.cleanSource.moveDestination", "s3://landing-archive/orders/")
.option("cloudFiles.cleanSource.retentionDuration", "7 days")    # wait before moving
```
Keeps the source directory small (faster listing) without a separate cleanup job. It deletes or moves files in the source. With `MOVE`, source and destination must be in the same external location, volume or DBFS mount (cross-bucket moves error). With `foreachBatch`, files become candidates as soon as the function returns successfully. For `DELETE`, enable bucket versioning so deletes are soft-deletes, and use lifecycle policies to purge old versions.

## Other production options
- `cloudFiles.maxFileAge`: expires file-state entries older than this to bound RocksDB state for high-volume streams. Minimum "14 days"; Databricks recommends a conservative value such as 90 days. Too aggressive a value can cause duplicate ingestion or missed files, and setting it on the first start means data older than it is not ingested.
- `cloudFiles.allowOverwrites` (default `false`): whether changes to input files may overwrite existing data.
- `cloudFiles.validateOptions` (default `true`): errors on unknown or inconsistent options.
- Keep the checkpoint location free of cloud lifecycle policies, or the stream state is corrupted.

## Verify
- [ ] Backlog drain shows multiple batches each under the limit; no executor OOM.
- [ ] After a forced missed-notification test, the backfill run ingests the file.
- [ ] Source prefix size stable with cleanSource enabled.

## Checked

2026-11-09: reviewed against the Databricks documentation fetched this batch.

Confirmed: the 1000-file default, hard file limit versus soft byte limit, AvailableNow behaviour, backfill semantics and file-events exceptions, cleanSource runtime requirement, MOVE constraints and DELETE advice, maxFileAge minimum and warning, checkpoint lifecycle warning, and the defaults of includeExistingFiles, useNotifications, allowOverwrites, validateOptions and cleanSource (production page and the Auto Loader options table).

Removed or corrected: the claim that Trigger.Once ignores limits, the numInputRows/batchDuration metrics, "listing can skip out-of-order names", the source-write-permission and destination-not-inside-source rules, and the "start with a recent prefix and use COPY INTO" suggestion (not on the pages read). The code example paths are illustrative.

Method: documentation only; no commands were run.
