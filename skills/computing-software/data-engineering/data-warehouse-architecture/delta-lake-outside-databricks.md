---
id: computing-software.data-engineering.data-warehouse-architecture.delta-lake-outside-databricks
name: delta-lake-outside-databricks
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, delta-rs, delta-lake, deltalake-python, open-table-formats]
level: advanced
status: verified
description: "Read and write Delta Lake tables without Databricks: delta-rs (deltalake Python), OSS Delta with Spark, DuckDB/Polars readers, protocol features, concurrency and maintenance."
sources:
  - https://delta-io.github.io/delta-rs/
  - https://github.com/delta-io/delta-rs/blob/main/docs/integrations/object-storage/s3.md
  - https://docs.delta.io/latest/quick-start.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delta Lake outside Databricks

**Goal:** use Delta tables from lightweight Python services, open-source Spark and query engines, compatibly with Databricks-written tables.

## delta-rs (Python package `deltalake`)
```python
from deltalake import DeltaTable, write_deltalake
import pyarrow as pa

write_deltalake("s3://acme-lake/silver/events", pa_table, mode="append",
                partition_by=["event_date"],
                storage_options={"AWS_REGION": "eu-west-1"})
dt = DeltaTable("s3://acme-lake/silver/events")
df = dt.to_pyarrow_dataset().to_table(filter=pa.compute.field("event_date") == "2026-10-18")
dt.history(5)
dt.optimize.compact()
dt.vacuum(retention_hours=168, dry_run=False)
(dt.merge(source=updates, predicate="t.id = s.id", source_alias="s", target_alias="t")
   .when_matched_update_all().when_not_matched_insert_all().execute())
```
No JVM; good for Lambda/containers and small/medium writes. Ran locally with `deltalake` 1.6.6: append with `partition_by`, `history`, `optimize.compact()` (returns a metrics dict), `vacuum(retention_hours=168, dry_run=False)` (returns the deleted-file list, empty here), `merge` with `t`/`s` aliases (returns a metrics dict) and `protocol()` (`ProtocolVersions(min_reader_version=1, min_writer_version=2, ...)` for a plain table). `to_pyarrow_dataset().to_table(filter=...)` worked.

## OSS Spark
```bash
# docs quick-start uses 4.0.0 (Scala 2.13); match your Spark version in the release matrix
pyspark --packages io.delta:delta-spark_2.13:<version> \
  --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
  --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog
```

## Readers
DuckDB `delta_scan('s3://...')` (counted 5 rows on the local table above) and Polars `pl.scan_delta` (shape (5, 3)) both read the delta-rs table. For Trino/Starburst, Athena, Redshift Spectrum and Snowflake, check each vendor's current Delta support docs (not checked here).

## Compatibility
- Check table **protocol and features** (`minReaderVersion`, `minWriterVersion`, features like deletion vectors, column mapping, liquid clustering, V2 checkpoints). Databricks-written tables may use features a given reader does not support yet.
- **UniForm** (Iceberg metadata generated alongside Delta) widens reader compatibility.

## Concurrency on S3
Concurrent writers need a commit coordination mechanism on S3 (no atomic put-if-absent historically): delta-rs supports a DynamoDB locking provider (`AWS_S3_LOCKING_PROVIDER` set to `dynamodb`, plus `DELTA_DYNAMO_TABLE_NAME`; the table must exist and the role needs GetItem/Query/PutItem/UpdateItem) or `AWS_S3_ALLOW_UNSAFE_RENAME=true` (unsafe, single writer only); the delta-rs docs also list an `aws_conditional_put` option (e.g. `etag`). Single-writer designs avoid the issue. For Unity Catalog-managed tables follow Databricks's current guidance on external writers. The concurrent-append test was not run (no S3/DynamoDB here).

## Maintenance
Without Databricks predictive optimization you must schedule compaction (`optimize.compact`/`z_order`), checkpointing and vacuum yourself.

## Verify
A table written by delta-rs is readable by Spark and DuckDB with equal counts; concurrent append test with the locking provider produces no lost commits.
