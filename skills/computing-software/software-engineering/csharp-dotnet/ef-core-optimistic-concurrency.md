---
id: computing-software.software-engineering.csharp-dotnet.ef-core-optimistic-concurrency
name: ef-core-optimistic-concurrency
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, ef-core, ef-concurrency-tokens, rowversion, dbupdateconcurrencyexception, optimistic-locking, lost-update, xmin]
level: practitioner
status: docs-checked
description: "Prevent lost updates in EF Core with concurrency tokens (rowversion, xmin, manual tokens), handle DbUpdateConcurrencyException and carry tokens through APIs."
sources:
  - https://learn.microsoft.com/en-us/ef/core/saving/concurrency
  - https://learn.microsoft.com/en-us/ef/core/saving/execute-insert-update-delete
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimistic concurrency in EF Core

**Goal:** when two users edit the same row, the second save fails detectably instead of
silently overwriting the first.

## Configure a token
SQL Server `rowversion` (auto-incremented by the DB on every update):
```csharp
public class Product
{
    public int Id { get; set; }
    public decimal Price { get; set; }
    [Timestamp] public byte[] Version { get; set; } = default!;
}
```
Other providers map `IsRowVersion()` to their own mechanism (check the provider docs, for example the Npgsql concurrency page for PostgreSQL). App-managed token for any provider, such as SQLite:
```csharp
[ConcurrencyCheck] public Guid Version { get; set; }
// set product.Version = Guid.NewGuid() on every change
```
EF then issues `UPDATE ... WHERE Id = @id AND Version = @originalVersion`; zero rows
affected -> `DbUpdateConcurrencyException`.

## Handling the conflict
```csharp
try { await db.SaveChangesAsync(ct); }
catch (DbUpdateConcurrencyException ex)
{
    var entry = ex.Entries.Single();
    var dbValues = await entry.GetDatabaseValuesAsync(ct);
    if (dbValues is null) return Results.NotFound();          // deleted meanwhile
    // Option A: tell the client (for example HTTP 409) with current values
    // Option B: merge rules, then retry:
    entry.OriginalValues.SetValues(dbValues);                 // refresh token
    await db.SaveChangesAsync(ct);
}
```
Choose deliberately: "client wins" (refresh original values and retry), "store wins"
(reload, discard), or ask the user. Silent client-wins defeats the purpose.

## Carrying the token through a web API
The original token must come from what the user SAW, not a fresh load:
- Return it in the DTO (or an HTTP validator such as `ETag`) and require it on update.
- On update: load entity, then `db.Entry(p).Property(x => x.Version).OriginalValue = dto.Version;`
  before applying changes. Otherwise EF compares against the just-loaded value and the
  check is meaningless.

## Notes
- `ExecuteUpdate`/`ExecuteDelete` are unaware of the change tracker, so add the token check to the query yourself if you need it.
- Pessimistic locking via raw SQL suits short critical sections, not user edit flows.

## Verify
- [ ] Integration test: two contexts load the same row, both save; the second throws.
- [ ] API returns a conflict status (for example 409) for a stale token and the response includes current state.

## Checked

Checked 2026-10-25 against dotnet/EntityFramework.Docs (saving/concurrency, saving/execute-insert-update-delete) on main.
Confirmed: `[Timestamp]` maps to SQL Server `rowversion`; `IsRowVersion()`; `[ConcurrencyCheck]` app-managed token (suitable for SQLite); the UPDATE ... WHERE token condition and `DbUpdateConcurrencyException` with `Entries`; `ExecuteUpdate`/`ExecuteDelete` have no interaction with the change tracker.
Removed as unconfirmed: the Npgsql `xmin` mapping snippet, `If-Match` and 412 specifics, the `FOR UPDATE` note.

Method: documentation only; no commands were run.
