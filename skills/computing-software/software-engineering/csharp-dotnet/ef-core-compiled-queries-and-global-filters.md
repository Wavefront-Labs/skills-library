---
id: computing-software.software-engineering.csharp-dotnet.ef-core-compiled-queries-and-global-filters
name: ef-core-compiled-queries-and-global-filters
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, ef-core-querying, ef-compiled-queries, ef-global-query-filters, soft-delete, multi-tenancy, ignorequeryfilters, asnotracking]
level: advanced
status: draft
description: "Speed hot EF Core queries with EF.CompileAsyncQuery, and apply global query filters for soft delete and tenants, including named filters (EF Core 10), IgnoreQueryFilters and pitfalls."
sources: ["https://learn.microsoft.com/en-us/ef/core/performance/advanced-performance-topics#compiled-queries", "https://learn.microsoft.com/en-us/ef/core/querying/filters", "https://learn.microsoft.com/en-us/ef/core/performance/efficient-querying"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EF Core compiled queries and global query filters

## Compiled queries
EF caches query translation automatically for most LINQ shapes (parameterised); `EF.CompileAsyncQuery` skips even the expression-tree processing, helpful in very hot paths (measure first).
```csharp
static readonly Func<AppDb, int, CancellationToken, Task<Order?>> _byId =
    EF.CompileAsyncQuery((AppDb db, int id, CancellationToken ct) =>
        db.Orders.AsNoTracking().FirstOrDefault(o => o.Id == id));
var order = await _byId(db, 42, ct);
// collections: EF.CompileAsyncQuery returning IAsyncEnumerable<T>
```
Rules: static field, take the context as first parameter, only supports certain operators (no `Include` of different shapes mid-flight - include is fine inside). Capturing variables bakes them as constants; pass them as parameters instead. Gains are modest (microseconds); the real wins are query shape, `AsNoTracking`, projection and indexes.

## Global query filters
```csharp
modelBuilder.Entity<Post>().HasQueryFilter(p => !p.IsDeleted);
modelBuilder.Entity<Invoice>().HasQueryFilter(i => i.TenantId == _tenant.Id);   // _tenant is a property on the DbContext, evaluated per context instance
```
Applied to every query on the entity and to `Include`d navigations; bypass with `.IgnoreQueryFilters()` (admin/reporting). **EF Core 10** adds named query filters (`HasQueryFilter("SoftDelete", ...)`, `IgnoreQueryFilters(["SoftDelete"])`) so multiple filters can be toggled independently; earlier versions allow one filter per entity.

## Gotchas
- Required navigation to a filtered entity: an Order whose required Customer is soft-deleted returns no orders (inner join). Make the relationship optional or add the same filter on the dependent.
- Filters don't apply to `ExecuteDelete/ExecuteUpdate` the way you expect; verify with SQL logging. Raw SQL (`FromSql`) skips filters unless composed.
- Tenant filter referencing a captured context field works because EF parameterises it; referencing a static/DI singleton does not.
- Cached models: filters are in the model, so one context type has one model per `OnModelCreating` unless `IModelCacheKeyFactory` is customised.
- Pair soft delete with a unique index filter (`HasFilter("[IsDeleted] = 0")`).

## Verify
`optionsBuilder.LogTo(Console.WriteLine, LogLevel.Information)` shows the WHERE clause; a test inserts a deleted row and asserts it is invisible by default and visible with `IgnoreQueryFilters`.
