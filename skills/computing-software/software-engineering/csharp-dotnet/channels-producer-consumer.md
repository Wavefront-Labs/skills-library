---
id: computing-software.software-engineering.csharp-dotnet.channels-producer-consumer
name: channels-producer-consumer
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, async-await, system-threading-channels, producer-consumer, bounded-channel, backpressure, backgroundservice, work-queue]
level: advanced
status: docs-checked
description: "Build in-process async work queues with System.Threading.Channels: bounded vs unbounded, full modes, multiple consumers, completion and BackgroundService integration."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/extensions/channels
  - https://learn.microsoft.com/en-us/dotnet/api/system.threading.channels.boundedchannelfullmode
  - https://learn.microsoft.com/en-us/dotnet/core/extensions/queue-service
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Channels for async producer-consumer

**Goal:** hand work from request handlers (producers) to background workers
(consumers) inside one process, with backpressure and clean shutdown.

## Create
```csharp
var channel = Channel.CreateBounded<Job>(new BoundedChannelOptions(capacity: 1_000)
{
    FullMode = BoundedChannelFullMode.Wait,   // producers await when full (backpressure)
    SingleReader = false,
    SingleWriter = false,
});
```
| FullMode | Behaviour when full |
|---|---|
| `Wait` | `WriteAsync` waits for space (backpressure) |
| `DropOldest` | removes and ignores the oldest item to make room |
| `DropNewest` | removes and ignores the newest item in the channel to make room |
| `DropWrite` | drops the item being written |
Unbounded channels have no capacity limit, so a slow consumer means growing memory. Prefer bounded channels when producers can outrun consumers.

## Produce and consume
```csharp
await channel.Writer.WriteAsync(job, ct);

await foreach (var job in channel.Reader.ReadAllAsync(ct))
{
    try { await HandleAsync(job, ct); }
    catch (Exception ex) { logger.LogError(ex, "job {Id} failed", job.Id); }   // one bad job must not kill the loop
}
```
Multiple consumers: start N tasks each running that loop on the same reader; each item
is read by one consumer.

## Completion
`channel.Writer.Complete()` signals no more items; `ReadAllAsync` finishes after draining.
`Complete(exception)` propagates a failure to readers. A channel used after it has been closed throws
`ChannelClosedException`; use `TryComplete` if several paths may close it.

## Hosting in ASP.NET Core
Register the channel (or a wrapper `IBackgroundQueue`) as a singleton, inject it into
controllers, and consume in a `BackgroundService`:
```csharp
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
    var workers = Enumerable.Range(0, 4).Select(_ => ConsumeAsync(stoppingToken));
    await Task.WhenAll(workers);
}
```
Remember scoped dependencies (DbContext): create a scope per job with
`IServiceScopeFactory`.

## Limits
- In-memory: items are lost on crash or deploy. For durable work use a real queue
  (Service Bus, RabbitMQ, SQS) or an outbox table.
- Graceful shutdown: `HostOptions.ShutdownTimeout` bounds how long
  draining can take.

## Verify
- [ ] Load test with slow consumers: memory stays bounded and producers slow down.
- [ ] Shutdown drains or deliberately abandons in-flight items, with logs saying which.

## Checked

Checked 2026-10-25 against dotnet/docs (core/extensions/channels) and dotnet/runtime `HostOptions.cs` on main.
Confirmed: `BoundedChannelFullMode` members and their semantics (`Wait`, `DropOldest`, `DropNewest`, `DropWrite`); `TryComplete`; `ReadAllAsync`; `ChannelClosedException` on use after close; `SingleReader`/`SingleWriter` options.
Removed as unconfirmed: the `TryWrite` return detail, the "silent drop" wording, and the numeric shutdown default (see the health checks skill for `ShutdownTimeout`).

Method: documentation only; no commands were run.
