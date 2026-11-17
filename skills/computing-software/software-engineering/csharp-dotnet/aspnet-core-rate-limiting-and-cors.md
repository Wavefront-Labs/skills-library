---
id: computing-software.software-engineering.csharp-dotnet.aspnet-core-rate-limiting-and-cors
name: aspnet-core-rate-limiting-and-cors
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-rate-limiting, cors, rate-limiter-middleware, partitioned-rate-limit, preflight, aspnet-core]
level: practitioner
status: docs-checked
description: "Configure ASP.NET Core rate limiting (fixed/sliding window, token bucket, concurrency, per-user partitions, 429 responses) and CORS policies with correct middleware order."
sources:
  - https://learn.microsoft.com/en-us/aspnet/core/performance/rate-limit
  - https://learn.microsoft.com/en-us/aspnet/core/security/cors
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/#middleware-order
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASP.NET Core rate limiting and CORS

**Goal:** protect endpoints from abuse with per-client limits, and let exactly the
intended browser origins call the API.

## Rate limiting
```csharp
builder.Services.AddRateLimiter(o =>
{
    o.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
    o.OnRejected = (ctx, _) =>
    {
        if (ctx.Lease.TryGetMetadata(MetadataName.RetryAfter, out var retry))
            ctx.HttpContext.Response.Headers.RetryAfter = ((int)retry.TotalSeconds).ToString();
        return ValueTask.CompletedTask;
    };
    o.AddPolicy("per-user", http => RateLimitPartition.GetTokenBucketLimiter(
        partitionKey: http.User.Identity?.Name ?? http.Connection.RemoteIpAddress?.ToString() ?? "anon",
        factory: _ => new TokenBucketRateLimiterOptions
        {
            TokenLimit = 100, TokensPerPeriod = 50, ReplenishmentPeriod = TimeSpan.FromSeconds(10),
            QueueLimit = 0,
        }));
    o.AddConcurrencyLimiter("reports", c => { c.PermitLimit = 4; c.QueueLimit = 10; });
});
app.UseRateLimiter();
app.MapGet("/api/search", Search).RequireRateLimiting("per-user");
app.MapPost("/api/reports", Build).RequireRateLimiting("reports");
```
Algorithms: fixed window, sliding window, token bucket (bursts with steady refill) and concurrency (limits in-flight work). Set `RejectionStatusCode` to 429 explicitly.

The built-in limiters are in-memory per process, so check how the effective limit scales with replicas. Behind proxies, confirm which client address your partition key sees.

## CORS
```csharp
builder.Services.AddCors(o => o.AddPolicy("spa", p => p
    .WithOrigins("https://app.acme.dev", "https://staging.acme.dev")
    .WithMethods("GET", "POST", "PUT", "DELETE")
    .WithHeaders("Content-Type", "Authorization")
    .AllowCredentials()
    .SetPreflightMaxAge(TimeSpan.FromHours(1))));
app.UseCors("spa");
```
- `AllowAnyOrigin()` with `AllowCredentials()` is an insecure configuration; the CORS service returns an invalid CORS response for it.
- The origin URL must not have a trailing slash, or the comparison fails and no header is returned.
- CORS is not a security feature; it relaxes the same-origin policy.
- A denied preflight returns 204 without CORS headers, so the browser does not send the request.

## Middleware order
`UseRouting` -> `UseCors` -> `UseAuthentication` -> `UseAuthorization` -> endpoints. `UseCors` goes after `UseRouting` and before `UseAuthorization`. `UseRateLimiter` must come after `UseRouting` when endpoint-specific limits are used; global-only limiters may run before routing.

## Verify
- [ ] Load test returns 429 once limits are exceeded, per partition and not globally.
- [ ] Browser from a non-listed origin is blocked; listed origin with credentials works.

## Checked

Checked 2026-10-25 against aspnet/AspNetCore.Docs (performance/rate-limit, security/cors, fundamentals/middleware) on main.
Confirmed: `RejectionStatusCode` set to 429 and an `OnRejected` callback reading `MetadataName.RetryAfter`; `TokenLimit`, `TokensPerPeriod`, `ReplenishmentPeriod`; `RequireRateLimiting`; `SetPreflightMaxAge`; no trailing slash in origins; `AllowAnyOrigin` with `AllowCredentials` is insecure and invalid; denied preflight returns 204; `UseCors` placement; `UseRateLimiter` after `UseRouting` for endpoint limits.
Removed as unconfirmed: the default 503 rejection code, the .NET 7 version label, the N-replicas multiplier, Redis-backed limiter advice, the preflight-401 explanation.

Method: documentation only; no commands were run.
