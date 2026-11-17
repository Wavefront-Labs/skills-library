---
id: computing-software.software-engineering.csharp-dotnet.ef-core-raw-sql-and-bulk-updates
name: ef-core-raw-sql-and-bulk-updates
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, ef-core, executeupdate, executedelete, ef-raw-sql, fromsql, sqlquery, sql-injection, bulk-operations]
level: practitioner
status: docs-checked
description: "Use EF Core raw SQL safely (FromSql, SqlQuery, ExecuteSql with interpolated parameters) and set-based ExecuteUpdate/ExecuteDelete instead of load-modify-save loops."
sources: ["https://learn.microsoft.com/en-us/ef/core/querying/sql-queries", "https://learn.microsoft.com/en-us/ef/core/saving/execute-insert-update-delete"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw SQL and bulk updates in EF Core

**Goal:** drop to SQL when LINQ can't express something or is too slow, without SQL
injection or out-of-sync tracked entities.

## Set-based updates (ExecuteUpdate and ExecuteDelete)
```csharp
await db.Orders
    .Where(o => o.Status == Status.Pending && o.CreatedAt < cutoff)
    .ExecuteUpdateAsync(s => s
        .SetProperty(o => o.Status, Status.Expired)
        .SetProperty(o => o.UpdatedAt, DateTime.UtcNow), ct);

await db.Sessions.Where(s => s.ExpiresAt < now).ExecuteDeleteAsync(ct);
```
One SQL statement instead of loading N entities. Caveats:
- Takes effect immediately, outside `SaveChanges`, and does not start a transaction implicitly (open one with `db.Database.BeginTransactionAsync()` if several operations must succeed together).
- The change tracker is not updated: already-tracked entities keep their old values. Avoid mixing tracked changes with these calls.
- It is unaware of the change tracker, so set audit fields explicitly in `SetProperty`.
- `ExecuteUpdate` does not support referencing navigations inside the `SetProperty` lambda.

## Raw SQL queries
```csharp
var rows = await db.Products
    .FromSql($"SELECT * FROM products WHERE search_vector @@ plainto_tsquery({term})")
    .Where(p => p.Active)              // composes: EF wraps it as a subquery
    .ToListAsync(ct);

var totals = await db.Database
    .SqlQuery<MonthTotal>($"SELECT date_trunc('month', created) AS Month, sum(total) AS Total FROM orders GROUP BY 1")
    .ToListAsync(ct);                  // non-entity types (EF Core 8)

await db.Database.ExecuteSqlAsync($"CALL refresh_stats({tenantId})", ct);
```
`FromSql`/`SqlQuery`/`ExecuteSql` take a `FormattableString`: interpolated values are wrapped in a `DbParameter`, so they are safe against SQL injection (`FromSql` was introduced in EF Core 7.0).

## The injection trap
`FromSqlRaw`/`ExecuteSqlRaw` take a plain string:
```csharp
db.Users.FromSqlRaw($"SELECT * FROM users WHERE name = '{name}'")   // INJECTABLE
db.Users.FromSqlRaw("SELECT * FROM users WHERE name = {0}", name)   // parameterised
```
Databases do not allow parameterising column names or other schema parts, so a dynamic identifier forces the Raw variants; validate such values against an allowlist.

## Mapping rules
`FromSql` is for entity types in your model and can only be used directly on a `DbSet`; use `SqlQuery<T>` for non-entity results.

## Verify
- [ ] No `FromSqlRaw` or `ExecuteSqlRaw` call interpolates user-supplied values into the SQL string.
- [ ] SQL log shows a single UPDATE/DELETE for bulk operations.
- [ ] Audit fields are still set where required (handled explicitly in the ExecuteUpdate).

## Checked

Checked 2026-10-25 against dotnet/EntityFramework.Docs (querying/sql-queries, saving/execute-insert-update-delete, what-is-new/ef-core-8.0) on main.
Confirmed: `FromSql` (EF Core 7.0) with interpolated parameters, `FromSqlRaw` for dynamic identifiers, composing LINQ over `FromSql` as a subquery, `SqlQuery<T>` for non-entity types, `ExecuteUpdate`/`ExecuteDelete` take effect immediately, start no implicit transaction, leave the change tracker stale, and cannot reference navigations in `SetProperty`.
Removed as unconfirmed: the interceptor and concurrency-token bypass claims, batching `Take` loops advice, the "must return all columns with matching names" rule and keyless-type advice, the grep check.

Method: documentation only; no commands were run.
