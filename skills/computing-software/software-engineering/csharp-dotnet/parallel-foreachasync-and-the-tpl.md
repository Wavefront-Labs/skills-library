---
id: computing-software.software-engineering.csharp-dotnet.parallel-foreachasync-and-the-tpl
name: parallel-foreachasync-and-the-tpl
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, parallel-foreachasync, tpl, plinq, maxdegreeofparallelism, data-parallelism]
level: practitioner
status: docs-checked
description: "Choose .NET parallelism: Parallel.ForEachAsync for async work, Parallel.For/ForEach and PLINQ for data parallelism, with degree-of-parallelism and ordering controls."
sources:
  - https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/task-parallel-library-tpl
  - https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.parallel.foreachasync
  - https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/introduction-to-plinq
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallel.ForEachAsync and the TPL

**Goal:** pick the right parallel construct and limit how much runs at once.

## Choosing
- `Parallel.ForEachAsync` runs an async body over a sequence; its overloads that take no options execute at most `ProcessorCount` operations in parallel. Pass `ParallelOptions` (with `MaxDegreeOfParallelism` and `CancellationToken`) to change that. A cancelled token is stored in the returned task as an `OperationCanceledException`.
- PLINQ (`AsParallel()`) uses all processors by default. `WithDegreeOfParallelism(n)` caps the processors used, for example to leave CPU time for other processes. `AsOrdered()` preserves source ordering for the rest of the query.
- If exceptions bubble up to the joining thread in PLINQ, the query may continue to process some items after the exception is raised.
- For multi-stage operations that must communicate and process data as it becomes available, the TPL Dataflow library is the documented option.

## Verify
- [ ] The degree of parallelism is set deliberately instead of left at the default where the downstream system is fragile.
- [ ] Order-sensitive PLINQ queries use `AsOrdered()`.

## Checked
2026-11-01. Confirmed against Microsoft Learn: the Parallel.ForEachAsync API page (ProcessorCount default for overloads without options, cancellation behaviour), Introduction to PLINQ (defaults, WithDegreeOfParallelism, AsOrdered, exceptions) and the TPL overview (Dataflow). Removed as unconfirmed by those pages: the first-exception-cancels claim, async-void warning for Parallel.ForEach, Partitioner sizes, thread-pool injection rate, ActionBlock BoundedCapacity advice, thread-local aggregation sample and ASP.NET guidance.
Method: documentation only; no commands were run.
