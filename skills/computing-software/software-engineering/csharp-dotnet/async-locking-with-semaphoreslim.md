---
id: computing-software.software-engineering.csharp-dotnet.async-locking-with-semaphoreslim
name: async-locking-with-semaphoreslim
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, semaphoreslim, async-lock, mutual-exclusion, throttling, keyed-locks, async-await]
level: practitioner
status: docs-checked
description: "Protect shared state and throttle concurrency in async C# with SemaphoreSlim: WaitAsync with timeout/cancellation, try/finally release, per-key locks, and why lock can't await."
sources: ["https://learn.microsoft.com/en-us/dotnet/api/system.threading.semaphoreslim", "https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/lock", "https://learn.microsoft.com/en-us/dotnet/standard/threading/semaphore-and-semaphoreslim"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async locking with SemaphoreSlim

**Goal:** mutual exclusion and concurrency limits that work across `await`.

## Why not lock
`lock` (Monitor, or `System.Threading.Lock`) is thread-affine: you cannot `await`
inside it, because the continuation may run on another thread.
`SemaphoreSlim` is not thread-affine and has `WaitAsync`.

## Async mutex
```csharp
private readonly SemaphoreSlim _gate = new(1, 1);

public async Task<Token> GetTokenAsync(CancellationToken ct)
{
    if (_cached is { IsExpired: false } t) return t;     // fast path without the lock
    await _gate.WaitAsync(ct);
    try
    {
        if (_cached is { IsExpired: false } t2) return t2;   // double-check after acquiring
        return _cached = await _auth.FetchTokenAsync(ct);
    }
    finally
    {
        _gate.Release();
    }
}
```
- `Release` in `finally`, always; but only if `WaitAsync` actually succeeded - put
  `WaitAsync` **before** the `try`.
- `WaitAsync(TimeSpan, ct)` returns `false` on timeout: check it.
- Not reentrant: awaiting the same semaphore again in a nested call deadlocks.

## Throttling
```csharp
private static readonly SemaphoreSlim Throttle = new(initialCount: 8, maxCount: 8);
await Throttle.WaitAsync(ct);
try { await CallFragileApiAsync(ct); } finally { Throttle.Release(); }
```

## Per-key locks
```csharp
private readonly ConcurrentDictionary<string, SemaphoreSlim> _locks = new();
var gate = _locks.GetOrAdd(key, _ => new SemaphoreSlim(1, 1));
```
The dictionary grows forever; evict with reference counting, or use a striped array
(`_stripes[(hash & int.MaxValue) % N]`).

## Alternatives
- `Channel<T>` with a single reader for serialising work (actor-style) - often cleaner than locks.
- `Lazy<Task<T>>` for one-time async initialisation.
- Across processes/instances: distributed locks (Redis/DB) - SemaphoreSlim is in-process only.

## Gotchas
- Dispose is rarely needed (only if `AvailableWaitHandle` was used).
- Releasing more than acquired throws `SemaphoreFullException` when `maxCount` is set - set it to catch bugs.

## Verify
- [ ] Every `WaitAsync` is followed by `try { } finally { Release(); }`.
- [ ] No `.Wait()` (sync) on semaphores in async code paths.

## Checked

- Date: 2026-10-28
- Confirmed on Microsoft Learn (SemaphoreSlim, WaitAsync, semaphore-and-semaphoreslim, lock statement pages): WaitAsync(TimeSpan, ct) returns a bool, SemaphoreFullException, AvailableWaitHandle, System.Threading.Lock.
- Removed: compiler error number, .NET 9 version note, Parallel.ForEachAsync suggestion, third-party library names.
Method: documentation only; no commands were run.
