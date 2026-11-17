---
id: computing-software.software-engineering.csharp-dotnet.async-timeouts-cancelafter-and-waitasync
name: async-timeouts-cancelafter-and-waitasync
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, cancelafter, waitasync, async-timeouts, linked-cancellation, timeprovider, async-await]
level: practitioner
status: docs-checked
description: "Put deadlines on async .NET code: CancelAfter with linked tokens, Task.WaitAsync, telling timeout from caller cancellation, and TimeProvider in tests."
sources:
  - https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads
  - https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.waitasync
  - https://learn.microsoft.com/en-us/dotnet/api/system.net.http.httpclient.timeout
  - https://learn.microsoft.com/en-us/dotnet/standard/datetime/timeprovider-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async timeouts: CancelAfter and WaitAsync

**Goal:** every external call has a deadline, timeouts are reported as timeouts, and
abandoned work actually stops.

## Timeout via a linked token
```csharp
public async Task<Quote> GetQuoteAsync(string sym, CancellationToken ct)
{
    using var cts = CancellationTokenSource.CreateLinkedTokenSource(ct);   // caller cancel OR timeout
    cts.CancelAfter(TimeSpan.FromSeconds(3));
    try
    {
        return await _client.GetFromJsonAsync<Quote>($"/quotes/{sym}", cts.Token)
               ?? throw new InvalidOperationException("empty quote");
    }
    catch (OperationCanceledException) when (!ct.IsCancellationRequested)
    {
        throw new TimeoutException($"Quote for {sym} timed out after 3s");    // our timeout, not the caller's
    }
}
```
Dispose linked sources (`using`) so their registration on the parent token is released.

## Task.WaitAsync
```csharp
var result = await SomeApiWithoutTokenAsync().WaitAsync(TimeSpan.FromSeconds(5), ct);
```
Faults with `TimeoutException` after 5 s - but the underlying operation **keeps running**; it only
stops waiting. Use it for APIs that accept no token; prefer real cancellation otherwise.

## HttpClient specifics
`HttpClient.Timeout` defaults to 100 seconds and cancels the request task when reached; it only applies to the `xxxAsync` methods that start a request. Prefer per-call tokens or resilience handlers for finer control.

## Layering
Outer (request) deadline > operation deadline > per-attempt deadline. Pass the request's
`HttpContext.RequestAborted` / ASP.NET `CancellationToken` parameter down so client disconnects stop work.

## Testable time
```csharp
public sealed class Poller(TimeProvider time)
{
    public Task WaitAsync(CancellationToken ct) => Task.Delay(TimeSpan.FromMinutes(5), time, ct);
}
// test: var fake = new FakeTimeProvider(); fake.Advance(TimeSpan.FromMinutes(5));
```
`TimeProvider` is included in the framework from .NET 8 and works with `CancellationTokenSource(TimeSpan, TimeProvider)`,
`Task.Delay(TimeSpan, TimeProvider, CancellationToken)` and `Task.WaitAsync(TimeSpan, TimeProvider, CancellationToken)`; `FakeTimeProvider` lives in the
`Microsoft.Extensions.TimeProvider.Testing` NuGet package.

## Gotchas
- `OperationCanceledException` vs `TaskCanceledException`: catch the base `OperationCanceledException`.
- `CancellationToken.None` passed deep down disables every timeout above it - grep for it.

## Verify
- [ ] Timeouts surface as `TimeoutException` (or a domain error), caller cancellation as cancellation.
- [ ] Tests use FakeTimeProvider instead of real delays.

## Checked

Checked 2026-10-25 against dotnet/dotnet-api-docs (Task, HttpClient, CancellationTokenSource) and dotnet/docs (timeprovider-overview) on main.
Confirmed: `Task.WaitAsync(TimeSpan, CancellationToken)` faults with `TimeoutException`; `HttpClient.Timeout` default 100 s; `CancellationTokenSource(TimeSpan, TimeProvider)`, `Task.Delay(TimeSpan, TimeProvider, CancellationToken)` and `Task.WaitAsync` TimeProvider overloads; `TimeProvider` in the framework from .NET 8; `FakeTimeProvider` in `Microsoft.Extensions.TimeProvider.Testing`.
Removed as unconfirmed: inner `TimeoutException` on HttpClient timeouts, `AddStandardResilienceHandler` timeout details, the linked-source leak explanation.

Method: documentation only; no commands were run.
