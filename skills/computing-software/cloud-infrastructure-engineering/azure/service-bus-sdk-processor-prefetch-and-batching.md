---
id: computing-software.cloud-infrastructure-engineering.azure.service-bus-sdk-processor-prefetch-and-batching
name: service-bus-sdk-processor-prefetch-and-batching
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, service-bus, servicebusprocessor, prefetch-count, batch-send, lock-renewal, sessions]
level: advanced
status: docs-checked
description: "Use the Azure Service Bus SDK well: ServiceBusProcessor concurrency, prefetch, lock renewal, session processing, batch sends and safe settlement."
sources: ["https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-performance-improvements", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-prefetch", "https://learn.microsoft.com/en-us/dotnet/api/azure.messaging.servicebus.servicebusprocessor", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-sessions", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service Bus SDK patterns

**Goal:** high throughput consumers and producers that do not lose or duplicate work unexpectedly.

## Clients
- One `ServiceBusClient` per namespace per process (singleton); senders/receivers are cheap and cached.
- Auth with `DefaultAzureCredential` and data roles (`Azure Service Bus Data Sender/Receiver`).

## Processor (.NET)
```csharp
var processor = client.CreateProcessor("orders", new ServiceBusProcessorOptions {
    MaxConcurrentCalls = 16,
    PrefetchCount = 0,                                   // raise only after measuring
    AutoCompleteMessages = false,
    MaxAutoLockRenewalDuration = TimeSpan.FromMinutes(10),   // SDK default is 5 minutes
    ReceiveMode = ServiceBusReceiveMode.PeekLock });
processor.ProcessMessageAsync += async a => { await Handle(a.Message); await a.CompleteMessageAsync(a.Message); };
processor.ProcessErrorAsync += e => { log.LogError(e.Exception, "{Source}", e.ErrorSource); return Task.CompletedTask; };
await processor.StartProcessingAsync();
```
- **Settlement**: Complete on success, Abandon to retry, DeadLetter with reason for poison messages; `MaxDeliveryCount` (default 10) moves repeated failures to DLQ.
- **Lock duration** on the entity (default 60 s, max 5 min) plus `MaxAutoLockRenewalDuration` for long handlers.
- **Sessions** (FIFO per key): `CreateSessionProcessor` with `MaxConcurrentSessions` and `SessionIdleTimeout`.

## Prefetch
- Prefetch pulls messages into a local buffer, locking them. Good for many small, fast messages.
- Rule of thumb from the performance guide: with the default 60 s lock, prefetch about 20 times the maximum processing rate of the receivers; with multiple clients on one entity, use 0. Too high causes lock expiry before processing (messages redelivered, delivery count inflates).
- Prefetched messages are lost from the local buffer if the client crashes (they return after lock expiry in PeekLock).

## Sending
```csharp
await using var sender = client.CreateSender("orders");
using ServiceBusMessageBatch batch = await sender.CreateMessageBatchAsync();
foreach (var o in orders) if (!batch.TryAddMessage(new ServiceBusMessage(JsonSerializer.SerializeToUtf8Bytes(o)) { MessageId = o.Id })) { await sender.SendMessagesAsync(batch); /* start new batch */ }
await sender.SendMessagesAsync(batch);
```
Set `MessageId` and enable **duplicate detection** on the entity for idempotent producers. A batch is limited to 256 KB on Standard and 1 MB on Premium; a single message can be up to 100 MB on Premium over AMQP.

## Verify
- [ ] Metrics: Active messages trend down, Dead-lettered messages near zero, no `MessageLockLost` exceptions in logs.

## Checked
Checked 2026-10-24 against azure-docs (service-bus-performance-improvements, service-bus-prefetch, service-bus-quotas limits include, message-transfers-locks-settlement, dead-letter-queues) and the Azure.Messaging.ServiceBus source (ServiceBusProcessorOptions, ServiceBusSessionProcessorOptions). Confirmed: option names ReceiveMode (default PeekLock), AutoCompleteMessages (default true), PrefetchCount (default 0), MaxAutoLockRenewalDuration (default 5 minutes), MaxConcurrentCalls (default 1), MaxConcurrentSessions, SessionIdleTimeout; lock duration maximum 5 minutes; default max delivery count 10; the 20x prefetch guidance. Fixed: batch size limit was stated as the maximum message size (Premium batches are limited to 1 MB).  The performance guide states a 60 s default lock expiration.

Method: documentation only; no commands were run.
