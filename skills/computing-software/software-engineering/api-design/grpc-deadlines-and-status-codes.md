---
id: computing-software.software-engineering.api-design.grpc-deadlines-and-status-codes
name: grpc-deadlines-and-status-codes
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, grpc-deadlines, grpc-status-codes, deadline-propagation, error-details, google-rpc-status, retries, cancellation]
level: practitioner
status: docs-checked
description: "Set and propagate gRPC deadlines, map failures to the right status codes, attach rich error details, and configure retries only for safe codes."
sources: ["https://grpc.io/docs/guides/deadlines/", "https://grpc.io/docs/guides/status-codes/", "https://google.aip.dev/193", "https://grpc.io/docs/guides/retry/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC deadlines and status codes

**Goal:** calls that fail fast and informatively instead of hanging forever or returning
UNKNOWN for everything.

## Deadlines
gRPC sets no deadline by default: without one a client can wait effectively forever.
```go
ctx, cancel := context.WithTimeout(ctx, 300*time.Millisecond)
defer cancel()
resp, err := client.GetInvoice(ctx, req)
```
- Servers: check `ctx.Err()` / `ctx.Done()` in long work and stop when the deadline
  passes; pass the SAME context to downstream calls so the remaining budget propagates
  (gRPC converts the deadline to a timeout with elapsed time deducted, so clock skew does not matter).
- Choose per-RPC deadlines from what you know of network latency and server processing time, validated by load testing, not one global value.
- Exceeded deadline -> `DEADLINE_EXCEEDED` on the client; the server may still be
  working, so non-idempotent operations need idempotency keys.

## Status code choice
| Situation | Code |
|---|---|
| Bad input (validation) | `INVALID_ARGUMENT` |
| Missing resource | `NOT_FOUND` |
| Create of existing | `ALREADY_EXISTS` |
| No/invalid credentials | `UNAUTHENTICATED` |
| Authenticated but not allowed | `PERMISSION_DENIED` |
| Precondition/state wrong (e.g. non-empty dir) | `FAILED_PRECONDITION` |
| Concurrency conflict, retry at higher level | `ABORTED` |
| Quota/rate limit | `RESOURCE_EXHAUSTED` |
| Transient, safe to retry | `UNAVAILABLE` |
| Bug / invariant broken | `INTERNAL` |
| Not implemented | `UNIMPLEMENTED` |
Never return `UNKNOWN` deliberately; it's what the library uses for unmapped errors.
Don't leak internal error strings (stack traces, SQL) in messages.

## Rich error details (AIP-193)
Attach `google.rpc.Status` details: `ErrorInfo` (machine-readable reason, domain and metadata;
AIP-193 requires it in every error response), `BadRequest` (field violations),
`LocalizedMessage` (localized text). Each detail type appears at most once.
```go
st, _ := status.New(codes.InvalidArgument, "invalid invoice").WithDetails(&errdetails.BadRequest{
    FieldViolations: []*errdetails.BadRequest_FieldViolation{{Field: "amount", Description: "must be > 0"}},
})
return nil, st.Err()
```

## Retries
Configure via service config (`retryPolicy`: maxAttempts, backoff, `retryableStatusCodes:
["UNAVAILABLE"]`). `UNAVAILABLE` is the usual retryable code, but retrying non-idempotent
operations is not always safe; never retry `INVALID_ARGUMENT` etc. Use retry throttling to avoid storms.

## Verify
- [ ] Every client call site sets a deadline (lint or interceptor that logs calls without one).
- [ ] Error-path tests assert the status code and details, not just "err != nil".

## Checked
2026-11-01. Confirmed against the gRPC deadlines and status-codes guides (no default deadline, propagation as elapsed-adjusted timeout, code meanings), AIP-193 (ErrorInfo required, BadRequest, LocalizedMessage, one of each detail) and the gRPC retry guide (retryableStatusCodes). Removed: grpc-timeout header name, p99.9 advice, RetryInfo and QuotaFailure, retry advice for DEADLINE_EXCEEDED.
Method: documentation only; no commands were run.
