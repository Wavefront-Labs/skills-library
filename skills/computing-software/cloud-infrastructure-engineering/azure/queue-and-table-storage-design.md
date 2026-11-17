---
id: computing-software.cloud-infrastructure-engineering.azure.queue-and-table-storage-design
name: queue-and-table-storage-design
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, storage-queues-design, azure-table-storage, queue-storage, poison-queue, partitionkey, rowkey]
level: practitioner
status: docs-checked
description: "Design with Azure Queue and Table storage: message limits, visibility timeout, poison handling, PartitionKey/RowKey design, scale targets, and when to step up."
sources: ["https://learn.microsoft.com/azure/storage/queues/storage-queues-introduction", "https://learn.microsoft.com/azure/storage/queues/scalability-targets", "https://learn.microsoft.com/azure/storage/tables/scalability-targets", "https://learn.microsoft.com/azure/storage/tables/table-storage-design-guidelines", "https://learn.microsoft.com/azure/azure-functions/functions-bindings-storage-queue-trigger"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue and Table storage design

**Goal:** use the cheap, simple storage services correctly - and know when to step up.

## Queue storage
- Message up to **64 KB** (store larger payloads in a blob, enqueue the pointer). TTL default 7 days; `-1` = never expires (service version 2017-07-29 or later).
- Delete each message once it has been processed successfully; make handlers idempotent.
- Poison handling: when a queue-triggered Azure Function fails, the runtime retries up to five times (including the first try), then adds the message to `<originalqueuename>-poison`; to handle poison messages yourself, check the message's dequeue count.
- Targets: up to 2,000 messages/s for a single queue (1-KiB messages), 20,000 messages/s per storage account - shard across queues beyond that.
```bash
az storage queue create --account-name st --name orders --auth-mode login
az storage message put --account-name st --queue-name orders --content '{"id":42}' --time-to-live 86400 --auth-mode login
```
Choose **Service Bus** when Queue storage's feature set is not enough (check the Service Bus documentation for FIFO, sessions, duplicate detection and topics).

## Table storage
- Entity max 1 MiB, up to 255 properties including the three system properties (PartitionKey, RowKey, Timestamp); key = **PartitionKey + RowKey**.
- Specify both PartitionKey and RowKey where you can: point queries are the most efficient table query.
- Partition = unit of scale: up to 2,000 entities/s per partition (1-KiB entities), 20,000 transactions/s per account. Avoid hot partitions
  (e.g. date-only PK); prefix with a hash or tenant ID.
- Entity group transaction: at most 100 entities and under 4 MiB payload, and an entity can be updated only once in it.
- Patterns: compound key values (`tenant|orderId`) give alternate keyed access paths.

## Gotchas
- Use Entra auth (`--auth-mode login`) for the CLI commands above.
- A table query can return no results yet still return a continuation header - always follow continuation tokens until none remain.

## Verify
- [ ] Load test stays within the per-queue and per-partition targets at peak; poison queue monitored with an alert.

## Checked
2026-10-28. Confirmed on the Queue and Table scalability-target pages, Queue Storage introduction, queue-trigger binding page and Query Timeout and Pagination page: 64 KB message, 7-day default TTL and -1, 2,000 messages/s per queue and 20,000/s per account, 1 MiB entity, 255 properties (3 system), 2,000 entities/s per partition, 100-entity group transaction, five Functions retries then `-poison` queue, continuation headers. Removed: `maxDequeueCount`, 1,000-entity page size, ordering/dedup statements, inverted-ticks pattern, Cosmos DB for Table claims, Service Bus feature list, 503 ServerBusy wording. CLI flags checked with check_commands.
Method: documentation only; no commands were run.
