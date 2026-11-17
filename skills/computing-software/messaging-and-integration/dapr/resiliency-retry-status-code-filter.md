---
id: computing-software.messaging-and-integration.dapr.resiliency-retry-status-code-filter
name: resiliency-retry-status-code-filter
category: computing-software
field: messaging-and-integration
product: dapr
tags: [resiliency, retries, matching, httpstatuscodes, grpcstatuscodes, status-codes, filter]
level: advanced
status: docs-checked
description: "Limit Dapr retries to chosen HTTP and gRPC status codes with matching.httpStatusCodes and gRPCStatusCodes, which codes the page says to retry or not, and the malformed-value log."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/resiliency/policies/retries/retries-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a retry policy retries any failure. The `matching` block narrows it to listed codes; codes not listed are not retried.

```yml
spec:
  policies:
    retries:
      retry5xxOnly:
        policy: constant
        duration: 5s
        maxRetries: 3
        matching:
          httpStatusCodes: "429,500-599" # retry the HTTP status codes in this range. All others are not retried. 
          gRPCStatusCodes: "1-4,8-11,13,14" # retry gRPC status codes in these ranges and separate single codes.
```

Format: a comma-separated string of single codes and ranges. HTTP values are 100-599; gRPC values 0-16.

Guidance table from the page. HTTP: do not retry 404 (resource missing), 400 (invalid request), 401 (get new credentials). Retry 408, 429 (respect `Retry-After` if present), 500, 502, 503, 504. gRPC: do not retry CANCELLED (1), INVALID_ARGUMENT (3), NOT_FOUND (5); retry DEADLINE_EXCEEDED (4), RESOURCE_EXHAUSTED (8), UNAVAILABLE (14), with backoff.

Note the page itself uses two different gRPC strings in its examples (`1-4,8-11,13,14` and `4,8-11,13,14`) while its table recommends not retrying 1 and 3; pick the list deliberately rather than copying.

A badly formatted value is not fatal: Dapr logs "Could not read resiliency policy" and the `daprd` startup sequence proceeds. The page does not say which retry behaviour applies in that case.

## Checked

2026-11-08. matching block, value formats and ranges, the HTTP and gRPC guidance tables, the differing gRPC example strings and the malformed-value log confirmed on the Retry resiliency policies page. Changed: removed advice that a typo silently drops the filter, which the page does not state.

Method: documentation only; every cited page read in full; no commands were run.
