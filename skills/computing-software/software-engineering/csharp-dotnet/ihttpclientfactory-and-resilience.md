---
id: computing-software.software-engineering.csharp-dotnet.ihttpclientfactory-and-resilience
name: ihttpclientfactory-and-resilience
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, ihttpclientfactory, http-resilience, typed-clients, polly, socket-exhaustion, aspnet-core, resilience-pipelines, dotnet-resilience]
level: practitioner
status: docs-checked
description: "Use HttpClient correctly in .NET: IHttpClientFactory typed clients, socket exhaustion and DNS staleness, the standard resilience handler and delegating handlers."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory", "https://learn.microsoft.com/en-us/dotnet/core/resilience/http-resilience", "https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/http/httpclient-guidelines"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IHttpClientFactory and resilience

**Goal:** outbound HTTP that reuses connections, follows DNS changes, and handles
transient failures without hand-written retry loops.

## The two classic bugs
- Creating and disposing `HttpClient` per request wastes connections; the factory manages the caching and lifetime of the underlying handlers.
- One static `HttpClient` forever: `HttpClient` only resolves DNS when a connection is created and ignores DNS TTLs, so traffic can keep going to old IPs after a failover. Fix for long-lived clients: `new SocketsHttpHandler { PooledConnectionLifetime = TimeSpan.FromMinutes(15) }`.
IHttpClientFactory addresses both. Avoid it if your app needs cookies, because pooled handlers share `CookieContainer` objects.

## Typed client
```csharp
builder.Services.AddHttpClient<BillingClient>(c =>
{
    c.BaseAddress = new Uri(builder.Configuration["Billing:BaseUrl"]!);
    c.DefaultRequestHeaders.UserAgent.ParseAdd("orders-service/1.0");
})
.AddStandardResilienceHandler();          // Microsoft.Extensions.Http.Resilience

public sealed class BillingClient(HttpClient http)
{
    public async Task<Invoice?> GetAsync(string id, CancellationToken ct) =>
        await http.GetFromJsonAsync<Invoice>($"invoices/{id}", ct);
}
```
Typed clients are registered as transient; don't capture them in singletons (inject `IHttpClientFactory` there instead).

## Standard resilience pipeline
`AddStandardResilienceHandler` (package `Microsoft.Extensions.Http.Resilience`) stacks, in order: rate limiter (1,000 permits, no queue) -> total request timeout (30 s) -> retry (max 3, exponential backoff with jitter, 2 s delay; handles HTTP 500 and above, 408, 429 and HTTP exceptions) -> circuit breaker (10% failure ratio, minimum throughput 100, 30 s sampling, 5 s break) -> per-attempt timeout (10 s). Tune:
```csharp
.AddStandardResilienceHandler(o =>
{
    o.Retry.MaxRetryAttempts = 2;
    o.AttemptTimeout.Timeout = TimeSpan.FromSeconds(3);
    o.TotalRequestTimeout.Timeout = TimeSpan.FromSeconds(10);
    o.Retry.DisableForUnsafeHttpMethods();       // retries are on for all HTTP methods by default
});
```
`AddStandardHedgingHandler` is the alternative for hedging requests.

## Delegating handlers (cross-cutting)
```csharp
public sealed class ApiKeyHandler(IOptions<BillingOptions> o) : DelegatingHandler
{
    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage r, CancellationToken ct)
    { r.Headers.Add("X-Api-Key", o.Value.ApiKey); return base.SendAsync(r, ct); }
}
builder.Services.AddTransient<ApiKeyHandler>();
builder.Services.AddHttpClient<BillingClient>().AddHttpMessageHandler<ApiKeyHandler>();
```

## Gotchas
- `HttpClient.Timeout` (100 s default) also applies on top of resilience timeouts; keep it consistent with the pipeline's total timeout.
- The factory adds logging via `ILogger` for all requests sent through its clients; check your log levels in production.

## Verify
- [ ] No `new HttpClient()` in request paths (grep).
- [ ] Integration test with a fault-injecting stub shows retries and the circuit opening.

## Checked

Checked 2026-10-25 against dotnet/docs (core/extensions/httpclient-factory, core/resilience/http-resilience, fundamentals/networking/http/httpclient-guidelines) and dotnet/dotnet-api-docs (HttpClient.Timeout) on main.
Confirmed: the standard resilience pipeline order and defaults (rate limiter 1,000 permits, total timeout 30 s, retry 3 with exponential backoff, jitter and 2 s delay, circuit breaker 10%/100/30 s/5 s, attempt timeout 10 s); retried statuses 500 and above, 408, 429; `DisableForUnsafeHttpMethods`; retries apply to all methods by default; `AddStandardHedgingHandler`; typed clients are transient; DNS only resolved on connection creation and `PooledConnectionLifetime` fix; cookie caveat; `HttpClient.Timeout` default 100 s.
Removed as unconfirmed: TIME_WAIT/socket exhaustion explanation, the 2-minute handler lifetime default, the `HttpRequestException` list item beyond "HTTP exceptions", the logging category name, the WireMock.Net reference.

Method: documentation only; no commands were run.
