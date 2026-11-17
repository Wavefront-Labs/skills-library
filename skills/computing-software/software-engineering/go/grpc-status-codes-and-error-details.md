---
id: computing-software.software-engineering.go.grpc-status-codes-and-error-details
name: grpc-status-codes-and-error-details
category: computing-software
field: software-engineering
product: go
tags: [go, go-grpc-rpc, go-grpc-status, grpc, status-codes, error-details, errdetails]
level: practitioner
status: docs-checked
description: "Return correct gRPC status codes from Go services, attach structured error details, and map them to and from domain errors."
sources:
  - https://pkg.go.dev/google.golang.org/grpc/status
  - https://grpc.github.io/grpc/core/md_doc_statuscodes.html
  - https://google.aip.dev/193
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# gRPC status codes and error details

**Goal:** clients can act on errors programmatically.

```go
import ("google.golang.org/grpc/codes"; "google.golang.org/grpc/status")

func (s *Server) GetOrder(ctx context.Context, r *pb.GetOrderRequest) (*pb.Order, error) {
    o, err := s.store.Get(ctx, r.Id)
    switch {
    case errors.Is(err, store.ErrNotFound):
        return nil, status.Errorf(codes.NotFound, "order %q not found", r.Id)
    case errors.Is(err, context.DeadlineExceeded):
        return nil, status.FromContextError(err).Err()
    case err != nil:
        return nil, status.Error(codes.Internal, "internal error") // do not leak details
    }
    return o, nil
}
```

The `status` package says service handlers should return an error created by that package (`status.New`, `Newf`, `Error`, `Errorf`, `FromProto`),
and a `Status` carries a code, a message and details; it is immutable. Details travel in the Details field of the status proto.
Client side: `status.FromError(err)` returns `(s, ok)`; `status.Code(err)` returns the code if the error is, or wraps, a status error, otherwise `OK` for nil and `Unknown`.

## Choosing codes (gRPC status code table)
- `InvalidArgument`: arguments problematic regardless of system state. `FailedPrecondition`: system not in the required state; do not retry until the state is fixed. `OutOfRange`: past a valid range that may change with state.
- `NotFound`; `AlreadyExists`; `PermissionDenied` (caller identified but not allowed; not for resource exhaustion) versus `Unauthenticated` (no valid credentials).
- `ResourceExhausted`: quota or space; `Unavailable`: transient, retry with backoff (not always safe for non-idempotent calls); `Aborted`: retry at a higher level, for example a failed test-and-set; `DeadlineExceeded`; `Internal`: broken invariants, reserved for serious errors.
- gRPC publishes no fixed retry list: each application decides which codes to retry.

## Error details (AIP-193)
- The message is a developer-facing, human-readable English debug message; localised text goes in a `LocalizedMessage` detail.
- AIP-193 says every error response must include an `ErrorInfo` in details (reason plus metadata), and each detail type may appear at most once (one `BadRequest`, but a `BadRequest` and a `PreconditionFailure` may both appear).

## Gotchas
- A server-side error that is not a status error maps to `Unknown`; `FromError` on an incompatible error returns `Unknown` with `ok` false.
- `FromError` also finds a status wrapped in other errors; for wrapped errors the message contains the entire `err.Error()` text, so map domain errors explicitly to keep client messages clean.
- Do not put stack traces or SQL text in messages seen by clients.

## Checked
2026-11-09. Confirmed on pkg.go.dev/google.golang.org/grpc/status (function list, `Code`, `FromContextError`, `FromError` wrapping and Unknown behaviour, `Status` is immutable),
the gRPC status code table (code meanings, retry guidance) and AIP-193 (message, `ErrorInfo` requirement, one of each detail type). Removed: the `WithDetails`/`errdetails.BadRequest` snippet and the
`bufconn` test advice (methods and package not covered by the cited pages), the "never retry InvalidArgument" absolute, and the claim that unwrapping needs newer grpc-go releases.
Method: documentation only; no commands were run.

## Verify
Table-test the error mapper with each domain error and assert `status.Code(err)` for each.
