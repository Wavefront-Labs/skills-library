---
id: computing-software.software-engineering.csharp-dotnet.kestrel-configuration-and-limits
name: kestrel-configuration-and-limits
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-hosting, kestrel-configuration, kestrel, request-limits, http2, http3, endpoints]
level: practitioner
status: docs-checked
description: "Configure Kestrel endpoints, protocols (HTTP/1-3), TLS, request size, header, timeout and connection limits, and understand the Kestrel versus reverse proxy split."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel", "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel/options", "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel/http3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kestrel configuration

```csharp
builder.WebHost.ConfigureKestrel(serverOptions =>
{
    serverOptions.Limits.MaxConcurrentConnections = 10_000;
    serverOptions.Limits.MaxRequestBodySize = 10 * 1024 * 1024;   // default 30,000,000 bytes (about 28.6 MB)
    serverOptions.Limits.KeepAliveTimeout = TimeSpan.FromMinutes(2);
    serverOptions.Limits.RequestHeadersTimeout = TimeSpan.FromSeconds(30);
    serverOptions.Limits.MinRequestBodyDataRate = new MinDataRate(bytesPerSecond: 240, gracePeriod: TimeSpan.FromSeconds(5));
    serverOptions.ListenAnyIP(8080);
    serverOptions.ListenAnyIP(8443, listenOptions =>
    {
        listenOptions.Protocols = HttpProtocols.Http1AndHttp2AndHttp3;
    });
});
```
`ConfigureEndpointDefaults` applies settings to every endpoint. `Limits` can also come from configuration (`Kestrel:Limits` section).

## Protocols
- HTTP/2 over TLS is negotiated with ALPN (application-layer protocol negotiation).
- HTTP/3 needs `HttpProtocols.Http1AndHttp2AndHttp3` on an endpoint and, on Linux, the `libmsquic` package installed from Microsoft's package repository.

## Rules
- Request body limits protect memory: change the limit per request through `IHttpMaxRequestBodySizeFeature` only where needed (it has an `IsReadOnly` property: the limit cannot be changed after the app has started reading the request body).
- `MinRequestBodyDataRate` per request is generally not supported for HTTP/2; the feature can only be disabled there by setting `MinDataRate` to null.
- `MaxConcurrentConnections` does not count connections upgraded to another protocol such as WebSockets.
- `AllowSynchronousIO` defaults to false; enable it only for libraries that cannot do asynchronous I/O, since blocking calls can starve the thread pool.
- `Http2.MaxStreamsPerConnection` limits concurrent request streams per HTTP/2 connection; excess streams are refused.
- For other sizes and defaults, read the Kestrel options page rather than trusting remembered numbers.

## Checked
Date: 2026-11-09. Confirmed on the three cited Learn pages (kestrel, kestrel/options, kestrel/http3): `Limits` property names, 30,000,000-byte default body size, `MinDataRate` HTTP/2 caveat, read-only body-limit property, upgraded-connection exclusion, `AllowSynchronousIO` default and risk, `MaxStreamsPerConnection`, `ConfigureEndpointDefaults`, `ListenAnyIP`, `Http1AndHttp2AndHttp3`, ALPN, `libmsquic`. Removed unconfirmed claims: `AddServerHeader`, `MaxRequestHeadersTotalSize` value, container port 8080 and `ASPNETCORE_HTTP_PORTS`, named-pipe API version, h2c wording, `Alt-Svc`, certificate hot reload, the 100-stream default, 413 behaviour, proxy advice and the curl/dotnet-counters verification lines.
Method: documentation only; no commands were run.
