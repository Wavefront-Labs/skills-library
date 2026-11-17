---
id: computing-software.software-engineering.csharp-dotnet.aspnet-core-web-apis
name: aspnet-core-web-apis
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp-dotnet, aspnet-core, dotnet, csharp, minimal-apis, controllers, dependency-injection, di-lifetimes, scoped, singleton, transient, options-pattern, ioptions, ioptionsmonitor, ef-core, entity-framework, dbcontext, async-await, cancellationtoken, health-checks, problem-details, typedresults, httpclientfactory, validateonstart]
level: practitioner
status: docs-checked
description: "Build ASP.NET Core web APIs: minimal APIs vs controllers, DI scope validation, the options pattern, EF Core pitfalls, async best practice and health checks."
sources:
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/options
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/error-handling
  - https://learn.microsoft.com/en-us/aspnet/core/performance/performance-best-practices
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel/options
  - https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/
  - https://learn.microsoft.com/en-us/ef/core/querying/single-split-queries
  - https://learn.microsoft.com/en-us/ef/core/performance/advanced-performance-topics
  - https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/applying
  - https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory
  - https://raw.githubusercontent.com/dotnet/AspNetCore.Docs/main/aspnetcore/host-and-deploy/health-checks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASP.NET Core web APIs: lifetimes, typed config, efficient data access

**Goal:** an ASP.NET Core API that resolves services with the right lifetimes, fails fast on bad config, queries the database efficiently, and reports health honestly.

## 1. Minimal APIs or controllers
- **Minimal APIs**: organise with `MapGroup` and extension methods; return `TypedResults` (Microsoft states it is preferred over `Results`):
```csharp
var orders = app.MapGroup("/orders").RequireAuthorization();
app.MapGet("/hello", () => TypedResults.Ok(new Message() { Text = "Hello World!" }));
```
- **Controllers**: still fine for large existing codebases. Don't mix styles within one feature.
- Validation: the minimal-API page documents `builder.Services.AddValidation()`; check which framework version your target supports.
- Errors: `builder.Services.AddProblemDetails()` followed by `app.UseExceptionHandler()` enables problem-details responses; never leak exception messages.

## 2. DI scope validation
- `ValidateScopes` and `ValidateOnBuild` are enabled by default in the Development environment and disabled elsewhere. With `ValidateOnBuild` a bad service configuration fails at app startup, not when the service is first requested. Turn both on in tests.
- A background work item needs its own scope: inject `IServiceScopeFactory` (a singleton) and create a scope per unit of work.
- Use `IHttpClientFactory`: creating more handlers than necessary can cause socket exhaustion, and handlers that keep connections open indefinitely can miss DNS changes.

## 3. Options pattern
```csharp
builder.Services.AddOptions<PaymentsOptions>()
    .BindConfiguration("Payments")
    .ValidateDataAnnotations()
    .ValidateOnStart();          // validate when the app starts
```
`IOptionsSnapshot<T>` is scoped and a snapshot taken when it is constructed, for transient and scoped dependencies. `IOptionsMonitor<T>` is a singleton that returns current values, which is especially useful in singleton dependencies. Keep secrets out of `appsettings.json`; supply them from a secure configuration source.

## 4. EF Core pitfalls
- `DbContext` is not thread-safe: don't share a context between threads, and await every async call before reusing it.
- N+1 and cartesian explosion: use explicit `Include` or projection, and `AsSplitQuery()` for multiple collection includes (see the single and split queries page).
- For deployment, Microsoft recommends a migration bundle for automation or a SQL script when review is needed, and advises considering carefully before applying migrations programmatically in production; don't make every replica migrate at startup.
- `AddDbContextPool` replaces `AddDbContext` to pool context instances; its `poolSize` parameter caps the pool.

## 5. Async
- Don't block with `Task.Wait` or `Task<T>.Result`: blocking calls lead to thread-pool starvation.
- `async void` is always a bad practice in ASP.NET Core apps (Microsoft).

## 6. Health checks
```csharp
builder.Services.AddHealthChecks();
app.MapHealthChecks("/health/live", new() { Predicate = _ => false });
```
By default the middleware runs all registered checks; the `Predicate` option on `HealthCheckOptions` selects a subset. A basic probe reporting that the app can process requests is a liveness check; add readiness checks on dependencies by tagging them and filtering on the tag.

## Gotchas
- The default maximum request body size in Kestrel is 30,000,000 bytes (about 28.6 MB); raise it deliberately for uploads.
- An `IOptionsSnapshot` is scoped, so do not inject it into a singleton; use `IOptionsMonitor`.

## Verify
- [ ] Tests run with `ValidateOnBuild`/`ValidateScopes` on.
- [ ] Missing or invalid config fails startup via `ValidateOnStart`.
- [ ] No `.Result`/`.Wait()` in request paths.
- [ ] Liveness stays healthy with the database down while readiness does not.

## Checked
2026-11-01. Confirmed on Microsoft Learn: minimal APIs (`MapGroup`, `TypedResults` preferred, `AddValidation`,
`ValidateScopes`/`ValidateOnBuild` Development default), error handling (`AddProblemDetails`,
`UseExceptionHandler`), options (snapshot scoped, monitor singleton, `ValidateOnStart`), performance best
practices (blocking calls, `async void`, `IServiceScopeFactory`), Kestrel options (30,000,000 byte
default body limit), DbContext configuration (not thread-safe), split queries, advanced performance
(`AddDbContextPool`, `poolSize`), applying migrations (bundles), httpclient-factory (socket exhaustion, DNS), and
the health-checks source in the ASP.NET Core docs repository (the Learn page itself returned 403;
`MapHealthChecks`, `Predicate`, liveness). Removed unconfirmed claims: Native-AOT and speed claims, the .NET 10
validation date, RFC 9457 wording, the captive-dependency table, `AddDbContextCheck`, `AsNoTracking` advice, the double-underscore
environment-variable rule, the cancellation-token binding detail, `ConfigureAwait` advice and the `Database.Migrate()` race claim.
Method: documentation only; no commands were run.
