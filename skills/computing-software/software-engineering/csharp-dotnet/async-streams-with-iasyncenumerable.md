---
id: computing-software.software-engineering.csharp-dotnet.async-streams-with-iasyncenumerable
name: async-streams-with-iasyncenumerable
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, async-await, iasyncenumerable, await-foreach, enumeratorcancellation, streaming, asasyncenumerable, system-linq-async]
level: practitioner
status: docs-checked
description: "Stream data asynchronously in .NET with IAsyncEnumerable: async iterators, cancellation with [EnumeratorCancellation], EF Core and ASP.NET Core streaming."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/generate-consume-asynchronous-stream", "https://learn.microsoft.com/en-us/dotnet/api/system.runtime.compilerservices.enumeratorcancellationattribute", "https://learn.microsoft.com/en-us/ef/core/querying/async"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async streams with IAsyncEnumerable

**Goal:** process large or paged data item by item without buffering everything,
while still being async and cancellable.

## Producing
```csharp
public async IAsyncEnumerable<Invoice> GetAllAsync(
    [EnumeratorCancellation] CancellationToken ct = default)
{
    string? cursor = null;
    do
    {
        var page = await _api.ListAsync(cursor, ct);
        foreach (var inv in page.Items) yield return inv;
        cursor = page.Next;
    } while (cursor is not null);
}
```
Without `[EnumeratorCancellation]`, a token passed via `.WithCancellation(ct)` by the
consumer never reaches your method.

## Consuming
```csharp
await foreach (var inv in svc.GetAllAsync().WithCancellation(ct))
    await HandleAsync(inv, ct);
```
By default stream elements are processed in the captured context; use `ConfigureAwait(false)` to avoid capturing it: `await foreach (var x in src.ConfigureAwait(false))`.
The loop disposes the enumerator asynchronously when it finishes (`IAsyncEnumerator<T>` derives from `IAsyncDisposable`).

## LINQ over async streams
.NET 10 introduces `System.Linq.AsyncEnumerable` (also shipped as a NuGet package), which replaces the community `System.Linq.Async` package; on older .NET versions reference `System.Linq.Async`. Buffering a huge stream into a list defeats the point of streaming.

## EF Core
```csharp
await foreach (var row in db.Orders.Where(o => o.Open).AsAsyncEnumerable().WithCancellation(ct))
```
`AsAsyncEnumerable()` streams results from the database instead of buffering them. DbContext is not thread-safe and a second operation started before the previous one completed throws, so avoid other operations on the same context inside the loop.


## Gotchas
- Each `await foreach` runs the iterator again (like `IEnumerable`); don't enumerate twice.
- `Parallel.ForEachAsync` accepts an `IAsyncEnumerable<T>` source and `ParallelOptions.MaxDegreeOfParallelism`.

## Verify
- [ ] Cancelling the consumer's token stops page fetching (verify with a mock counting calls).
- [ ] Memory stays flat while streaming a large result set (measure it).

## Checked

Checked 2026-10-25 against dotnet/docs (generate-consume-asynchronous-stream; compatibility note "System.Linq.AsyncEnumerable in .NET 10") and dotnet/EntityFramework.Docs (miscellaneous/async) on main.
Confirmed: `[EnumeratorCancellation]` and `WithCancellation`; `ConfigureAwait` on async streams; async disposal of the enumerator; `System.Linq.AsyncEnumerable` arrives in .NET 10 and `System.Linq.Async` is the older package; EF Core `AsAsyncEnumerable()`.
Also confirmed: DbContext thread-safety (EF docs dbcontext-configuration) and `Parallel.ForEachAsync` IAsyncEnumerable overloads (dotnet-api-docs).
Removed as unconfirmed: the `WhereAwait`/`SelectAwait` names, the ASP.NET Core JSON streaming section, the DataReader and exception-timing details.

Method: documentation only; no commands were run.
