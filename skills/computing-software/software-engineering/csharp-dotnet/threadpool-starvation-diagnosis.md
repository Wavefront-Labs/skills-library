---
id: computing-software.software-engineering.csharp-dotnet.threadpool-starvation-diagnosis
name: threadpool-starvation-diagnosis
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, csharp-threading, threadpool-starvation, sync-over-async, dotnet-counters, thread-injection]
level: advanced
status: docs-checked
description: "Recognise and fix .NET thread pool starvation: sync-over-async blocking, symptoms, dotnet-counters and dotnet-stack evidence, and why raising MinThreads is a stopgap."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/diagnostics/debug-threadpool-starvation", "https://learn.microsoft.com/en-us/dotnet/standard/threading/the-managed-thread-pool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread pool starvation

Starvation happens when the pool has no free threads for new work items; the app responds slowly under load while CPU stays well below 100%.

## Diagnose
```bash
dotnet-counters monitor -n MyApp
#   dotnet.thread_pool.thread.count rising slowly;  dotnet.thread_pool.queue.length large;  dotnet.thread_pool.work_item.count low
dotnet-stack report -n MyApp          # constant blocking: threads parked in Task.Wait / GetResult frames
dotnet-trace collect -n MyApp ...     # sporadic blocking: collect over time, analyse the .nettrace later
```
- Signals from the docs: after a rapid rise to 2-3x the processor count, the pool adds about 1-2 threads per second; the key signals are that slow steady climb and CPU far below 100%. Large queue length with low completed work items is common but not guaranteed.
- A thread count that stabilises above roughly three times the core count usually means application code blocks pool threads and the pool compensates. Each thread also costs memory, and after load changes or restarts the pool starves again while it ramps up.
- Starting in .NET 6 the pool scales up much faster in response to certain blocking Task APIs, so starvation lasts a shorter time but can still occur.
- `dotnet-stack` suits consistent blocking in every request; `dotnet-trace` suits blocking that happens only every few minutes; a `dotnet-dump` can be opened in Visual Studio for better visualisation.
- In dotnet-counters output, the counter names above apply to .NET 9 and later; older versions display differently.

## Fix
To eliminate starvation, keep pool threads unblocked. Typical culprits:
1. Sync-over-async: `.Result`, `.Wait()`, `GetAwaiter().GetResult()` in request paths (visible as `Task.GetResultCore` and `SpinThenBlockingWait` frames in `dotnet-stack`). Make the call chain async end to end.
2. Other blocking calls (synchronous I/O, `Thread.Sleep`) inside request handlers: use async APIs.
3. Long CPU work or unbounded fan-out on pool threads: limit concurrency.

## Stopgap
`ThreadPool.SetMinThreads` raises the number of threads created on demand without the ramp-up delay. The docs warn that unnecessarily raising the minimum can cause performance problems and that the pool usually performs better with its own algorithm. Treat it as a measured stopgap, not the fix.

## Verify
After the fix, queue length stays low under load and the thread count no longer climbs; re-run `dotnet-stack` and confirm no threads wait in `GetResult` frames.

## Checked
2026-11-08. Confirmed against the "Debug ThreadPool starvation" tutorial (counters, 2-3x then 1-2 per second growth, three-times-cores heuristic, .NET 6 heuristics change, dotnet-stack vs dotnet-trace guidance, GetResultCore frames) and the Managed thread pool page (SetMinThreads warning). Removed as unconfirmed: step-per-thread latency figures, the EventPipe provider and keyword string, the runtime starvation warning event, specific SetMinThreads values and the runtimeconfig key, the 1-CPU container remark, the ConfigureAwait remark, and the Parallel.ForEachAsync and Channel recommendations.
Method: documentation only; no commands were run.
