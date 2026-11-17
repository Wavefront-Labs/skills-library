---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.retry-decisions-under-overload
name: retry-decisions-under-overload
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [retry-decisions, retry-on-overload, retries, handling-overload, overloaded-dont-retry, exponential-backoff]
level: practitioner
status: docs-checked
description: "Decide when clients retry: per-request caps, per-client retry budget, retry at one layer only, and an 'overloaded; don't retry' signal to stop amplification."
sources: ["https://sre.google/sre-book/handling-overload/", "https://sre.google/sre-book/addressing-cascading-failures/", "https://grpc.io/docs/guides/retry/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deciding when to retry on overload

SRE Book "Handling Overload" rules for retries when a backend rejects for overload:
1. **Per-request retry budget**: at most three attempts for one request; after that the failure bubbles up to the caller.
2. **Per-client retry budget**: each client tracks the ratio of its requests that are retries and retries only while that
   ratio is below 10%. In the book's worst case this reduces growth from just under 3x to 1.1x.
3. **Retry at one layer only**: retry only at the layer immediately above the one rejecting. If that layer gives up, it
   returns an "overloaded; don't retry" error (or a degraded response) so upper layers do not multiply the attempts
   (the book calls the alternative a combinatorial retry explosion).

## Decision table
| Response | Retry? |
|---|---|
| Task-level "task overloaded" from one backend | yes, on a different backend task, within the per-request and per-client budgets |
| "overloaded; don't retry" | no; propagate failure or return a degraded response |
| Permanent errors, malformed requests | no; they will never succeed |

## Signalling "don't retry"
The Cascading Failures chapter says to return a specific status when overloaded so clients and other layers back off and
do not retry. The Handling Overload chapter describes one way to decide: clients put an attempt counter in request
metadata, backends keep histograms of it, and a backend that sees many retries returns "overloaded; don't retry" instead
of the standard "task overloaded". The book does not prescribe header or status names; define your own and document them.

## Implementation notes
- Use randomized exponential backoff and cap retries per request (Cascading Failures chapter).
- gRPC service config has `retryPolicy` (`maxAttempts`, `initialBackoff`, `maxBackoff`, `backoffMultiplier`,
  `retryableStatusCodes`) and `retryThrottling` (`maxTokens`, `tokenRatio`). The client keeps a token count per server;
  failed RPCs decrement it, successes add `tokenRatio`, and retries pause when it falls below half of `maxTokens`.
  Read the gRPC retry guide for the exact JSON layout and the jitter it applies.

## Gotchas
- Retries hide problems from dashboards; the book notes that graphs of retry rates can be mistaken for a symptom rather
  than a compounding cause. Export per-attempt metrics and a retry ratio.
- Mesh or SDK retries count toward amplification; check what your stack retries by default.

## Verify
- [ ] Amplification test: overload a backend, measure backend request rate against client request rate; it should stay near the 1.1x the budget is designed for.
- [ ] Only one layer retries (trace shows retries at a single hop).

## Checked
2026-11-01. Confirmed against the SRE Book chapters "Handling Overload" (retry budgets of three attempts and 10%, the 3X
and 1.1x worst case, retry only at the layer above, "overloaded; don't retry", attempt-counter histograms), "Addressing
Cascading Failures" (randomized exponential backoff, per-request limit, specific overload status, retry-rate graphs) and
the gRPC retry guide (policy fields, token-based throttling). Removed: the status table rows for 429, DEADLINE_EXCEEDED,
connection refused and idempotent writes, the sample header names, the Istio default, the sliding-minute window.
Method: documentation only; no commands were run.
