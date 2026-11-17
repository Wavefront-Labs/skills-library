---
id: computing-software.software-engineering.csharp-dotnet.response-compression-and-forwarded-headers
name: response-compression-and-forwarded-headers
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-controllers, aspnet-hosting, response-compression, forwarded-headers, reverse-proxy, breach]
level: practitioner
status: docs-checked
description: "Configure ASP.NET Core response compression (Brotli/Gzip, BREACH risk) and ForwardedHeaders behind proxies and load balancers, including KnownProxies trust and middleware order."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/performance/response-compression", "https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/proxy-load-balancer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Response compression and forwarded headers

## Compression
```csharp
builder.Services.AddResponseCompression(options =>
{
    options.EnableForHttps = false;                 // the default; true is a security risk (CRIME and BREACH on dynamic pages)
    options.Providers.Add<BrotliCompressionProvider>();
    options.Providers.Add<GzipCompressionProvider>();
});
builder.Services.Configure<BrotliCompressionProviderOptions>(options =>
{
    options.Level = CompressionLevel.Fastest;        // alternatives: Optimal, SmallestSize, NoCompression
});
app.UseResponseCompression();
```
- Prefer server-based compression (IIS, Apache, Nginx) where available: the middleware probably cannot match the performance of those modules. Kestrel and HTTP.sys do not offer built-in compression.
- Every response should set `Content-Type`; the middleware compresses only MIME types in its list (replace or add via `ResponseCompressionOptions.MimeTypes`; wildcards such as `text/*` are not supported).
- BREACH can be mitigated in ASP.NET Core with antiforgery tokens.

## Forwarded headers
Behind a proxy, scheme, host and remote IP describe the proxy hop. The middleware restores them from `X-Forwarded-For`, `X-Forwarded-Proto` and `X-Forwarded-Host`:
```csharp
builder.Services.Configure<ForwardedHeadersOptions>(options =>
{
    options.ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto | ForwardedHeaders.XForwardedHost;
    options.KnownProxies.Add(IPAddress.Parse("10.0.0.100"));   // or add a CIDR range to KnownNetworks
});
app.UseForwardedHeaders();                                      // before other middleware
```
- Only loopback addresses are trusted by default (known proxies and known networks); add the proxy or its network, otherwise headers from other hosts are ignored.
- `ForwardLimit` defaults to 1, so only the rightmost entry in each header is processed; raise it only when several trusted proxies chain, and set it to null only when `KnownProxies` or `KnownNetworks` are configured.
- Setting the environment variable `ASPNETCORE_FORWARDEDHEADERS_ENABLED` to `true` enables the middleware with settings designed for cloud environments; it does not enable features such as restricting by `KnownProxies`.
- Accepting forwarded headers from untrusted sources allows header spoofing.

## Checked
Date: 2026-11-09. Confirmed on the two cited Learn pages (response-compression, proxy-load-balancer): `EnableForHttps` default and CRIME/BREACH warning, provider and level names, server-module preference and Kestrel limitation, MIME type rules, antiforgery mitigation, `KnownProxies`/`KnownNetworks`, loopback default, `ForwardLimit` default 1, middleware before others, and the environment variable and its caveat. Removed unconfirmed claims: `MapStaticAssets()` precompressed serving, `KnownIPNetworks` (.NET 10), Front Door/CDN advice, chunking remark, curl verification lines, specific redirect-loop and OAuth callback consequences.
Method: documentation only; no commands were run.
