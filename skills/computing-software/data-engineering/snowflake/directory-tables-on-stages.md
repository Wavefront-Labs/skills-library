---
id: computing-software.data-engineering.snowflake.directory-tables-on-stages
name: directory-tables-on-stages
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, directory-tables, stages, unstructured-data, file-catalog]
level: practitioner
status: docs-checked
description: "Catalogue files on Snowflake stages with directory tables: enabling, auto refresh, querying file metadata, streams on stages, and file URLs for unstructured data."
sources:
  - https://docs.snowflake.com/en/user-guide/data-load-dirtables
  - https://docs.snowflake.com/en/user-guide/data-load-dirtables-auto
  - https://docs.snowflake.com/en/user-guide/unstructured-intro
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Directory tables on stages

**Goal:** query the list of files on a stage (paths, sizes, timestamps) like a table, and react to new files.

## Enable
```sql
CREATE STAGE docs_stage
  URL = 's3://acme-docs/contracts/' STORAGE_INTEGRATION = s3_int
  DIRECTORY = (ENABLE = TRUE AUTO_REFRESH = TRUE);
-- internal stage
CREATE STAGE uploads DIRECTORY = (ENABLE = TRUE) ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
ALTER STAGE uploads REFRESH;          -- manual sync of the metadata
```
AUTO_REFRESH on external stages relies on the cloud provider's event notifications (see CREATE STAGE); `ALTER STAGE ... REFRESH` syncs the metadata manually.

## Query
```sql
SELECT relative_path, size, last_modified, file_url
FROM DIRECTORY(@docs_stage)
WHERE relative_path ILIKE '%.pdf' AND last_modified > dateadd('day', -1, current_timestamp());
```
Join with processing results to find unprocessed files.

## React to new files
```sql
CREATE STREAM docs_changes ON STAGE docs_stage;
CREATE TASK process_docs WAREHOUSE = etl_wh WHEN SYSTEM$STREAM_HAS_DATA('docs_changes')
AS INSERT INTO doc_queue SELECT relative_path FROM docs_changes WHERE metadata$action = 'INSERT';
```

## File URLs
- `BUILD_SCOPED_FILE_URL`, `BUILD_STAGE_FILE_URL` and `GET_PRESIGNED_URL` generate scoped, file and pre-signed URLs; see the unstructured data introduction for how they differ.

## Gotchas
- Internal stages used with pre-signed, file or scoped URLs are created with `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')` (unstructured data docs).
- Directory metadata lags until refresh; auto-refresh notifications can be delayed.

## Verify
Upload a file; after refresh (or notification), it appears in `DIRECTORY(@stage)` and in the stream.

## Checked
2026-10-28. Confirmed against CREATE STAGE (DIRECTORY = (ENABLE, AUTO_REFRESH, REFRESH_ON_CREATE), SNOWFLAKE_SSE), CREATE STREAM (ON STAGE, directory table streams with METADATA columns and RELATIVE_PATH, SIZE, LAST_MODIFIED, MD5, FILE_URL), the triggered tasks page and the unstructured data page (BUILD_SCOPED_FILE_URL, BUILD_STAGE_FILE_URL, GET_PRESIGNED_URL, SNOWFLAKE_SSE). Removed: the directory_notification_channel column, URL lifetime and privilege descriptions, UDF and Cortex remark and the serverless credit claim.
Method: documentation only; no commands were run.
