---
id: computing-software.software-engineering.csharp-dotnet.async-await-and-task-based-concurrency
name: async-await-and-task-based-concurrency
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, async-await, task, valuetask, configureawait, sync-over-async, deadlock, synchronizationcontext, cancellationtoken, async-void, csharp-async]
level: advanced
status: docs-checked
description: "Write correct async C#: avoid sync-over-async deadlocks, pick ConfigureAwait(false) deliberately, and when ValueTask actually helps over Task."
sources: ["https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios", "https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.valuetask-1", "https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.configureawait"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Async/await in C# — the sync-over-async deadlock and when ValueTask earns its keep

**Goal:** write async code that doesn't deadlock when something up the call stack
blocks on it, and know when `ValueTask` is a real optimisation versus unnecessary
complexity.

## 1. The sync-over-async deadlock
```csharp
var result = GetDataAsync().Result;   // or .Wait(), or .GetAwaiter().GetResult()
```
Microsoft's async guidance: blocking the current thread to wait synchronously for a
`Task` can result in deadlocks and blocked context threads, and it also wraps
exceptions in `AggregateException` (for `Wait`/`Result`). The preferred solution is to use
async/await throughout your call stack, retrieving results with `await`, not
`Task.Wait` or `Task.Result`.

If you truly cannot (a legacy synchronous boundary), the same guidance shows
wrapping the call in `Task.Run(async () => await GetDataAsync()).GetAwaiter().GetResult()`
as a workaround for complex scenarios; it still blocks a thread.

## 2. `ConfigureAwait(false)`
```csharp
await SomeAsync().ConfigureAwait(false);
```
The parameter is `continueOnCapturedContext`: `true` attempts to marshal the continuation
back to the captured context, `false` does not. The API docs say that when a method awaits
a task directly, the continuation usually occurs in the thread that created the task,
depending on the async context; this can be costly and can result in a deadlock on the
UI thread, and calling `ConfigureAwait(false)` avoids both. See the ConfigureAwait FAQ
linked from that page for when it matters in your host.

## 3. `Task` vs `ValueTask`
`ValueTask<TResult>` is a struct for methods that are likely to complete synchronously
and are invoked so frequently that allocating a `Task` per call would be prohibitive. The
docs say the default choice for any asynchronous method should be `Task` or
`Task<TResult>`, and `ValueTask` should be used only if performance analysis proves it
worthwhile. A `ValueTask<TResult>` may only be awaited once, and you may not read `Result`
until it has completed. Never: await it multiple times, call `AsTask` multiple times,
or use `.Result`/`.GetAwaiter().GetResult()` before completion or more than once. If those
limits are unacceptable, convert with `AsTask`. When a `Task`-returning method completes
synchronously and successfully, the docs point to `Task.CompletedTask`.

## 4. `async void` only for event handlers
```csharp
private async void OnClick(object sender, RoutedEventArgs e) { await DoWorkAsync(); }  // OK: event handler
```
Event handlers must return `void`, so `async void` is acceptable there. Elsewhere it
doesn't follow the Task-based model: exceptions thrown in an `async void` method can't
be caught outside that method, such methods are difficult to test, and they can have
negative side effects if the caller doesn't expect them to be asynchronous. Return `Task`
instead.

## 5. `Task.Run` is for CPU-bound work
The async-scenarios guide: for I/O-bound work (such as waiting for data from a database),
use `async`/`await` without `Task.Run`; for CPU-bound work, `await` a `Task.Run` so the
caller stays responsive. Don't wrap already-async I/O in `Task.Run`.

## Verify
- [ ] No `.Result`/`.Wait()`/`.GetAwaiter().GetResult()` on an in-flight `Task` in
      code that can be reached from a UI or other captured-context caller.
- [ ] `ValueTask` is used only where measurement justified it, and every call site awaits
      it exactly once.
- [ ] No `async void` outside an event-handler signature.
- [ ] `Task.Run` appears only around CPU-bound work or a deliberate sync-over-async bridge.

## Checked
2026-11-01. Confirmed on Microsoft Learn: Asynchronous programming scenarios (blocking can cause
deadlocks, use async/await throughout the call stack, `Task.Wait`/`Result` wrap exceptions in
`AggregateException`, `Task.Run(async () => await ...).GetAwaiter().GetResult()` workaround,
async void rules, I/O-bound vs CPU-bound guidance); `ValueTask<TResult>` struct docs
(await once, `AsTask`, never-do list, default to `Task`, `Task.CompletedTask`);
`Task.ConfigureAwait` docs (`continueOnCapturedContext`, UI-thread deadlock note). Removed
unconfirmed claims: ASP.NET Core having no SynchronizationContext and its ConfigureAwait
guidance, library-code consistency advice, CancellationToken.None default-parameter
claim, `Task.WhenAll` exception aggregation detail, and `await using` versus `using` behaviour.
Method: documentation only; no commands were run.

Related: computing-software.software-engineering.csharp-dotnet.aspnet-core-web-apis,
computing-software.software-engineering.python.asyncio-concurrency-patterns
