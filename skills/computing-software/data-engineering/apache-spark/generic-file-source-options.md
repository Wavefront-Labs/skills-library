---
id: computing-software.data-engineering.apache-spark.generic-file-source-options
name: generic-file-source-options
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark-data-sources, ignorecorruptfiles, ignoremissingfiles, recursive-file-lookup, pathglobfilter, modifiedafter, file-source]
level: practitioner
status: docs-checked
description: "Use Spark's generic file source options (pathGlobFilter, recursiveFileLookup, modifiedAfter/Before, ignoreCorruptFiles, ignoreMissingFiles) to read messy landing zones safely."
sources:
  - https://spark.apache.org/docs/latest/sql-data-sources-generic-options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic file source options

**Goal:** read only the files you mean to from a landing directory, and decide consciously how to treat broken or vanishing files.

These options are documented on the Generic File Source Options page; check there which formats support each one.

## Filtering which files are read
```python
df = (spark.read.format("json")
      .option("pathGlobFilter", "*.json")          # file-name filter
      .option("recursiveFileLookup", "true")        # read nested dirs; DISABLES partition inference
      .option("modifiedAfter", "2026-10-17T00:00:00")
      .option("modifiedBefore", "2026-10-18T00:00:00")
      .load("s3a://landing/vendor_x/"))
```
- `recursiveFileLookup=true` disables partition inference, so a Hive-style `dt=...` folder will not become a `dt` column; extract it from the path yourself, or keep partition discovery (the default). It also throws if the source specifies a partitionSpec.
- `modifiedAfter`/`modifiedBefore` take timestamps in the form `YYYY-MM-DDTHH:mm:ss`.

## Broken and missing files
```python
spark.conf.set("spark.sql.files.ignoreCorruptFiles", "true")   # or .option("ignoreCorruptFiles","true")
spark.conf.set("spark.sql.files.ignoreMissingFiles", "true")
```
- `spark.sql.files.ignoreCorruptFiles` and `spark.sql.files.ignoreMissingFiles` both default to false. With `ignoreCorruptFiles` on, rows from corrupt files are not returned, so reconcile file counts against row counts.
- `ignoreMissingFiles`: tolerates files deleted between listing and reading. Better to avoid the race than to hide it.

## Gotchas
- Very many small files: listing dominates; `spark.sql.sources.parallelPartitionDiscovery.threshold` is the related setting (see the configuration page).

## Verify
- [ ] The number of files read equals the number expected for the window (check the Spark UI input metrics).
- [ ] If ignoreCorruptFiles is on, a reconciliation step alerts on skipped files.

## Checked

2026-10-28. Confirmed against: Spark generic file source options and binaryFile pages (pathGlobFilter, recursiveFileLookup disables partition inference and conflicts with partitionSpec, modifiedBefore/modifiedAfter format), configuration page (spark.sql.files.ignoreCorruptFiles / ignoreMissingFiles default false, parallelPartitionDiscovery.threshold). Removed (not confirmable in the fetched pages): format list, batch-only and timezone claims, Hadoop glob claim, warning text, _metadata column section, hidden-file and gzip claims, Auto Loader.

Method: documentation only; no commands were run.
