---
id: computing-software.software-engineering.csharp-dotnet.masstransit-and-azure-service-bus
name: masstransit-and-azure-service-bus
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-messaging-jobs, masstransit, azure-service-bus, consumers, dead-letter, saga]
level: advanced
status: draft
description: "Consume and publish messages in .NET with MassTransit and Azure.Messaging.ServiceBus: consumers, retries, dead-letter queues, sessions, outbox integration, and licensing change in MassTransit 9."
sources: ["https://masstransit.io/documentation/concepts", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-dotnet-get-started-with-queues", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-dead-letter-queues"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MassTransit and Azure Service Bus

## Raw SDK (Azure.Messaging.ServiceBus)
```csharp
await using var client = new ServiceBusClient(fullyQualifiedNamespace, new DefaultAzureCredential());   // managed identity, no connection string
var sender = client.CreateSender("orders");
await sender.SendMessageAsync(new ServiceBusMessage(BinaryData.FromObjectAsJson(evt)) { MessageId = evt.Id.ToString(), SessionId = evt.CustomerId });

await using var proc = client.CreateProcessor("orders", new ServiceBusProcessorOptions { MaxConcurrentCalls = 8, AutoCompleteMessages = false, MaxAutoLockRenewalDuration = TimeSpan.FromMinutes(10) });
proc.ProcessMessageAsync += async a => { await Handle(a.Message); await a.CompleteMessageAsync(a.Message); };   // exception => abandon => redelivery
proc.ProcessErrorAsync += a => { log.LogError(a.Exception, "sb error"); return Task.CompletedTask; };
await proc.StartProcessingAsync();
```
- Delivery is **at least once**; set `MessageId` and enable duplicate detection on the entity (time window) plus idempotent handlers.
- After `MaxDeliveryCount` (default 10) messages go to the dead-letter subqueue `$DeadLetterQueue`; monitor it, replay deliberately. Use `DeadLetterMessageAsync` for poison messages.
- Sessions give per-key ordered processing. Prefer topics+subscriptions for pub/sub with SQL/correlation filters.
- Lock duration (default 30 s-5 min) must exceed handling time, or renew.

## MassTransit
```csharp
builder.Services.AddMassTransit(x => {
    x.AddConsumer<SubmitOrderConsumer>();
    x.AddEntityFrameworkOutbox<AppDb>(o => { o.UseSqlServer(); o.UseBusOutbox(); });         // transactional outbox + inbox dedupe
    x.UsingAzureServiceBus((ctx, cfg) => {
        cfg.Host(new Uri("sb://acme.servicebus.windows.net"), h => h.TokenCredential = new DefaultAzureCredential());
        cfg.UseMessageRetry(r => r.Exponential(5, TimeSpan.FromSeconds(1), TimeSpan.FromMinutes(1), TimeSpan.FromSeconds(2)));
        cfg.ConfigureEndpoints(ctx);
    });
});
public class SubmitOrderConsumer : IConsumer<SubmitOrder> { public async Task Consume(ConsumeContext<SubmitOrder> c) { await c.Publish(new OrderSubmitted(c.Message.Id)); } }
```
Also: Request/response clients, sagas (state machines) with EF/Redis persistence, scheduling, RabbitMQ/SQS/in-memory transports (in-memory for tests with the test harness `AddMassTransitTestHarness`).
**Licensing:** MassTransit v8 is open source (Apache 2.0); v9 moves to a commercial licence, so pin v8 or budget accordingly. Alternatives: Wolverine, NServiceBus (commercial), Rebus.

## Gotchas
- Message contracts are public APIs: add fields compatibly; use records in a shared contracts package.
- Poison loops from unhandled exceptions: cap retries and dead-letter.
- Don't consume and publish in different DB transactions without outbox.

## Verify
Harness test asserts `consumer.Consumed.Any<SubmitOrder>()` and published `OrderSubmitted`; send a malformed message and confirm it lands in the DLQ after retries.
