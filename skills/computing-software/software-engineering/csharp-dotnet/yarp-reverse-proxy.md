---
id: computing-software.software-engineering.csharp-dotnet.yarp-reverse-proxy
name: yarp-reverse-proxy
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-realtime-rpc, yarp-reverse-proxy, yarp, api-gateway, load-balancing, health-checks]
level: practitioner
status: draft
description: "Build an API gateway or reverse proxy with YARP: routes and clusters in config, transforms, load balancing, active health checks, auth at the edge and rate limiting."
sources: ["https://microsoft.github.io/reverse-proxy/", "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/yarp/yarp-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# YARP reverse proxy

```csharp
builder.Services.AddReverseProxy().LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));
builder.Services.AddRateLimiter(o => o.AddFixedWindowLimiter("api", w => { w.PermitLimit = 100; w.Window = TimeSpan.FromMinutes(1); }));
app.UseRateLimiter(); app.UseAuthentication(); app.UseAuthorization();
app.MapReverseProxy();
```
```json
"ReverseProxy": {
  "Routes": {
    "orders": { "ClusterId": "orders", "AuthorizationPolicy": "default", "RateLimiterPolicy": "api",
      "Match": { "Path": "/api/orders/{**rest}" },
      "Transforms": [ { "PathRemovePrefix": "/api" }, { "RequestHeader": "X-Forwarded-Prefix", "Set": "/api" } ] } },
  "Clusters": {
    "orders": { "LoadBalancingPolicy": "PowerOfTwoChoices",
      "HealthCheck": { "Active": { "Enabled": true, "Interval": "00:00:10", "Timeout": "00:00:03", "Path": "/healthz" },
                       "Passive": { "Enabled": true } },
      "Destinations": { "d1": { "Address": "https://orders-1:8443" }, "d2": { "Address": "https://orders-2:8443" } } } } }
```
## Notes
- Package `Yarp.ReverseProxy`. Routes match host/path/headers/methods; clusters hold destinations. Config reload is live; dynamic sources via `IProxyConfigProvider` (Kubernetes ingress controller exists).
- Policies: `RoundRobin`, `LeastRequests`, `Random`, `PowerOfTwoChoices`, `FirstAlphabetical`; session affinity via cookie or header.
- It is built on ASP.NET middleware, so auth, CORS, rate limiting, output caching and custom middleware via `MapReverseProxy(p => p.Use(...))` all apply at the edge; validate JWT at the gateway and forward identity headers only from the gateway.
- Streaming and WebSockets/gRPC pass through; HTTP/2 to backends needs `HttpClient.Version` config.
- Transforms: path, query, headers, forwarded headers (`X-Forwarded` defaults on), response transforms.
- Timeouts: `ActivityTimeout`, per-route `Timeout`; request body limits still apply (Kestrel `MaxRequestBodySize`).

## Gotchas
- Do not pass the original `Host` header unless backends expect it (`RequestHeaderOriginalHost`).
- Trust: strip inbound identity headers (`X-User-Id`) so clients cannot spoof them.
- Retry non-idempotent requests carelessly and you duplicate writes.
- Health checks must hit a cheap endpoint.

## Verify
Stop one destination: traffic continues via the other after the active check fails it; unauthenticated call to a protected route returns 401 at the gateway without reaching the backend.
