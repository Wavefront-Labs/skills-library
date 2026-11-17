---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-import-from-s3
name: dynamodb-import-from-s3
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-import-from-s3, dynamodb-import-export, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Create a new table from files in S3 with no write capacity use."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataImport.HowItWorks.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Import from S3

**Goal:** Create a new table from files in S3 with no write capacity use.

## Steps
- aws dynamodb import-table --s3-bucket-source S3Bucket=my-bucket,S3KeyPrefix=data/ --input-format CSV --table-creation-parameters file://table.json
- Formats: CSV, DYNAMODB_JSON, ION; GZIP, ZSTD or no compression.
- Import always creates a new table; it cannot load into an existing one, and it uses no write capacity.
- Errors are logged to CloudWatch Logs.

## Gotcha
Items failing validation are skipped and logged, and the import then ends FAILED with ItemValidationError; read the log before cutting over.

## Verify
- [ ] describe-import shows COMPLETED, ErrorCount 0 and the item count equals the source row count.

## Checked
Checked 2026-11-03 against the import-from-S3 pages and botocore (ImportTable, DescribeImport, S3BucketSource S3Bucket/S3KeyPrefix/S3BucketOwner): formats, compression types, new-table-only, no write capacity and CloudWatch Logs error logging match. Removed the unsupported "error limit stops the import" and corrected the gotcha to the documented skip-and-fail behaviour; resolved the compression "(confirm)".
Method: documentation only; no commands were run.
