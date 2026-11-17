---
id: computing-software.software-engineering.csharp-dotnet.aspnet-core-middleware-pipeline-ordering
name: aspnet-core-middleware-pipeline-ordering
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, aspnet-core, middleware-pipeline, aspnet-middleware, exception-handling, routing]
level: practitioner
status: docs-checked
description: "Order ASP.NET Core middleware correctly: the canonical pipeline, why UseRouting/UseAuthentication/UseAuthorization/UseCors order matters, and writing custom middleware."
sources:
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/write
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/error-handling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASP.NET Core middleware pipeline ordering

**Goal:** every request passes through middleware in an order where errors are caught, security runs before endpoints, and nothing is silently skipped.

## 1. The canonical order
```csharp
var app = builder.Build();

app.UseExceptionHandler();             // first: catches exceptions from everything after it (needs AddProblemDetails)
if (!app.Environment.IsDevelopment()) app.UseHsts();
app.UseHttpsRedirection();
app.UseStaticFiles();                  // short-circuits for files
app.UseRouting();                      // selects the endpoint (implicit in minimal hosting if omitted)
app.UseCors();                         // after routing, before auth, so endpoint CORS metadata applies
app.UseRateLimiter();
app.UseAuthentication();               // establishes HttpContext.User
app.UseAuthorization();                // evaluates endpoint policies; needs routing info
app.MapControllers();
app.MapHealthChecks("/healthz");
app.Run();
```
Middleware runs in registration order on the way in and reverse order on the way out.

## 2. Ordering bugs and their symptoms
| Rule from the docs | Why |
|---|---|
| `UseCors`, `UseAuthentication`, `UseAuthorization` must appear in that order | CORS headers and the user identity must be set before authorization runs |
| `UseCors` before `UseResponseCaching` | CORS headers on every response, including cached ones |
| `UseRateLimiter` after `UseRouting` when endpoint-specific limits (`[EnableRateLimiting]`) are used | it needs the endpoint; global-only limiters may run before routing |
| `UseRequestLocalization` before middleware that reads the culture (for example `UseStaticFiles`) | culture is set first |
| Exception handler first | it only catches exceptions from middleware registered after it |
| Custom middleware that depends on the user goes after `UseAuthentication` | `HttpContext.User` is populated by authentication |

## 3. Writing middleware
Inline:
```csharp
app.Use(async (ctx, next) =>
{
    ctx.Response.Headers["X-Request-Id"] = ctx.TraceIdentifier;
    await next(ctx);
});
```
Class-based (convention):
```csharp
public sealed class TimingMiddleware(RequestDelegate next, ILogger<TimingMiddleware> log)
{
    public async Task InvokeAsync(HttpContext ctx)
    {
        var sw = Stopwatch.StartNew();
        try { await next(ctx); }
        finally { log.LogInformation("{Path} {Status} {Ms}ms", ctx.Request.Path, ctx.Response.StatusCode, sw.ElapsedMilliseconds); }
    }
}
app.UseMiddleware<TimingMiddleware>();
```
Convention middleware is constructed once at app startup, not per request: inject scoped services (DbContext) as `InvokeAsync` parameters, not constructor parameters. Or implement `IMiddleware` (resolved per request, must be registered in DI).

## 4. Short-circuiting and branching
- Not calling `next` ends the pipeline (static files, health checks).
- `app.Map("/admin", b => ...)` branches by path; `app.UseWhen(ctx => ..., b => ...)` conditionally adds middleware and rejoins.

## Gotchas
- Changes to the response after it has started (`HttpResponse.HasStarted`) throw an exception; do not call `next` after the response is sent.
- `UseRouting` runs at the beginning of the pipeline if you do not call it; calling it explicitly controls where it sits.

## Verify
- Integration tests (WebApplicationFactory) assert the response for a preflight, an unauthenticated request and a thrown exception.

## Checked

Checked 2026-10-25 against aspnet/AspNetCore.Docs (fundamentals/middleware/index and write) on main.
Confirmed: the ordering rules in the table (CORS, authentication, authorization order; CORS before response caching; rate limiter after routing for endpoint-specific limits; localization before static files); `UseRouting` default position when omitted; `UseWhen` rejoins the pipeline; convention middleware is constructed at startup and gets scoped services through `Invoke`/`InvokeAsync` parameters; response changes after start throw.
Removed as unconfirmed: the symptom column (401/CORS/compression/forwarded-header behaviours), `.ShortCircuit()` version note, `UseOutputCache` placement.

Method: documentation only; no commands were run.
