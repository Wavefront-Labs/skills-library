---
id: computing-software.software-engineering.csharp-dotnet.periodictimer-background-loops
name: periodictimer-background-loops
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-async, periodictimer, backgroundservice, timers, no-overlap-ticks]
level: practitioner
status: docs-checked
description: "Run periodic async work with PeriodicTimer (.NET 6+) in a BackgroundService: single consumer, awaiting ticks, cancellation, error handling, TimeProvider constructor."
sources: ["https://learn.microsoft.com/en-us/dotnet/api/system.threading.periodictimer", "https://learn.microsoft.com/en-us/dotnet/core/extensions/workers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PeriodicTimer loops

```csharp
public sealed class Refresher(IServiceScopeFactory scopes, ILogger<Refresher> log) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stop)
    {
        using var timer = new PeriodicTimer(TimeSpan.FromMinutes(1));
        try {
            while (await timer.WaitForNextTickAsync(stop))
            {
                try {
                    await using var scope = scopes.CreateAsyncScope();   // scoped services need a scope per tick
                    await scope.ServiceProvider.GetRequiredService<IRefreshJob>().RunAsync(stop);
                }
                catch (Exception ex) when (ex is not OperationCanceledException) { log.LogError(ex, "tick failed"); }
            }
        } catch (OperationCanceledException) { }
    }
}
```
## What the docs state
- `PeriodicTimer` "enables waiting asynchronously for timer ticks"; it is `IDisposable` and sealed.
- Single consumer: only one `WaitForNextTickAsync` call may be in flight at a time.
- `Dispose()` may be called concurrently with an active `WaitForNextTickAsync` to interrupt it, which then returns `false`.
- Constructors: `PeriodicTimer(TimeSpan)` and `PeriodicTimer(TimeSpan, TimeProvider)`; the `Period` property can be get/set. Available from .NET 6.
- `BackgroundService` is an abstract class implementing `IHostedService`; subclasses implement `ExecuteAsync(CancellationToken)`. The worker template's loop runs until the stopping token signals cancellation. If you override `StartAsync` or `StopAsync` you must call and await the base method.
- A run-once worker must call `IHostApplicationLifetime.StopApplication()` or the host runs indefinitely.

## Practitioner notes (not stated on the cited pages)
- Awaiting each tick inside the loop means ticks are only consumed when the previous run has finished, so work does not overlap; the pages do not describe how missed ticks are handled, so test that behaviour.
- Create a DI scope per tick for scoped services (the worker page does not cover this).
- Catch exceptions inside the loop; whether an unhandled exception stops the host is host-configuration dependent, so check your version's documentation.
- The first tick comes after one period; run the job once before the loop for an immediate run.

## Verify
With `FakeTimeProvider`, advance the period and assert the job ran once per tick and never concurrently; cancel and confirm the service exits promptly.

## Checked
Method: 2026-11-08 docs-only read of the PeriodicTimer API page and the Worker Services page. Single-consumer, dispose-returns-false, constructor and BackgroundService claims match. Removed unsupported claims: tick coalescing, "cancel throws", the Timer-overlap and async-void comparison, BackgroundServiceExceptionBehavior default, and the "drift" claim; kept practical advice labelled as unstated by the pages.
