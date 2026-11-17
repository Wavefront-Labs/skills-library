---
id: computing-software.software-engineering.csharp-dotnet.taskcompletionsource-and-async-bridging
name: taskcompletionsource-and-async-bridging
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-async, taskcompletionsource, callback-to-task, runcontinuationsasynchronously, cancellation]
level: advanced
status: docs-checked
description: "Wrap callback, event or message-based APIs as awaitable Tasks with TaskCompletionSource, using RunContinuationsAsynchronously, cancellation and timeouts correctly."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/asynchronous-programming-patterns/interop-with-other-asynchronous-patterns-and-types", "https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.taskcompletionsource-1", "https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.taskcreationoptions", "https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.waitasync"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TaskCompletionSource

```csharp
public Task<Reply> SendAsync(Request r, CancellationToken ct)
{
    var tcs = new TaskCompletionSource<Reply>(TaskCreationOptions.RunContinuationsAsynchronously);
    _pending[r.Id] = tcs;                                   // message correlation table
    var reg = ct.Register(() => { if (_pending.TryRemove(r.Id, out var t)) t.TrySetCanceled(ct); });
    tcs.Task.ContinueWith(_ => reg.Dispose(), TaskScheduler.Default);
    _transport.Send(r);
    return tcs.Task;
}
void OnMessage(Reply m) { if (_pending.TryRemove(m.Id, out var t)) t.TrySetResult(m); }
```

`TaskCompletionSource<TResult>` creates a `Task<TResult>` that you complete yourself with `SetResult`, `SetException` or `SetCanceled`. The Microsoft interop page uses it to wrap the older APM and EAP patterns as Tasks.

## Rules
1. Pass `TaskCreationOptions.RunContinuationsAsynchronously` to the constructor: it forces continuations added to the task to execute asynchronously (available since .NET Framework 4.6).
2. Prefer the `TrySet*` methods (`TrySetResult`, `TrySetException`, `TrySetCanceled`, which also accepts a `CancellationToken`) when completion can race, for example a timeout against a reply.
3. Complete it on every path: success, error, cancellation. A source that is never completed leaves its task pending forever.
4. Remove dictionary entries and dispose cancellation registrations so they do not accumulate.
5. For a timeout use `task.WaitAsync(TimeSpan, CancellationToken)`; the returned task faults with a `TimeoutException` if the timeout elapses first. Overloads also take a `TimeProvider`.

## Gotchas
- Prefer built-ins when they fit (`Task.FromResult`, `Task.Run`, `Channel<T>`, `SemaphoreSlim`); use a source for one-shot completion signals.
- Do not block on `tcs.Task.Result` from the thread that must complete the source.

## Verify
Tests: reply completes the task; cancel produces `OperationCanceledException`; a late reply after timeout is ignored; the pending table is empty afterwards.

## Checked
2026-11-08. Confirmed against the TaskCompletionSource<TResult> class page (SetResult, SetException, TrySet* methods, TrySetCanceled(CancellationToken)), the TaskCreationOptions page (RunContinuationsAsynchronously text and .NET Framework 4.6 availability), the Task.WaitAsync page (overloads, TimeoutException, TimeProvider) and the interop page (TaskCompletionSource wraps APM and EAP). Removed as unconfirmed: the deadlock and stall explanation, the non-generic TaskCompletionSource version note, the .NET 6 gate on WaitAsync, and the self-unsubscribing event handler advice. The code sample is illustrative and was not compiled.
Method: documentation only; no commands were run.
