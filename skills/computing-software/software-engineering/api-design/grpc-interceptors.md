---
id: computing-software.software-engineering.api-design.grpc-interceptors
name: grpc-interceptors
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, grpc-interceptors, middleware, grpc-auth, grpc-metrics, opentelemetry]
level: practitioner
status: docs-checked
description: "Write gRPC unary and streaming interceptors for auth, logging, metrics and tracing, order them correctly, and reuse the ecosystem ones instead of hand-rolling."
sources: ["https://grpc.io/docs/guides/interceptors/", "https://github.com/grpc-ecosystem/go-grpc-middleware"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gRPC interceptors

Interceptors are gRPC middleware (also called filters): logic that is independent of any single RPC method and applies to all or most calls. They are added when building a channel or server, run for every RPC on it, and come in client and server forms with different APIs.

Good uses: metadata handling, logging, fault injection, caching, metrics, policy enforcement, server-side authentication and authorization. Client-side authentication is better done with the call credentials API (see grpc-metadata-and-call-credentials). Interceptors are per-call; they cannot manage TCP connections, ports or TLS.

## Go server example
```go
func authUnary(ctx context.Context, req any, info *grpc.UnaryServerInfo, h grpc.UnaryHandler) (any, error) {
    md, _ := metadata.FromIncomingContext(ctx)
    tok := md.Get("authorization")
    if len(tok) == 0 { return nil, status.Error(codes.Unauthenticated, "missing token") }
    claims, err := verify(tok[0]); if err != nil { return nil, status.Error(codes.Unauthenticated, "bad token") }
    return h(context.WithValue(ctx, claimsKey{}, claims), req)
}
srv := grpc.NewServer(
    grpc.StatsHandler(otelgrpc.NewServerHandler()),            // OpenTelemetry tracing and metrics
    grpc.ChainUnaryInterceptor(metricsU, loggingU, authUnary, recoveryU),
    grpc.ChainStreamInterceptor(metricsS, loggingS, authStream, recoveryS))
```
`verify`, `claimsKey` and the other interceptor names are placeholders for your own code.

## Order
Order is significant: think of interceptors as a line between the application and the network, and learn which end your implementation runs first. The go-grpc-middleware README chain runs metrics, then logging, then auth (skipping the health check), then recovery. It says to make the recovery interceptor the last one so a panic does not skip other interceptors, and that interceptors injecting context fields must be chained before the logging adapter.

## Use, don't write
go-grpc-middleware v2 (module path ends in `v2`) offers auth, logging, ratelimit, retry, timeout, validator, protovalidate, recovery and `selector` (apply an interceptor only to chosen methods or services). Prometheus metrics live in its separate `providers/prometheus` module (replacing the deprecated go-grpc-prometheus). For OpenTelemetry use `otelgrpc`. grpc-go also has native retries.

## Gotchas
- Use `selector` (or the method name `/pkg.Service/Method`) to exempt unauthenticated methods such as health checks.
- Do not log full request messages (PII, size); log method, code, duration, peer.

## Checked
2026-11-08. Confirmed against the grpc.io Interceptors guide (use cases, per-call scope, ordering, client-auth note) and the go-grpc-middleware README (interceptor list, v2 path, chain order, recovery guidance, deprecated go-grpc-prometheus, otelgrpc). Removed: the claimed outermost recovery order, the Java/Python/.NET/Node interceptor API lines, and the OpenTelemetry Go page (not read).
Method: documentation only; no commands were run.
