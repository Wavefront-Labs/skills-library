---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-table-bucket-iceberg-catalog
name: s3-table-bucket-iceberg-catalog
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [iceberg-rest-catalog, table-bucket, lakehouse, iceberg, rest-catalog]
level: advanced
status: docs-checked
description: "Run an Iceberg REST catalog on SeaweedFS table buckets: port 8181, catalog equals bucket, auth methods per engine and the s3tables.bucket command."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Table-Bucket
  - https://github.com/seaweedfs/seaweedfs/wiki/SeaweedFS-Iceberg-Catalog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 table bucket iceberg catalog

A table bucket holds Iceberg tables and doubles as the catalog, so Spark, Trino, Dremio, DuckDB, Doris, RisingWave and OLake Go can use SeaweedFS as both catalog and storage, with no Hive Metastore or Glue.

```bash
weed mini                                    # S3 on 8333, Iceberg REST on 8181
weed shell
> s3tables.bucket -create -name my-catalog
```
Mapping: the URI `http://localhost:8181/v1/my-catalog/` maps to the table bucket `my-catalog`. Without a prefix (`http://localhost:8181/v1/`) the bucket `warehouse` is used. One bucket is one catalog, so create several for independent catalogs.

Auth by engine: SigV4 (Spark, Trino, RisingWave), OAuth2 (DuckDB, Doris, OLake Go), unsigned REST plus S3 keys (Dremio). The same S3 bucket policies and IAM apply.

Iceberg REST port flag: `-s3.port.iceberg` with `weed mini`, `--port.iceberg` standalone (default 8181); S3 is on 8333. Without IAM configuration (for example `weed mini` with no `-s3.config`) the catalog allows anonymous access by default.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki pages S3 Table Bucket (no Hive Metastore or Glue) and SeaweedFS Iceberg Catalog (ports, URI to bucket mapping, default `warehouse` bucket, auth per engine, port flags, anonymous default). Fixed the port flag (`-iceberg.port` is not on the page); removed the Admin UI and weed server claims and the Verify line.
Method: documentation only; no commands were run.
