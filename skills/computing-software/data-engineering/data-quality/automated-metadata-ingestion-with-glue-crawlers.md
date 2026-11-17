---
id: computing-software.data-engineering.data-quality.automated-metadata-ingestion-with-glue-crawlers
name: automated-metadata-ingestion-with-glue-crawlers
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, glue-data-catalog, glue-crawlers, metadata-ingestion]
level: practitioner
status: docs-checked
description: "Populate a catalog automatically with AWS Glue crawlers: classifiers, table and partition grouping, incremental crawls, schema-change handling, with gotchas."
sources:
  - https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html
  - https://docs.aws.amazon.com/glue/latest/dg/crawler-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated metadata ingestion with Glue crawlers

**Goal:** a catalog that reflects what actually exists in storage without manual table registration.

## How a crawler works
1. Runs your custom classifiers in the order you set; the first to recognise the data creates the schema and the rest are skipped. If none match, built-in classifiers (JSON, CSV, Avro and others) try.
2. Connects to the data store (some need connection properties) and infers a schema.
3. Groups data into tables or partitions using crawler heuristics.
4. Writes metadata to the Data Catalog: a table in a database (the default database if none is specified), with a `classification` attribute naming the classifier that recognised it.
- A crawler can crawl multiple data stores in one run, and on repeat runs it looks for new or changed files and tables.
- Compressed files must be downloaded to be processed. For formats that compress internally (Parquet) the compressionType property is not set; for whole-file compression (gzip) it is.
- Generated table names allow only alphanumerics and underscore; prefix up to 64 characters, name up to 128; duplicates get a hash suffix.

## Tables vs partitions on S3
You give an Include path. When most schemas at a folder level are similar, the crawler creates partitions of one table rather than separate tables (for example `year=/month=/day=` folders under one prefix become one table with three partition keys). Two sibling table folders with similar schemas under one Include path become a single table with extra partition columns. To force separate tables, add each table's root folder as its own data store in the crawler.

Athena treats each table as one S3 prefix; different schemas under one prefix are not recognised as separate tables and can yield zero results, so use a separate Include path per schema.

## Customisation options
- Incremental crawls: add only new partitions.
- Partition indexes: created by default for S3 and Delta Lake targets.
- S3 event notifications: identify changes between crawls by listing only the subfolder that triggered the event, instead of the full target.
- Schema changes: configure the crawler (console or API) so it does not change an existing schema.
- Single schema per S3 path when data is compatible; table location and partition-level setting; table threshold (maximum tables the crawler may create); Lake Formation credentials.

## Gotchas
- One folder of inconsistent files can produce unexpected tables or partitions; keep layouts consistent and set the table location level or separate data stores.
- Lock down schema changes for tables used by production jobs.

## Verify
A new S3 partition appears in the catalog after the next run, and no unintended schema updates occurred.

## Checked
Method: docs-only read on 2026-11-09 of both AWS Glue pages in full as text. The DataHub page returned only a short shell, so that source, the DataHub recipe and the OpenMetadata/DataHub connector section were removed. Also removed as unstated on the pages: the create-crawler CLI example and its parameter values, CombineCompatibleSchemas, LOG/CRAWL_NEW_FOLDERS_ONLY option names, grok/CSV header notes, and type-inference claims.
