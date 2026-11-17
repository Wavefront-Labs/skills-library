---
id: computing-software.software-engineering.go.grpc-interceptors-and-deadlines
name: grpc-interceptors-and-deadlines
category: computing-software
field: software-engineering
product: go
tags: [go, go-grpc-rpc, go-grpc-interceptors, grpc, interceptors, deadlines]
level: practitioner
status: docs-checked
description: "Add unary and stream interceptors to Go gRPC servers and clients for logging, auth, recovery and deadline propagation."
sources:
  - https://pkg.go.dev/google.golang.org/grpc#UnaryServerInterceptor
  - https://grpc.io/docs/guides/deadlines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# gRPC interceptors and deadlines

**Goal:** cross-cutting concerns in one place, and every call bounded by a deadline.

```go
func logging(log *slog.Logger) grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req any, info *grpc.UnaryServerInfo, h grpc.UnaryHandler) (any, error) {
        start := time.Now()
        resp, err := h(ctx, req)
        log.InfoContext(ctx, "rpc", "method", info.FullMethod,
            "code", status.Code(err).String(), "dur", time.Since(start))
        return resp, err
    }
}

srv := grpc.NewServer(grpc.ChainUnaryInterceptor(recovery(), logging(log), auth()))

// client: a per-call deadline, and a default for all calls
ctx, cancel := context.WithTimeout(ctx, 2*time.Second)
defer cancel()
resp, err := client.GetOrder(ctx, req)
conn, _ := grpc.NewClient(target, grpc.WithTransportCredentials(creds),
    grpc.WithChainUnaryInterceptor(timeoutDefault(3*time.Second)))
```

`timeoutDefault` is your own client interceptor that applies a default `context.WithTimeout` when the caller set none. gRPC converts the deadline to a timeout with elapsed time deducted, so clock skew between hosts does not matter; the server cancels the call (`CANCELLED`) once the client's deadline passes, but your handler must stop its own work, so pass `ctx` into downstream calls and check it in long loops. `grpc.NewClient` (added in v1.63) is the constructor on the package page; it does not connect until first use.

## Gotchas
- Interceptor order matters: `ChainUnaryInterceptor` runs them in the order given, so put recovery first (outermost) and auth before business logging.
- Without a deadline a hung upstream holds a goroutine and connection forever.

## Verify
Call with a 10 ms deadline against a handler that sleeps 1 s and expect `DEADLINE_EXCEEDED` (`codes.DeadlineExceeded`) on the client and a cancelled `ctx` on the server.

## Checked
2026-11-03. Confirmed on pkg.go.dev/google.golang.org/grpc: `UnaryServerInterceptor`, `UnaryServerInfo.FullMethod`, `UnaryHandler`, `ChainUnaryInterceptor`, `WithChainUnaryInterceptor`, `WithTransportCredentials`, `NewClient` (v1.63). Confirmed on grpc.io deadlines guide: deadline-to-timeout conversion, CANCELLED, DEADLINE_EXCEEDED. Removed: the `grpc-timeout` header name, go-grpc-middleware list, stream-wrapping claim, replaced Dial note (all unconfirmed).
Method: documentation only; no commands were run.
