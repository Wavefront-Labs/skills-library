---
id: computing-software.cloud-infrastructure-engineering.azure.service-bus-queues-topics-and-dead-lettering
name: service-bus-queues-topics-and-dead-lettering
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, service-bus, queues, topics, subscriptions, sessions, dead-letter-queue, dlq, peek-lock, receive-and-delete, lock-duration, lock-renewal, max-delivery-count, duplicate-detection, scheduled-messages, deferred-messages, message-batching, prefetch, sql-filters, correlation-filters, auto-forwarding, premium-messaging-units, geo-dr, geo-replication, storage-queues, amqp, managed-identity-service-bus, idempotent-consumers]
level: practitioner
status: docs-checked
description: "Design Service Bus messaging: queues vs topics vs Storage Queues, peek-lock and lock renewal, sessions for ordering, dead-letter handling, duplicate detection, filters, Premium sizing, geo-DR."
sources: ["https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-premium-messaging", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-dead-letter-queues", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-transfers-locks-settlement", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-sessions", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/duplicate-detection", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-geo-dr", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-geo-replication", "https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-azure-and-service-bus-queues-compared-contrasted", "https://learn.microsoft.com/en-us/cli/azure/servicebus"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service Bus — queues, topics and the semantics that make consumers correct

**Goal:** producers and consumers decoupled by a broker with at-least-once delivery
you've designed for (idempotency), ordering where it's needed (sessions), poison
messages isolated (DLQ) and observed, and a tier that won't throttle at peak.

## 1. Which queue
| Need | Use |
|---|---|
| At-least-once, ordering (FIFO per session), transactions, duplicate detection, pub/sub, > 64 KB messages, long-term scheduling | **Service Bus** (Standard: shared; **Premium**: dedicated messaging units, up to 100 MB messages over AMQP, VNet/private endpoint, predictable latency) |
| Queue larger than 80 GB, simple poll-based work items, no ordering | **Storage Queues** (message up to 64 KB) |
| High-throughput event streams, replay | Event Hubs (see its skill) |
| Reactive event routing with push/filters | Event Grid |
```bash
az servicebus namespace create -g rg -n sb-orders-prod -l uksouth --sku Premium --capacity 1 --zone-redundant true --disable-local-auth true --public-network-access Disabled
az servicebus queue create -g rg --namespace-name sb-orders-prod -n orders --lock-duration PT1M --max-delivery-count 5 --enable-dead-lettering-on-message-expiration true \
  --default-message-time-to-live P7D --enable-duplicate-detection true --duplicate-detection-history-time-window PT10M --enable-session false --max-size 5120
az servicebus topic create ... -n order-events; az servicebus topic subscription create ... --topic-name order-events -n billing --max-delivery-count 10
az servicebus topic subscription rule create ... --subscription-name billing -n high-value --filter-sql-expression "amount > 1000 AND region = 'EU'"   # or --correlation-filter
```

## 2. Receive semantics
- **Peek-lock** (default): message locked for `lockDuration` (max 5 min); consumer calls `complete` / `abandon` (back to queue, delivery count +1) / `dead-letter` / `defer`. Lock expiry = redelivery → **at-least-once**; handle duplicates with an idempotency key (`MessageId`/business key in a store).
- **Receive-and-delete**: at-most-once; only for telemetry you can lose.
- Long processing: SDK auto **lock renewal** (`MaxAutoLockRenewalDuration`) — but the lock is held client-side; a crashed consumer loses it at expiry regardless.
- `maxDeliveryCount` exceeded → **dead-letter queue** (`<queue>/$DeadLetterQueue`) with `DeadLetterReason`/`DeadLetterErrorDescription`; also DLQ on TTL expiry (opt-in), filter evaluation errors, and explicit dead-lettering by the consumer (validation failure — never `abandon` a message that will fail the same way).
- **Sessions** (`--enable-session true`): `SessionId` groups messages; one consumer holds a session at a time → strict FIFO per key (order ID, device); session state (`SetState`) for small workflow state. Session-enabled queues require session receivers — a plain receiver gets an error.
- Prefetch (`PrefetchCount`, default 0 = off) for throughput; docs suggest about 20 times the receivers' processing rate when lock duration is the 60 s default. Batch sends (`SendMessagesAsync(batch)`): message up to 256 KB on Standard; on Premium up to 100 MB over AMQP (1 MB over HTTP) and 1 MB per batch.
- Scheduled (`ScheduledEnqueueTime`) for delayed delivery/retries with backoff (re-send a copy, complete the original); deferred for "park until later" by sequence number.
- Transactions: send+complete across entities in one scope (same namespace); **auto-forwarding** chains queues/subscriptions; **transfer DLQ** for forwarding failures.

## 3. Topics and filters
Topic → N subscriptions, each a virtual queue with its own DLQ/rules. Filters: **SQL** (properties, `LIKE`, `IN`, `EXISTS`), **correlation** (equality on system/user properties — much cheaper; prefer it), boolean `TrueFilter`. Actions can rewrite properties. Limits: 2,000 SQL filters per topic, 100,000 correlation filters per topic, 2,000 subscriptions per topic. Fan-out at the broker, not in code; use a subscription per consumer type, with `--max-delivery-count` and TTL tuned per consumer.

## 4. Capacity and resilience
- Standard: shared, credit-based throttling (documented limit 1,000 operations per second); Premium **messaging units** (1/2/4/8/16; autoscale available) with no fixed operations-per-second limit; watch `ThrottledRequests`, `ServerErrors`, `ActiveMessages`, `DeadletteredMessages`, `ScheduledMessages`, `NamespaceCpuUsage`/`NamespaceMemoryUsage` (Premium; the older `CPUXNS`/`WSXNS` are deprecated), `IncomingMessages/OutgoingMessages`.
- **Geo-DR** (Premium; metadata pairing + alias namespace name; messages *not* replicated; failover repoints the alias and breaks the pairing) vs **geo-replication** (Premium; metadata and data replicated to a secondary region, customer-promoted; synchronous mode gives RPO 0, asynchronous mode allows data loss within the configured lag). The docs recommend geo-replication for most DR scenarios.
- Partitioned entities spread across brokers (Standard: up to 100 partitioned entities per namespace; Premium namespaces can be created with 1, 2 or 4 partitions).
- Client: use the SDK's processor (`ServiceBusProcessor`/`@azure/service-bus` subscribe) with `MaxConcurrentCalls`, AMQP over 5671 (or AMQP-over-WebSockets 443), retry policy exponential; `ServiceBusTrigger` in Functions/KEDA `azure-servicebus` scaler in Container Apps for autoscaled consumers.

## 5. Security and ops
- Entra roles: *Azure Service Bus Data Sender/Receiver/Owner* on namespace/entity scope (names as in the Azure built-in roles list); `--disable-local-auth true` kills SAS; private endpoint `privatelink.servicebus.windows.net`; CMK (Premium) via Key Vault.
- Diagnostics: `OperationalLogs`, `RuntimeAuditLogs` (who sent/received, with identity — Premium), `VNetAndIPFilteringLogs`; alert on `DeadletteredMessages > 0` per entity and on `ActiveMessages` growing (consumer stall) — plus Service Bus Explorer in the portal to peek/resubmit DLQ messages.
- DLQ handling pattern: a dedicated process reads the DLQ, logs reason + payload to a case store, and resubmits after fix (new message, `complete` the DLQ one). DLQ messages don't expire; they count toward the entity size — an ignored DLQ fills the queue.

## Gotchas
- `lockDuration` shorter than processing time + auto-renew off = silent duplicate processing; every "we got the webhook twice" story.
- Duplicate detection keys on **`MessageId`** only within the configured window; producers must set it deterministically (not a new GUID per retry).
- Sessions: a consumer with `MaxConcurrentSessions` higher than the number of partitions/throughput you need starves others; sessions with no `SessionId` on send fail with a clear error, but a *topic subscription* with sessions on and senders unaware is a classic.
- Message size includes properties (system and user) and payload; a 255 KB body plus properties can exceed 256 KB on Standard.
- Standard-tier throttling returns server busy errors: retry with exponential backoff, not a tight loop; Premium throttles at resource saturation.
- Geo-DR alias failover is a one-time move that breaks the pairing; messages are not replicated, so unprocessed messages in the old primary are not in the secondary. Role assignments, private endpoints and network settings are not replicated either.
- Entity names with `/` create hierarchy in the portal only; auto-forwarding to a topic subscription needs the full `topic/Subscriptions/name` path.

## Verify
- [ ] `az servicebus namespace show --query "{sku:sku.name,zr:zoneRedundant,local:disableLocalAuth,pna:publicNetworkAccess}"` matches; consumers authenticate with managed identity (`RuntimeAuditLogs` shows the identity).
- [ ] Chaos: kill a consumer mid-message → the message is redelivered once and the handler's idempotency check skips the duplicate (log shows "already processed").
- [ ] Poison test: a malformed message lands in the DLQ after `maxDeliveryCount` with a reason; the DLQ alert fires; resubmission path works.
- [ ] Load test at 2× expected rate: `ThrottledRequests` = 0, `ActiveMessages` returns to ~0 within the SLO; session-ordered queue delivers in sequence per key.

## Checked
Checked 2026-10-24 against azure-docs Service Bus pages (quotas and limits includes, premium messaging, dead-letter queues, message transfers and settlement, duplicate detection, geo-DR, geo-replication, Storage queues compared) and the azure-docs-cli servicebus reference. Confirmed: lock duration maximum 5 minutes; default max delivery count 10; TTL expiry goes to the DLQ only when dead-lettering on expiration is enabled; message and batch size limits; 1, 2, 4, 8, 16 messaging units; filter and subscription limits; geo-DR (metadata only, alias, failover breaks pairing) versus geo-replication (data replicated, sync or async); all az servicebus flags used in the examples exist. Found wrong or stale and fixed: rules limit stated as per subscription (it is per topic: 2,000 SQL, 100,000 correlation); CPUXNS/WSXNS metrics (deprecated); Premium described as non-partitioned (partitioned Premium namespaces exist); unconfirmed throughput figure and default zone redundancy removed.

Method: documentation only; no commands were run.
