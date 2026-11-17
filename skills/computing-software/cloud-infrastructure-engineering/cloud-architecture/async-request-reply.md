---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.async-request-reply
name: async-request-reply
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, async-request-reply, http-202, polling, status-endpoint, long-running-operations, webhooks, callback, retry-after, location-header]
level: practitioner
status: docs-checked
description: "Expose long-running work over HTTP with 202 Accepted plus a status endpoint: Location and Retry-After headers, job store, polling vs callbacks, expiry and client behaviour."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/async-request-reply", "https://www.rfc-editor.org/rfc/rfc9110#name-202-accepted", "https://google.aip.dev/151"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asynchronous request-reply

**When:** the back end runs work for seconds to minutes, so the client cannot wait on the same connection
(see Azure's Asynchronous Request-Reply pattern). Polling suits clients that cannot receive callbacks
(browsers, firewalled callers). Prefer callbacks, WebSockets/SignalR or a notification service when they are available.

## Protocol
1. `POST /reports` → validate synchronously (reply 400 immediately if invalid), offload to a queue, return
   **202 Accepted** with `Location: /reports/jobs/{id}` (the status endpoint to poll) and `Retry-After`
   (estimated completion time, so clients poll less).
   A 202 means accepted for processing, not completed; HTTP has no facility to re-send the final status code,
   so the outcome must be exposed on the status resource.
2. `GET /reports/jobs/{id}` → `200` with a status body while working. Suggested fields: `status`
   (Pending, Running, Succeeded, Failed, Canceled), `createdAt`, `lastUpdatedAt`, optional `percentComplete`, and a
   structured `error` object when Failed (consider RFC 9457 Problem Details).
3. On completion the status endpoint returns `303 See Other` with `Location` pointing at the result. Use 303
   rather than 302: 303 tells the client to GET the result, whereas some clients replay the original method
   on 302 and could duplicate a POST. The result resource then returns 200, 201 or 204.
4. Optional: a dedicated status endpoint avoids the ambiguity of polling the target URL, where 404 means both
   "not created yet" and "invalid id". Allow cancel via `DELETE` on the status resource.
5. Google AIP-151 "long-running operations" is a well-specified variant: methods return a
   `google.longrunning.Operation` that the client can poll; it suggests about 10 seconds as a rule of thumb for
   "a significant amount of time" and about 30 days for operation expiry.

## Implementation
- Durable job record (id, status, createdAt, lastUpdatedAt, result pointer); authorise status reads by owner
  (job ids leak otherwise).
- **Idempotency key** (for example an `Idempotency-Key` header) on the POST: a duplicate key returns the existing
  status resource instead of enqueuing a second job.
- Define a retention policy for status resources and results; an `Expires` header on the status response can tell
  clients the window.
- `lastUpdatedAt` lets clients tell stalled from in-progress; consider marking jobs Failed if a worker dies.
- A client you control can follow `Location` and `Retry-After` exactly; clients others write (for example low-code
  tools) may handle 202 their own way.

## Gotchas
- Clients ignoring `Retry-After` hammer the status endpoint; rate-limit it and cache responses briefly.
- 202 then the job silently vanishes from the queue (DLQ) → status stuck at pending; add a sweeper that
  marks stale jobs failed.
- Services vary: Azure Resource Manager uses a modified variant of this pattern with different headers.

## Verify
- [ ] The client never waits on one open connection for a 10-minute job.
- [ ] Repeat POST with same idempotency key returns the same job id.
- [ ] Kill the worker: job turns `failed` within your chosen timeout.

## Checked
2026-11-08. Confirmed against the Azure Architecture Center pattern page (read through the example section: 202,
Location, Retry-After, status fields, 303 vs 302, RFC 9457, retention and Expires, DELETE cancel, idempotency key,
when not to use), RFC 9110 section on 202 (searched for the 202 and 303 definitions rather than read end to end)
and Google AIP-151 (Operation, 10 second and 30 day rules of thumb). Removed unsupported claims: gateway and load
balancer timeout figures, HMAC-signed webhooks, `410 Gone`, CORS exposure, the 24 h expiry example.
Method: documentation only; no commands were run.
