---
id: computing-software.data-engineering.etl-pipeline-design.salesforce-bulk-api-extraction
name: salesforce-bulk-api-extraction
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, salesforce-bulk-api, source-systems, soql, pk-chunking, api-limits, deleted-records]
level: advanced
status: docs-checked
description: "Extract Salesforce data at scale with Bulk API 2.0 query jobs: incremental SOQL, unsupported query features, result paging, limit budgeting and formula field pitfalls."
sources:
  - https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/queries.htm
  - https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/salesforce_app_limits_platform_bulkapi.htm
  - https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Salesforce extraction with Bulk API 2.0

**Goal:** incremental, complete extraction of Salesforce objects (including deletes) within API limits, when a managed connector is not an option or needs debugging.

## Incremental query
```sql
SELECT Id, AccountId, StageName, Amount, CloseDate, IsDeleted, SystemModstamp, LastModifiedDate
FROM Opportunity
WHERE SystemModstamp > 2026-10-17T00:00:00Z
```
- Filter on a last-change timestamp field and keep a watermark per object. Look up in the Object Reference which timestamp (SystemModstamp or LastModifiedDate) moves for the kinds of change you must capture; this skill did not verify that.
- Keep an overlap on the watermark (a few minutes) and dedupe by `Id` plus the timestamp.
- Avoid `LIMIT` and `ORDER BY` on extract queries: they disable PK chunking, so queries run longer and can time out.

## Bulk API 2.0 query flow
A query job is created with `POST /services/data/vXX.X/jobs/query`. Query jobs need API version 47.0 or later. Supported calls on `/services/data/vXX.X/jobs/query`:

| Call | Purpose |
|---|---|
| POST `.../jobs/query` | create a query job |
| GET `.../jobs/query` | info on all query jobs in the org |
| GET `.../jobs/query/<queryJobId>` | info on one job |
| GET `.../jobs/query/<queryJobId>/results` | fetch results |
| PATCH `.../jobs/query/<queryJobId>` | abort the job |
| DELETE `.../jobs/query/<queryJobId>` | delete the job |

- Jobs are asynchronous: poll the job-info call until the job finishes, then fetch results. The results response body is always compressed.
- Bulk API 2.0 chunks large query jobs itself for objects that support it (custom objects, and Sharing and History tables that support standard objects). The `isPkChunkingSupported` field in the job-info response tells you whether an object supports PK chunking. You do not configure batches.
- The API retries automatically. If the message says it retried more than 15 times, add filter criteria and retry.
- The client can page through the full result set using the `locator` and `maxRecords` query parameters of the results call; it is not bound to a fixed set of files.
- Job results can be retrieved within 7 days of job completion; jobs in a terminal state older than 7 days are deleted.

## Query features Bulk API 2.0 does not support
- `GROUP BY`, `OFFSET` and `TYPEOF` clauses; aggregate functions such as `COUNT()`; date functions in `GROUP BY` (date functions in `WHERE` are fine).
- Compound address or geolocation fields: query the component fields instead.
- Parent-to-child relationship queries (child-to-parent is supported).
SOQL also has no arbitrary joins, wildcards in field lists, or calculation expressions, so select explicit fields and join in the warehouse.

## Deletes
Soft-deleted and purged records need separate handling from the incremental query. Check the Bulk API 2.0 and REST API references for the deleted-record options (not covered by the pages read for this skill), and periodically reconcile full Id lists to catch rows you missed.

## Limits budgeting
- Bulk API 2.0 query jobs: 10,000 query jobs per rolling 24 hours and 1 TB total query results per rolling 24 hours. Current usage is in `DailyBulkV2QueryJobs` and `DailyBulkV2QueryFileStorageMB` in the response of the REST limits method (`/vXX.X/limits/`).
- Query jobs do not consume the 15,000-batches-per-24-hours allocation (only ingest jobs do).
- Maximum retrieved file size is 1 GB, and the timeout for retrieving query results is 20 minutes.
- Schedule large full extracts off-hours; prefer incremental.

## Pitfalls
- Formula fields and roll-ups can change without the record's timestamp moving; recompute them in the warehouse from source fields or periodically full-refresh those columns.
- The integration user only sees fields it has permission to; use a dedicated integration user with a documented permission set.
- `describe` the object each run to detect new or removed fields (schema drift).

## Verify
- [ ] Row counts per object reconcile with a count taken another way (and with IsDeleted handling).
- [ ] API usage per day stays under an agreed share of the limits above.

## Checked
Checked 2026-11-08 against the Bulk API 2.0 Query page (supported URIs, chunking, unsupported SOQL), the Bulk API limits and allocations page (query job and result limits, retries, retrieval timeout, results lifespan) and the SOQL overview page (no joins, wildcards or expressions). Removed unconfirmed claims: the specific CSV curl example and headers, Recycle Bin and getDeleted windows, queryAll semantics, SystemModstamp indexing, the org-wide REST limit field name, field-level-security behaviour. The pages are the stripped text of the docs, not the full guides.
Method: documentation only; no commands were run.
