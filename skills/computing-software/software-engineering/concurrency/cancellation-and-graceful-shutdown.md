---
id: computing-software.software-engineering.concurrency.cancellation-and-graceful-shutdown
name: cancellation-and-graceful-shutdown
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, concurrency-models, task-cancellation, graceful-shutdown, cancellation-token, structured-concurrency, sigterm]
level: practitioner
status: gated
description: "Cancel concurrent work and shut down cleanly: cooperative cancellation (context, CancellationToken, interrupts), structured concurrency, SIGTERM handling and drain timeouts."
sources:
  - https://pkg.go.dev/context
  - https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads
  - https://docs.python.org/3/library/asyncio-task.html#task-groups
  - https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cancellation and shutdown of concurrent tasks

Cancellation is **cooperative** in almost every runtime: you request it, and the task must notice and stop at a safe point.

## Per-runtime mechanisms
| Runtime | Mechanism |
|---|---|
| Go | `context.Context`: `ctx, cancel := context.WithTimeout(parent, 2*time.Second); defer cancel()`; check `ctx.Done()` in loops/selects; pass ctx to every blocking call |
| .NET (not run (gated: unconfirmed, source is paywalled or blocked)) | `CancellationTokenSource` / `CancellationToken` passed to async APIs; `token.ThrowIfCancellationRequested()`; `cts.CancelAfter(...)` |
| Java (not run (gated: unconfirmed, source is paywalled or blocked)) | `Thread.interrupt()` (blocking calls throw `InterruptedException`; restore the flag with `Thread.currentThread().interrupt()` if you cannot propagate it), `Future.cancel(true)`, `ExecutorService.shutdown()` then `awaitTermination` then `shutdownNow()` |
| Python asyncio | `task.cancel()` raises `CancelledError` at the next await (run: a sibling in a `TaskGroup` saw `CancelledError` when another task raised); `asyncio.timeout()`; `TaskGroup` cancels siblings on failure |
| Kotlin (not run (gated: unconfirmed, source is paywalled or blocked)) | coroutine `Job.cancel()`, structured scopes, `isActive`/`ensureActive()`, `withTimeout` |
| JS | `AbortController`/`AbortSignal` passed to `fetch` and your own functions (run on Node 20: `abort()` fires the `abort` event with reason `AbortError`) |
| Rust async (not run (gated: unconfirmed, source is paywalled or blocked)) | dropping a future cancels it at its next `.await`; `tokio_util::sync::CancellationToken`; `tokio::select!` |

## Rules
- **Propagate** the token/context through every layer; a function that does I/O and does not accept one cannot be cancelled.
- Check for cancellation in long CPU loops (every N iterations).
- **Do not swallow cancellation:** catching `CancelledError`/`OperationCanceledException`/`InterruptedException` and continuing breaks shutdown. Clean up and re-raise.
- Clean up in `finally`/`defer`/`using`; cancellation can arrive at any await point - keep invariants valid across awaits (Rust async cancellation safety: avoid holding partial state across `.await` in `select!` branches).
- **Structured concurrency:** child tasks must not outlive their parent scope (Python `TaskGroup`, Kotlin `coroutineScope`, Java 21+ `StructuredTaskScope` preview, Go `errgroup.WithContext`, Trio nurseries). Prevents leaked goroutines/tasks.

## Graceful shutdown of a service
1. Receive SIGTERM (Kubernetes sends it, then SIGKILL after `terminationGracePeriodSeconds`, default 30 s per the pod lifecycle docs).
2. Fail readiness / stop accepting new work (deregister from load balancer). A short `preStop` sleep (5-10 s) covers endpoint propagation delay.
3. Stop consumers from fetching new messages; finish or nack in-flight ones.
4. Drain in-flight requests with a deadline (`http.Server.Shutdown(ctx)` in Go, ASP.NET `HostOptions.ShutdownTimeout`, Spring `server.shutdown=graceful` + `spring.lifecycle.timeout-per-shutdown-phase`).
5. Cancel remaining work when the deadline passes; flush logs/metrics/traces; close pools.
6. Exit with code 0.
Make sure PID 1 receives the signal: exec-form `ENTRYPOINT ["app"]` (not a shell wrapper), or use `tini`/`--init`.

## Verify
- [ ] Test: start a long request, send SIGTERM, request completes and process exits before the grace period.
- [ ] Goroutine/task leak check after cancellation (`goleak`, asyncio debug mode, thread count back to baseline).
