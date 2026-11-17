---
id: computing-software.software-engineering.csharp-dotnet.ef-core-logging-and-interceptors
name: ef-core-logging-and-interceptors
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, ef-logging, ef-interceptors, toquerystring, savechanges-interceptor, slow-query-logging, ef-core, ef-slow-queries, ef-core-operations]
level: practitioner
status: docs-checked
description: "See and shape what EF Core sends to the database: LogTo and logging categories, ToQueryString, sensitive data logging, and interceptors for auditing, soft delete and slow queries."
sources: ["https://learn.microsoft.com/en-us/ef/core/logging-events-diagnostics/", "https://learn.microsoft.com/en-us/ef/core/logging-events-diagnostics/interceptors", "https://learn.microsoft.com/en-us/ef/core/logging-events-diagnostics/simple-logging"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# EF Core logging and interceptors

**Goal:** know the exact SQL each LINQ query produces, and hook cross-cutting behaviour
into EF without polluting business code.

## Seeing SQL
```csharp
var q = db.Orders.Where(o => o.Total > 100).OrderBy(o => o.Number);
Console.WriteLine(q.ToQueryString());              // SQL with parameter declarations, no execution

options.LogTo(Console.WriteLine, LogLevel.Information)        // simple logging
       .EnableSensitiveDataLogging()                          // parameter VALUES - development only
       .EnableDetailedErrors();
```
Simple logging includes every message at `Debug` level or above by default; pass a minimum `LogLevel` to `LogTo` to reduce it. Tag queries for
traceability in DB tools: `db.Orders.TagWith("OrdersController.List")`.

## SaveChanges interceptor: audit fields
```csharp
public sealed class AuditInterceptor(TimeProvider time, ICurrentUser user) : SaveChangesInterceptor
{
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData e, InterceptionResult<int> result, CancellationToken ct = default)
    {
        foreach (var entry in e.Context!.ChangeTracker.Entries<IAuditable>())
        {
            if (entry.State == EntityState.Added) entry.Entity.CreatedAt = time.GetUtcNow();
            if (entry.State is EntityState.Added or EntityState.Modified)
            { entry.Entity.UpdatedAt = time.GetUtcNow(); entry.Entity.UpdatedBy = user.Id; }
            if (entry.State == EntityState.Deleted && entry.Entity is ISoftDeletable s)
            { entry.State = EntityState.Modified; s.IsDeleted = true; }       // soft delete
        }
        return base.SavingChangesAsync(e, result, ct);
    }
}
builder.Services.AddScoped<AuditInterceptor>();
builder.Services.AddDbContext<AppDbContext>((sp, o) => o.UseNpgsql(cs).AddInterceptors(sp.GetRequiredService<AuditInterceptor>()));
```

## Command interceptor: slow queries
```csharp
public sealed class SlowQueryInterceptor(ILogger<SlowQueryInterceptor> log) : DbCommandInterceptor
{
    public override ValueTask<DbDataReader> ReaderExecutedAsync(DbCommand cmd, CommandExecutedEventData e,
        DbDataReader result, CancellationToken ct = default)
    {
        if (e.Duration > TimeSpan.FromMilliseconds(500))
            log.LogWarning("Slow query {Ms} ms: {Sql}", e.Duration.TotalMilliseconds, cmd.CommandText);
        return base.ReaderExecutedAsync(cmd, e, result, ct);
    }
}
```
Other interceptor interfaces: `IDbConnectionInterceptor` (opening and closing connections), `IDbTransactionInterceptor`, `IMaterializationInterceptor` (creating and initializing entity instances). Register interceptors with `AddInterceptors` when configuring the DbContext.

## Verify
- [ ] Sensitive data logging only enabled in Development (guarded by environment check).
- [ ] Slow-query warnings configured.

## Checked

Checked 2026-10-25 against dotnet/EntityFramework.Docs (logging-events-diagnostics: simple-logging, interceptors, index; querying/tags) on main.
Confirmed: `LogTo` with a minimum `LogLevel` (default Debug and above); `EnableSensitiveDataLogging` and `EnableDetailedErrors`; `AddInterceptors`; interceptor interfaces (`IDbCommandInterceptor`, `IDbConnectionInterceptor`, `IDbTransactionInterceptor`, `ISaveChangesInterceptor`, `IMaterializationInterceptor`); `TagWith`; `ReaderExecutingAsync` override shape.
Removed as unconfirmed: the `Database.Command` category and level, the `ConfigureWarnings` throw block and event ids, the EF Core 3 client-evaluation note, the third-party OpenTelemetry instrumentation package.

Method: documentation only; no commands were run.
