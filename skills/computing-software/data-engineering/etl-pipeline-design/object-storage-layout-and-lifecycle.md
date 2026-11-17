---
id: computing-software.data-engineering.etl-pipeline-design.object-storage-layout-and-lifecycle
name: object-storage-layout-and-lifecycle
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, file-formats, object-storage-layout, s3, gcs, adls, lifecycle-policies, storage-classes, small-files]
level: practitioner
status: docs-checked
description: "Lay out data lakes on S3, GCS or ADLS: prefix and directory design, file sizing, request rates, lifecycle rules, storage classes and versioning pitfalls."
sources:
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html
  - https://cloud.google.com/storage/docs/lifecycle
  - https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-best-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Object storage layout and lifecycle

**Goal:** a lake whose paths are predictable, whose files are efficient to read, and whose storage bill doesn't grow forever with data nobody reads.

## 1. Buckets and prefixes
- Separate buckets (or containers/accounts) per **environment** and per **sensitivity/access boundary** (`acme-lake-prod-raw`, `acme-lake-prod-curated`, `acme-lake-prod-restricted`) so access control, encryption and lifecycle are easy to reason about per bucket. This is design advice, not a vendor requirement.
- Within: `<layer>/<domain>/<dataset>/<partition>=<value>/file`, e.g. `raw/sales/orders/ingest_date=2026-10-16/part-0001.parquet`.
- Plan the layout up front: Azure's guidance is that file format, file size and directory structure all affect performance and cost. It suggests parent directories for region and subject matter with date and time below them, so ACLs can secure the parents; putting the date first makes that much harder and multiplies directories over time.
- A batch layout with `In`, `Out` and `Bad` folders per source, each with date folders below, gives a place to quarantine files that fail processing. When output goes straight into a Hive table or database you do not need `In` and `Out`.
- Name time-series files and folders consistently (for example `/DataSet/YYYY/MM/DD/datafile_YYYY_MM_DD.tsv`); partition pruning on time-series data helps Hive workloads read only a subset.
- Table formats (Delta/Iceberg) manage their own data-file paths; you choose only the table root.

## 2. Partitioning
- Partition by what queries filter on and what lifecycle acts on: usually date, at a granularity that keeps files large.
- Avoid high-cardinality partition keys (`customer_id`): millions of folders and tiny files.
- Partition by **ingest/arrival date** in raw (append-only, easy reprocessing); by business date in curated.

## 3. File sizing and request rates
- Per-file overhead (listing, access checks, metadata operations) makes many small files slow. Azure's Data Lake Storage guidance is to organise data into files of roughly 256 MB to 100 GB, and notes some engines struggle above 100 GB. Reads and writes there are billed in 4 MB increments, so tiny files cost the same per operation as 4 MB files.
- Aggregate small files into larger ones, saved in a read-optimised format such as Parquet; for real-time data, a streaming engine with a message broker can write larger files.
- Parquet and ORC (columnar) suit read-heavy or column-subset queries; Avro (row-based) suits write-heavy or whole-record access such as message buses.
- S3 supports at least 3,500 PUT/COPY/POST/DELETE or 5,500 GET/HEAD requests per second per partitioned prefix, with no limit on the number of prefixes in a bucket. Reads and writes scale by spreading across prefixes (10 prefixes for reads gives up to 55,000 requests per second). Scaling is gradual, and you may see 503 (Slow Down) errors until it completes.

## 4. Lifecycle and storage classes
- **S3 Lifecycle** has transition actions (to another storage class) and expiration actions (S3 deletes expired objects). A new configuration applies to existing objects as well as new ones: an expiration rule queues existing old objects for removal. A bucket policy cannot block a Lifecycle rule's deletes or transitions, even if it denies all principals. Transition requests have costs; there are no retrieval charges for transitions, but per-request ingestion charges apply when moving data into a class. Expiring objects in a class with a minimum storage duration can incur a charge.
- **Cloud Storage Object Lifecycle Management** covers TTL, retaining noncurrent versions and downgrading storage classes. Conditions include age, `matchesStorageClass`, `daysSinceNoncurrentTime`, `isLive` and `numNewerVersions` (the last three are for versioned buckets). `SetStorageClass` and `matchesStorageClass` cannot be used on buckets with Autoclass enabled. An `AbortIncompleteMultipartUpload` action exists for cleaning up incomplete uploads. With versioning, deleting a live object by lifecycle makes it noncurrent, and a rule can then delete the noncurrent version later.
- Check access patterns before tiering data that is still queried.
- **Never** apply lifecycle expiration under Delta/Iceberg table paths: the table format must delete files itself (VACUUM, expire snapshots), otherwise you corrupt tables.
- Versioning protects against accidental deletes; pair it with a rule that expires noncurrent versions or old versions accumulate cost.

## 5. Access and safety
- Grant by prefix or directory through roles and catalog permissions, not long-lived keys.
- On Azure Data Lake Storage, combine Azure RBAC roles with ACLs on directories and files in the hierarchical file system; see the Blob storage security recommendations and the Data Lake Storage access control model articles.

## Verify
- [ ] Path convention documented and followed (lint new prefixes in code review).
- [ ] Average file size per dataset within target; small-file compaction scheduled.
- [ ] Lifecycle rules exist for raw/tmp/old versions and none touch table-format paths.
- [ ] Storage cost by prefix is reviewed quarterly.

## Checked
Checked 2026-11-08: S3 performance overview and S3 lifecycle overview (both read in full), the Azure Data Lake Storage best practices page (lines 18-81 read: ingest, file formats, file size, directory structures; security section skimmed) and the Cloud Storage lifecycle page (searched for actions and conditions, not read end to end). Removed unconfirmed claims: the S3 lifecycle JSON and storage class names, 128 MB-1 GB size target (replaced by Azure's 256 MB to 100 GB), random-prefix remark, Hive partition auto-discovery, ADLS atomic renames and POSIX ACLs, Intelligent-Tiering and Autoclass cost behaviour, S3 account-level security settings. Bucket naming and the Delta/Iceberg warning are design advice.
Method: documentation only; no commands were run.
