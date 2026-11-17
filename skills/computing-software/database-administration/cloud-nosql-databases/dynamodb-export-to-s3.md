---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-export-to-s3
name: dynamodb-export-to-s3
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-export-to-s3, dynamodb-import-export, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Export table data for analytics without using read capacity."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataImport.HowItWorks.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export to S3

**Goal:** Export table data for analytics without using read capacity.

## Steps
- Requires PITR enabled. aws dynamodb export-table-to-point-in-time --table-arn TABLE_ARN --s3-bucket my-bucket --export-format DYNAMODB_JSON
- Formats are DYNAMODB_JSON and ION; full and incremental exports are available (ExportType FULL_EXPORT or INCREMENTAL_EXPORT).
- Exports use no read capacity; the data in S3 can be queried with Athena.
- Full exports are charged by table size.

## Gotcha
The export is a snapshot from the chosen time, not live; plan reruns for freshness.

## Verify
- [ ] list-exports shows COMPLETED and Athena row counts match the table at export time.

## Checked
Checked 2026-11-03 against the export-to-S3 pages and botocore (ExportTableToPointInTime, ListExports): PITR requirement, formats, incremental export type, no read capacity use and Athena mention match. Resolved the incremental "(confirm)"; replaced "per GB exported" with the documented table-size charge and dropped the unconfirmed "compressed files with a manifest" detail.
Method: documentation only; no commands were run.
