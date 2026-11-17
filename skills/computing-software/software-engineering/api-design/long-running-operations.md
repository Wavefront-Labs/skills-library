---
id: computing-software.software-engineering.api-design.long-running-operations
name: long-running-operations
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, pagination, long-running-operations, async-request-reply, aip-151, http-202, polling]
level: practitioner
status: docs-checked
description: "Expose long-running work via an operation resource (AIP-151) or an Azure-style status monitor with 202 Accepted: polling with Retry-After, status, result and error shape."
sources:
  - https://google.aip.dev/151
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md#long-running-operations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Long-running operations

When work takes longer than a reasonable HTTP request (AIP-151 gives 10 seconds as a rule of thumb: video transcoding, report generation, provisioning, bulk imports), do not hold the connection open. Accept the request and return a handle.

## Flow (async request-reply)
```
POST /v1/reports            {"type": "sales", "month": "2026-09"}
202 Accepted
Location: /v1/operations/op_7f2a
Retry-After: 5
{"name": "operations/op_7f2a", "done": false, "metadata": {"progress_percent": 0}}

GET /v1/operations/op_7f2a
200 OK  {"name": "operations/op_7f2a", "done": false, "metadata": {"progress_percent": 40}}

GET /v1/operations/op_7f2a
200 OK  {"name": "operations/op_7f2a", "done": true,
         "response": {"name": "reports/r_91", "download_uri": "..."}}
```
On failure the operation is `done` with an `error` instead of a `response`; the GET itself still succeeds and the error describes the work's failure.

## Operation resource (AIP-151 `google.longrunning.Operation`)
- AIP-151: the method must carry a `google.longrunning.operation_info` annotation defining both the response and metadata types; metadata carries progress and similar information on each `GetOperation` call; changing either type is a breaking change.
- A finished operation has `done: true` and a `response`; non-terminal errors can go in the metadata message.
- Azure style: a status monitor with `status` of `NotStarted` or `Running` (non-terminal) and `Succeeded`, `Failed` or `Canceled` (terminal); `Failed` carries an `error` with code and message, and `Succeeded` carries `result`. The 202 response includes an `Operation-Location` header, and the client waits at least the `Retry-After` interval between polls.

## Design rules
- Azure guidelines: even when the work completes before the response, still return 202 Accepted with the status property in the terminal state, so clients code one path.
- `Retry-After` guides polling; clients use backoff and a max wait.
- Make the initiating request idempotent so a retried POST does not start duplicate jobs (Azure: an Operation-Id that matches an existing operation with the same content is treated as a retry; different content is a 409-Conflict).
- Persist operation state durably (not in memory on one instance).
- Keep completed operations for a documented retention period.
- Offer a webhook/callback for clients that do not want to poll; still keep the operation resource as source of truth.
- Authorise reads of the operation the same as the resulting resource.

## Verify
- [ ] Client SDK or test polls to completion, handles failure and cancellation.
- [ ] Duplicate POST with the same idempotency key returns the same operation.
- [ ] Worker crash mid-job: operation eventually fails or resumes, never stays `done: false` forever (timeout sweeper).

## Checked
2026-11-01. Confirmed: AIP-151 (operation_info annotation, metadata, done/response, 10-second rule of thumb); Azure ConsiderationsForServiceDesign long-running operations (status monitor values, Operation-Location, Retry-After, 202 even if finished, Operation-Id retry and 409). Removed: Google-style Cancel/List/Wait/Delete method list, error code 13, 7-day retention example.
Method: documentation only; no commands were run.
