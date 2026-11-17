---
id: computing-software.software-engineering.csharp-dotnet.ado-net-commands-and-sqlclient-resiliency
name: ado-net-commands-and-sqlclient-resiliency
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-ado-net, dbcommand-parameters, sqlclient-resiliency, sqlinjection, connection-pooling, transient-faults]
level: practitioner
status: draft
description: "Use ADO.NET safely: parameterised DbCommand, async readers, transactions, connection pooling and Microsoft.Data.SqlClient transient-fault retry (configurable retry logic, Encrypt defaults)."
sources: ["https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/ado-net-overview", "https://learn.microsoft.com/en-us/sql/connect/ado-net/configurable-retry-logic-sqlclient-introduction", "https://learn.microsoft.com/en-us/sql/connect/ado-net/sql-server-connection-pooling"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ADO.NET commands and SqlClient resiliency

```csharp
await using var conn = new SqlConnection(cs);          // pooled; Open late, Dispose early
await conn.OpenAsync(ct);
await using var tx = (SqlTransaction)await conn.BeginTransactionAsync(IsolationLevel.ReadCommitted, ct);

await using var cmd = new SqlCommand("SELECT Id, Name FROM Users WHERE Email = @email AND Active = @a", conn, tx);
cmd.Parameters.Add("@email", SqlDbType.NVarChar, 256).Value = email;     // typed params: correct plan reuse, no injection
cmd.Parameters.Add("@a", SqlDbType.Bit).Value = true;
cmd.CommandTimeout = 30;
await using var r = await cmd.ExecuteReaderAsync(CommandBehavior.SequentialAccess, ct);
while (await r.ReadAsync(ct)) Console.WriteLine($"{r.GetInt32(0)} {r.GetString(1)}");
await tx.CommitAsync(ct);
```
## Rules
- **Never concatenate user input into SQL.** Identifiers (table/column) cannot be parameters: allowlist them. `IN` lists: table-valued parameters or generated `@p0,@p1`.
- Specify parameter type and size (`AddWithValue` infers poorly and causes plan cache bloat / implicit conversions).
- Pooling is keyed on the exact connection string; keep it constant. Leaks (not disposing) exhaust `Max Pool Size` (100) with timeout errors.
- Prefer provider-neutral `DbConnection`/`DbCommand` via `DbProviderFactory` only if multi-DB is needed.
- `ExecuteScalarAsync`, `ExecuteNonQueryAsync` for single values/DML; `SqlBulkCopy` for bulk inserts.

## Resiliency (Microsoft.Data.SqlClient 3.0+)
```csharp
var opts = new SqlRetryLogicOption { NumberOfTries = 5, DeltaTime = TimeSpan.FromSeconds(1), MaxTimeInterval = TimeSpan.FromSeconds(20),
                                      TransientErrors = new[] { 4060, 40197, 40501, 40613, 49918 } };
var provider = SqlConfigurableRetryFactory.CreateExponentialRetryProvider(opts);
conn.RetryLogicProvider = provider; cmd.RetryLogicProvider = provider;
```
Retry only idempotent commands; never inside a user transaction mid-way (retry the whole unit). EF Core adds `EnableRetryOnFailure()` and requires `CreateExecutionStrategy().ExecuteAsync` for manual transactions. Version 4.0+ defaults `Encrypt=true`; trust certs properly, not `TrustServerCertificate=true` in production.

## Gotchas
- Use `Microsoft.Data.SqlClient`, not legacy `System.Data.SqlClient`.
- MARS and long-lived readers hold connections.
- Timeouts: `CommandTimeout` (seconds) separate from `Connect Timeout`.
- Cancel tokens abort server-side work; check logs for partial effects outside transactions.

## Verify
Test with a hostile string (`' OR 1=1 --`) returning zero rows, and a fault-injection run (kill connection) showing retries and eventual success.
