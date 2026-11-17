---
id: computing-software.software-engineering.csharp-dotnet.task-whenall-and-concurrent-awaits
name: task-whenall-and-concurrent-awaits
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, task-whenall, task-whenany, concurrent-async, aggregateexception, task-wheneach, async-await]
level: practitioner
status: docs-checked
description: "Run independent async operations concurrently with Task.WhenAll, WhenAny and WhenEach: when each completes, how a faulted task surfaces its exception, and when to use WhenEach."
sources:
  - https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/start-multiple-async-tasks-and-process-them-as-they-complete
  - https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.whenall
  - https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.wheneach
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task.WhenAll and concurrent awaits

**Goal:** overlap independent async operations instead of awaiting them one after another.

## The three combinators
- `Task.WhenAll(tasks)` returns a task that completes when all of the supplied tasks have completed. Start the tasks first (call the async methods), then await the combined task.
- `Task.WhenAny(tasks)` lets you start several tasks and process them one by one as they complete rather than in the order started.
- `Task.WhenEach(tasks)` (.NET 9 and later) returns an `IAsyncEnumerable` that yields the supplied tasks as they complete, so you iterate with `await foreach` instead of looping on `WhenAny` and removing finished tasks.

```csharp
await foreach (Task<int> t in Task.WhenEach(downloadTasks))
    Use(await t);
```

## Reading results and exceptions
- Awaiting a faulted task throws the first child exception stored in its `AggregateException`; reading `.Result` throws the `AggregateException` itself.
- A task returned by `WhenAny` is already complete, but await it to get its result and to surface its exception.
- A `WhenAny` loop is fine for a small number of tasks; for many tasks prefer `WhenEach`.

## Verify
- [ ] Independent awaits run concurrently: tasks are started before any is awaited.
- [ ] Each task returned by `WhenAny` or `WhenEach` is awaited so faults are observed.
- [ ] Large fan-out uses `WhenEach` rather than a `WhenAny` loop.

## Checked
2026-11-01. Confirmed against Microsoft Learn: "Start multiple async tasks and process them as they complete" (WhenAny processing, first child exception from AggregateException versus .Result, WhenEach introduced in .NET 9, WhenAny loop suited to few tasks) and the Task.WhenAll and Task.WhenEach API pages (completion semantics). Removed as unconfirmed by those pages: latency figures, unbounded fan-out and SemaphoreSlim advice, the claim that WhenAll rethrows only the first exception, linked-cancellation first-wins pattern, and the DbContext concurrency note.
Method: documentation only; no commands were run.
