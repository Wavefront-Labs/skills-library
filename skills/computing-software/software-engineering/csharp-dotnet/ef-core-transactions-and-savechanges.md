---
id: computing-software.software-engineering.csharp-dotnet.ef-core-transactions-and-savechanges
name: ef-core-transactions-and-savechanges
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, ef-transactions, savechanges, execution-strategy, isolation-level, savepoints, ef-core]
level: advanced
status: docs-checked
description: "Control EF Core transactions: implicit SaveChanges transactions, explicit transactions across saves, retrying execution strategies, isolation and savepoints."
sources: ["https://learn.microsoft.com/en-us/ef/core/saving/transactions", "https://learn.microsoft.com/en-us/ef/core/miscellaneous/connection-resiliency", "https://learn.microsoft.com/en-us/ef/core/saving/basic"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EF Core transactions and SaveChanges

**Goal:** atomic business operations that survive transient database failures without
double-applying work.

## SaveChanges is already transactional
All changes tracked in one `SaveChangesAsync` call are sent in a single transaction (batched
statements); on failure nothing is committed. Many operations need nothing more: modify
entities, call SaveChanges once.

## Explicit transactions across several saves
```csharp
await using var tx = await db.Database.BeginTransactionAsync(IsolationLevel.RepeatableRead, ct);
var account = await db.Accounts.SingleAsync(a => a.Id == id, ct);
account.Debit(amount);
await db.SaveChangesAsync(ct);                     // needs generated IDs before the next step
db.Ledger.Add(new LedgerEntry(account.Id, -amount));
await db.SaveChangesAsync(ct);
await db.Database.ExecuteSqlInterpolatedAsync($"SELECT pg_notify('ledger', {account.Id.ToString()})", ct);
await tx.CommitAsync(ct);                          // dispose without commit = rollback
```
Savepoints: `await tx.CreateSavepointAsync("before-items")` / `RollbackToSavepointAsync` (EF also
creates one automatically when SaveChanges runs inside a user transaction).

## Retries and execution strategies
```csharp
o.UseSqlServer(cs, sql => sql.EnableRetryOnFailure(maxRetryCount: 5));
```
With a retrying strategy, a user-initiated transaction throws ("The configured execution strategy
does not support user-initiated transactions") unless the whole unit is wrapped:
```csharp
var strategy = db.Database.CreateExecutionStrategy();
await strategy.ExecuteAsync(async () =>
{
    db.ChangeTracker.Clear();                         // re-run from clean state
    await using var tx = await db.Database.BeginTransactionAsync(ct);
    ... // load, modify, save
    await tx.CommitAsync(ct);
});
```
The delegate may run more than once: make it idempotent, and beware "commit succeeded but the
connection dropped before acknowledgement" - use idempotency keys or verify-on-retry for
non-idempotent effects.

## Isolation and concurrency
The default is the provider's. Prefer optimistic
concurrency tokens for lost-update protection; raise isolation (`Serializable`) only for
specific invariants and handle serialization failures with retries.

## External side effects
Don't call HTTP APIs or publish messages inside the DB transaction and assume atomicity. Use
the transactional outbox: write the message to an outbox table in the same transaction, publish
afterwards.

## TransactionScope
`new TransactionScope(TransactionScopeAsyncFlowOption.Enabled)` works for ambient transactions
across multiple contexts on the **same** connection string; distributed transactions (MSDTC) are
supported on Windows only (.NET 7+) - avoid.

## Checked
2026-10-28: Confirmed in the EF Core transactions, connection resiliency and saving pages: transactional SaveChanges, user transactions with savepoints, the execution-strategy exception text, CreateExecutionStrategy wrapping, distributed transactions added in .NET 7 for Windows only. Removed the Npgsql retry note, the claim about ExecuteUpdate and raw SQL joining the transaction, and the named default isolation levels.
Method: documentation only; no commands were run.

## Verify
- [ ] Multi-step writes either use a single SaveChanges or an explicit transaction inside the execution strategy.
- [ ] Retry paths tested (simulate a transient error) and proven idempotent.
