---
id: computing-software.data-engineering.trino.trino-fault-tolerant-exchange-manager
name: trino-fault-tolerant-exchange-manager
category: computing-software
field: data-engineering
product: trino
tags: [exchange-manager, exchange-spooling, exchange-base-directories, s3-spooling, hdfs-spooling]
level: advanced
status: docs-checked
description: "Configure the Trino exchange manager that spools FTE data to S3, GCS, Azure Blob Storage, HDFS or a local directory, with its tuning properties."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/fault-tolerant-execution.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino fault tolerant exchange manager

Exchange spooling stores intermediate data for fault-tolerant execution. Create `etc/exchange-manager.properties` on the coordinator and every worker (or point `exchange-manager.config-file` in `config.properties` elsewhere), set `exchange-manager.name` to `filesystem` or `hdfs`, and list locations in `exchange.base-directories`.

AWS S3 (any S3-compatible store; only AWS S3 and MinIO are tested):

```properties
exchange-manager.name=filesystem
exchange.base-directories=s3://exchange-spooling-bucket
exchange.s3.region=us-west-1
exchange.s3.aws-access-key=example-access-key
exchange.s3.aws-secret-key=example-secret-key
```

If a query fails with "Please reduce your request rate", list several buckets, comma-separated, to spread the I/O.

Other targets:
- Azure: use Blob Storage, not Data Lake Storage. `exchange.base-directories=abfs://container_name@account_name.dfs.core.windows.net` plus `exchange.azure.connection-string` or `exchange.azure.endpoint`.
- GCS: `gs://` base directory, `exchange.s3.endpoint=https://storage.googleapis.com`, HMAC keys as the access and secret keys, and `exchange.gcs.json-key-file-path` or `exchange.gcs.json-key`.
- HDFS: `exchange-manager.name=hdfs`, a base directory such as `hadoop-master:9000/exchange-spooling-directory`, and `hdfs.config.resources`. For Hadoop-compatible filesystems enable `exchange.hdfs.skip-directory-scheme-validation`.
- Local directory: only for standalone non-production clusters unless shared across all nodes.

Tuning defaults: `exchange.max-page-storage-size` `16MB`, `exchange.sink-buffer-pool-min-size` `10`, `exchange.sink-buffers-per-partition` `2`, `exchange.sink-max-file-size` `1GB`, `exchange.source-concurrent-readers` `4`, `exchange.s3.max-error-retries` `10`, `exchange.s3.upload.part-size` `5MB`. Compression defaults to `LZ4` here. Add a bucket lifecycle rule to expire objects abandoned by node crashes.

## Checked

2026-11-04. Read against the Trino docs page `admin/fault-tolerant-execution.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
