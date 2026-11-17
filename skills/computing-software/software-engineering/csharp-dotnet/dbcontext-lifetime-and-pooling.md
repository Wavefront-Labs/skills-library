---
id: computing-software.software-engineering.csharp-dotnet.dbcontext-lifetime-and-pooling
name: dbcontext-lifetime-and-pooling
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dbcontext-lifetime, dbcontext-pooling, idbcontextfactory, ef-core, background-services, thread-safety]
level: practitioner
status: docs-checked
description: "Manage EF Core DbContext lifetime: scoped per request, AddDbContextPool, IDbContextFactory for background services and Blazor, never sharing a context across threads."
sources: ["https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/", "https://learn.microsoft.com/en-us/ef/core/performance/advanced-performance-topics#dbcontext-pooling", "https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/#using-a-dbcontext-factory-eg-for-blazor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DbContext lifetime and pooling

**Goal:** one short-lived unit of work per operation, no cross-thread sharing, and
cheap context creation under load.

## Rules
- A `DbContext` is a unit of work: change tracker + connection usage. Short-lived.
- **Not thread-safe**: concurrent operations on one instance throw "A second operation was
  started on this context instance before a previous operation completed".
- Long-lived contexts accumulate tracked entities (memory, slow `SaveChanges`, stale data).

## Web apps: scoped
```csharp
builder.Services.AddDbContext<AppDbContext>(o => o.UseNpgsql(cs));   // scoped = one per HTTP request
```
Don't inject a scoped DbContext into a singleton (captive dependency; dependency injection scope validation reports it).

## Pooling
```csharp
builder.Services.AddDbContextPool<AppDbContext>(o => o.UseNpgsql(cs), poolSize: 1024);
```
Reuses context instances (state reset between uses) - saves allocation/setup on high-throughput
services. Constraints: the context must not hold per-request state in fields set via
constructor injection; use `OnConfiguring` carefully. For per-tenant state with pooling, use
`PooledDbContextFactory` plus setting a property after rent, or a scoped wrapper.

## Background work and other lifetimes: factory
```csharp
builder.Services.AddDbContextFactory<AppDbContext>(o => o.UseNpgsql(cs));   // also pooled: AddPooledDbContextFactory

public sealed class Reconciler(IDbContextFactory<AppDbContext> factory) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            await using var db = await factory.CreateDbContextAsync(ct);   // fresh per iteration
            await ReconcileBatchAsync(db, ct);
            await Task.Delay(TimeSpan.FromMinutes(1), ct);
        }
    }
}
```
Alternatively create a scope: `using var scope = scopeFactory.CreateScope();`. Blazor Server
circuits are long-lived - always use the factory there.

## Parallel work
Need concurrency? One context per task:
```csharp
await Parallel.ForEachAsync(batches, ct, async (b, t) =>
{
    await using var db = await factory.CreateDbContextAsync(t);
    ...
});
```

## Connection pooling is separate
ADO.NET providers pool connections independently of DbContext pooling; size via the
connection string (`Maximum Pool Size`). Context pooling does not reduce DB connections.

## Checked
2026-10-28: Confirmed in the EF Core DbContext configuration and advanced performance pages: DbContext is not thread-safe, AddDbContextPool poolSize default 1024, AddDbContextFactory for non-scoped units of work. Removed the quoted DI exception text (ASP.NET DI page not fetched).
Method: documentation only; no commands were run.

## Verify
- [ ] No DbContext captured by singletons or static fields; DI scope validation on in tests.
- [ ] Background services create a context per unit of work.
