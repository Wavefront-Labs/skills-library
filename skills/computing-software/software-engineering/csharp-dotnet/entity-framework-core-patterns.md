---
id: computing-software.software-engineering.csharp-dotnet.entity-framework-core-patterns
name: entity-framework-core-patterns
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, entity-framework-core, ef-core, n-plus-one, change-tracking, asnotracking, dbcontext, lazy-loading, query-splitting]
level: advanced
status: docs-checked
description: "Avoid EF Core's common traps: N+1 queries from lazy loading, cartesian explosion from multiple Includes, change-tracking overhead on read paths, and DbContext lifetime."
sources: ["https://learn.microsoft.com/en-us/ef/core/querying/related-data/lazy", "https://learn.microsoft.com/en-us/ef/core/querying/single-split-queries", "https://learn.microsoft.com/en-us/ef/core/querying/tracking", "https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/", "https://learn.microsoft.com/en-us/ef/core/performance/advanced-performance-topics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EF Core patterns — where the ORM's convenience becomes a performance bug

**Goal:** know the handful of EF Core defaults that are convenient in a demo and
expensive at scale.

## 1. N+1 from lazy loading
```csharp
var orders = context.Orders.ToList();
foreach (var o in orders) { Console.WriteLine(o.Customer.Name); }  // lazy-loads Customer per order
```
Lazy loading is enabled with `UseLazyLoadingProxies()` (Microsoft.EntityFrameworkCore.Proxies
package; navigations must be `virtual`) or by injecting `ILazyLoader`. The docs warn it can
cause unneeded extra database roundtrips, the N+1 problem. Prefer eager loading
(`.Include(...)`) when you know you need the related data, or a projection (`.Select`)
that picks only the columns you need. Don't enable lazy loading unless you need it:
explicit `.Include` makes the cost visible in the code.

## 2. Multiple collection `.Include`s: cartesian explosion
```csharp
var blogs = await ctx.Blogs.Include(b => b.Posts).Include(b => b.Contributors).ToListAsync();
```
EF Core loads related entities with JOINs in a single query by default. Two sibling
collection navigations on the same entity produce a cross product: 10 posts and 10
contributors return 100 rows for that one blog. This does not happen for nested
`Include(...).ThenInclude(...)` collections. `AsSplitQuery()` issues one SQL query per
included collection instead; `UseQuerySplittingBehavior(QuerySplittingBehavior.SplitQuery)`
makes it the default and `AsSingleQuery()` opts a query back out. EF Core warns when a query
loads multiple collections and no splitting mode is configured.

Split queries trade this for drawbacks the docs list: no consistency guarantee across the
multiple queries if the database is updated concurrently, an extra roundtrip per query,
and more buffering in memory on databases that allow only one active query. Measure for
your data shape. With Skip/Take on EF versions before 10, make the ordering fully unique.

## 3. `AsNoTracking()` for read-only queries
```csharp
var products = await context.Products.AsNoTracking().ToListAsync();
```
The change tracker records entities so `SaveChanges` can persist changes. The docs say
no-tracking queries are useful for read-only results and are generally quicker, since
no tracking information is set up; they also do no identity resolution. Use
`AsNoTrackingWithIdentityResolution()` if you need identity resolution without tracking.
`UseQueryTrackingBehavior(QueryTrackingBehavior.NoTracking)` sets the default for a
context. Keep tracked queries for entities you will update and save. Projecting into
an anonymous type also means the result is not tracked.

## 4. DbContext lifetime
A `DbContext` instance is designed for a single unit of work, so its lifetime is usually
very short. In web apps, tying it to the request is a good default, and `AddDbContext`
registers it as a scoped service by default. A `DbContext` is not thread-safe: do not
share one between threads, and await async calls before continuing to use it.

## Gotchas
- Compiled queries (`EF.CompileAsyncQuery`, or `EF.CompileQuery` for synchronous
  queries) exist for hot, identical-shape queries; the performance docs describe them.
- Projecting with `.Select()` into a DTO or anonymous type before materialising fetches
  only the columns you choose (the docs recommend this to omit big columns).

## Verify
- [ ] Any navigation access needed is via explicit `.Include` or projection, confirmed
      by reviewing the generated SQL or query log.
- [ ] Queries with several sibling collection `Include`s were checked for cartesian
      explosion and a single/split mode chosen on purpose.
- [ ] Read-only query paths use `AsNoTracking()`.
- [ ] `DbContext` lifetime matches request/unit-of-work scope, and no instance is
      shared across threads.

## Checked
2026-11-01. Confirmed on Microsoft Learn: Lazy Loading of Related Data (`UseLazyLoadingProxies`,
`virtual` navigations, `ILazyLoader`, N+1 warning); Single vs. Split Queries (cartesian explosion
example, `ThenInclude` exception, `AsSplitQuery`, `AsSingleQuery`, `UseQuerySplittingBehavior`,
warning condition, drawbacks, Skip/Take ordering note); Tracking vs. No-Tracking Queries
(`AsNoTracking`, `UseQueryTrackingBehavior`, identity resolution, anonymous-type projection);
DbContext Lifetime, Configuration, and Initialization (single unit of work, request scope,
scoped `AddDbContext`, not thread-safe); Advanced Performance Topics (`EF.CompileAsyncQuery`,
`EF.CompileQuery`). Removed unconfirmed claims: migration table-lock behaviour and
`Script-Migration` advice, client-evaluation logging advice, `ToQueryString`, singleton
DbContext memory-growth wording, and the profiling advice on compiled queries.
Method: documentation only; no commands were run.

Related: computing-software.software-engineering.csharp-dotnet.aspnet-core-web-apis,
computing-software.software-engineering.concurrency.profiling-before-optimising
