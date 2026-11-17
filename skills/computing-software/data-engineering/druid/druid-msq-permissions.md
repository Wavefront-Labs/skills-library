---
id: computing-software.data-engineering.druid.druid-msq-permissions
name: druid-msq-permissions
category: computing-software
field: data-engineering
product: druid
tags: [msq, permissions, extern, read-datasource, write-datasource, authorization]
level: advanced
status: docs-checked
description: "Grant the permissions MSQ needs for SELECT, INSERT, REPLACE and EXTERN."
sources:
  - https://github.com/apache/druid/blob/master/docs/multi-stage-query/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All authenticated users can reach the MSQ task engine through UI and API, but without extra permissions they cannot read or write datasources or external data.

Required permissions:
- SELECT from a datasource: READ on that datasource.
- INSERT or REPLACE into a datasource: WRITE and READ on the target. If `druid.sql.planner.authorizeTableVisibility = false`, only WRITE is needed.
- EXTERN and input-source table functions: READ on a resource named EXTERNAL of type EXTERNAL. Users without it get a 403 error.

Once submitted, a query runs as a `query_controller` task. These are Overlord tasks and follow the Overlord security model, so users with Overlord API access can do some things for queries they did not submit, including retrieving status or cancelling them. Plan Overlord permissions with that in mind.

Any user with Overlord API access can submit `query_controller` tasks with only the WRITE DATASOURCE permission.

The page also lists these extra requirements: INSERT or REPLACE queries need READ permission on the output datasource, and SELECT queries need READ permission on the `__query_select` datasource, a stub datasource that gets created.

Durable storage permissions: when MSQ stores intermediate files in Amazon S3 it needs `s3:GetObject` (plus read permission on the object), `s3:PutObject`, `s3:AbortMultipartUpload` and `s3:DeleteObject`. For Azure Blob Storage it needs the `Microsoft.Storage/storageAccounts/blobServices/containers/blobs` operations `read`, `write`, `add/action` and `delete`.

## Checked

2026-11-08. Read multi-stage-query/security.md in full. Added the output datasource and __query_select requirements, the Overlord API note and the S3 and Azure durable storage permissions.

Method: documentation only; no commands were run.
