---
id: computing-software.software-engineering.csharp-dotnet.ef-core-relationships-and-loading
name: ef-core-relationships-and-loading
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, ef-relationships, eager-loading, lazy-loading, include, projections, ef-core]
level: practitioner
status: docs-checked
description: "Model and load EF Core relationships: delete behaviours, Include vs projections, split queries against cartesian explosion, explicit and lazy loading, N+1."
sources: ["https://learn.microsoft.com/en-us/ef/core/modeling/relationships", "https://learn.microsoft.com/en-us/ef/core/querying/related-data/", "https://learn.microsoft.com/en-us/ef/core/saving/cascade-delete"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EF Core relationships and loading

**Goal:** correct foreign keys and delete rules, and queries that fetch exactly the
related data needed in as few round trips as sensible.

## Configuring relationships
```csharp
e.HasMany(c => c.Orders)
 .WithOne(o => o.Customer)
 .HasForeignKey(o => o.CustomerId)
 .OnDelete(DeleteBehavior.Restrict);           // don't cascade-delete order history

e.HasMany(p => p.Tags).WithMany(t => t.Posts)
 .UsingEntity(j => j.ToTable("post_tags"));     // skip navigation, implicit join entity
```
Expose FK properties (`CustomerId`) alongside navigations: lets you set relations without loading
the principal and keeps queries simple. Required vs optional follows FK nullability.

Delete behaviours: `Cascade` (default for required), `ClientSetNull` (default for optional),
`Restrict`/`NoAction`, `SetNull`.

## Loading strategies
**Projection (best for reads)**
```csharp
var list = await db.Orders.Where(o => o.CustomerId == id)
    .Select(o => new OrderSummary(o.Id, o.Number, o.Lines.Count, o.Lines.Sum(l => l.Qty * l.Price)))
    .ToListAsync(ct);
```
Fetches only needed columns; no tracking; aggregates in SQL.

**Eager loading**
```csharp
var order = await db.Orders
    .Include(o => o.Lines).ThenInclude(l => l.Product)
    .Include(o => o.Customer)
    .AsSplitQuery()                         // separate SQL per collection: avoids cartesian explosion
    .SingleAsync(o => o.Id == id, ct);
```
Filtered include: `.Include(o => o.Lines.Where(l => !l.Cancelled))`. Multiple collection
includes in one JOIN multiply rows (orders x lines x payments); use split queries
or projection.

**Explicit loading**
`await db.Entry(order).Collection(o => o.Lines).LoadAsync(ct);` when needed conditionally.

**Lazy loading** (`UseLazyLoadingProxies`, virtual navigations): convenient, but produces N+1
queries silently and fails after the context is disposed. Avoid in web apps; if used, detect N+1
via logging.

## Spotting N+1
Enable SQL logging in development; a loop that triggers one SELECT per item is N+1. Fix with
projection or Include.

## Gotchas
- Navigation fix-up: tracked entities get navigations populated from other queries in the same
  context - results can look "loaded" when they aren't loaded by this query.
- Serialising entities with cycles (Customer.Orders[0].Customer) fails or loops; return DTOs.

## Checked
2026-10-28: Confirmed in the EF Core relationships, eager loading, single vs split queries and cascade delete pages: ClientSetNull/Restrict/Cascade/SetNull behaviours, Include/ThenInclude, AsSplitQuery, lazy loading proxies. Removed the SQL Server cascade-path claim, the EF warning claim and the profiler tools.
Method: documentation only; no commands were run.

## Verify
- [ ] Hot endpoints issue a bounded number of SQL statements regardless of result size.
- [ ] Delete behaviours reviewed in the migration (`ON DELETE` clauses).
