---
id: computing-software.software-engineering.api-design.bulk-export-and-import-jobs
name: bulk-export-and-import-jobs
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, bulk-export, data-import-api, long-running-operations, async-jobs, ndjson]
level: advanced
status: draft
description: "Design asynchronous bulk export and import APIs: job resources, polling, NDJSON files in object storage, partial failure reports and idempotent re-runs."
sources: ["https://hl7.org/fhir/uv/bulkdata/export.html", "https://google.aip.dev/151", "https://docs.stripe.com/reports/api"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bulk export and import jobs

Big data sets don't fit synchronous request/response or pagination; model the work as a job.

## Export (pattern used by FHIR Bulk Data, Stripe reports)
1. `POST /exports {"type":"orders","filter":"create_time>=\"2026-01-01\"","format":"ndjson"}`
   -> `202 Accepted`, `Location: /exports/e7` (or an AIP-151 long-running operation).
2. `GET /exports/e7` -> `{"state":"RUNNING","progress":0.4}` ; honour `Retry-After` for polling,
   or send a webhook on completion.
3. Done -> `{"state":"SUCCEEDED","files":[{"url":"https://...signed...","size_bytes":...,"records":...}],
   "expire_time":"..."}`. Files are **NDJSON** (one record per line, streamable) or CSV, gzip,
   split at ~1 GB. URLs are short-lived signed object-storage links.
4. `DELETE /exports/e7` cancels/cleans up.
- Snapshot consistency: export as of a timestamp (`as_of`), so records don't shift mid-export.
- Incremental: `since=<timestamp>` so clients sync deltas instead of full dumps.

## Import
1. Client uploads a file (signed upload URL or multipart) -> `POST /imports {"file":"uploads/u1","mode":"upsert"}`.
2. Validate the whole file first (`dry_run=true` option) and report all errors, not the first.
3. Process in batches; job reports `processed`, `succeeded`, `failed` counts and an **error file**
   (line number + error code + message) the client can fix and resubmit.
4. Idempotency: each row carries an external id; import = upsert by external id, so re-running a
   failed job doesn't duplicate. Accept an `Idempotency-Key` on job creation.
- Decide atomicity explicitly: all-or-nothing (stage then swap) vs best-effort per row.

## Operations
Quotas per tenant (concurrent jobs, rows/day), run jobs on a separate worker pool so exports don't
starve online traffic, and audit-log who exported what (exports are a data-exfiltration path).
