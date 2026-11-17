---
id: computing-software.cloud-infrastructure-engineering.azure.event-hubs-streaming-kafka-and-capture
name: event-hubs-streaming-kafka-and-capture
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, event-hubs, event-streaming, kafka, kafka-endpoint, capture, consumer-groups, partitions, partition-key, throughput-units, processing-units, auto-inflate, event-processor-client, checkpointing, blob-checkpoint-store, retention, schema-registry, avro, dedicated-cluster, premium-tier, geo-replication, event-hubs-namespace, managed-identity-event-hubs, backpressure, stream-processing]
level: practitioner
status: docs-checked
description: "Run Event Hubs as a streaming backbone: partition and consumer-group design, TUs vs PUs with auto-inflate, EventProcessorClient checkpointing, Kafka endpoint, Capture to ADLS, Schema Registry."
sources: ["https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-quotas", "https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-scalability", "https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-premium-overview", "https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-features", "https://learn.microsoft.com/en-us/azure/event-hubs/azure-event-hubs-apache-kafka-overview", "https://learn.microsoft.com/en-us/azure/event-hubs/apache-kafka-transactions", "https://learn.microsoft.com/en-us/azure/event-hubs/log-compaction", "https://learn.microsoft.com/en-us/azure/event-hubs/schema-registry-overview", "https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-overview", "https://learn.microsoft.com/en-us/azure/event-hubs/monitor-event-hubs-reference", "https://learn.microsoft.com/en-us/cli/azure/eventhubs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event Hubs — a partitioned log for telemetry and events, with Kafka compatibility

**Goal:** millions of events per second ingested into a hub whose partition count
matches consumer parallelism, consumers that checkpoint and rebalance safely, raw
events archived to the lake automatically, and producers that didn't have to change.

## 1. Model and sizing
- Namespace (tier + capacity) → **event hubs** (topics) → **partitions** (ordered, append-only, 1–32 Standard / up to 100 Premium / 1 024 Dedicated) → **consumer groups** (independent cursors; every hub has `$Default`; limits per event hub: 20 Standard, 100 Premium, 1,000 Dedicated).
- Ordering is per partition; choose a **partition key** (device/tenant/order ID) for order per entity, or none for round-robin maximum spread. Partition count is **fixed after creation** on Standard (dynamic partition scale-out is a Premium and Dedicated feature) — size for the future: partitions ≥ max parallel consumers you'll ever want.
- Capacity: **Throughput units** (Standard: 1 TU = 1 MB/s or 1 000 events/s in, 2 MB/s out; 1–40 with **auto-inflate**), **Processing units** (Premium: 1, 2, 4, 6, 8, 10, 12 or 16 PU; about 5-10 MB/s ingress and 10-20 MB/s egress per PU as an approximate figure; 90-day retention; resource isolation), **Capacity units** (Dedicated cluster: single tenant, up to 1,000 event hubs per namespace).
```bash
az eventhubs namespace create -g rg -n evh-telemetry-prod -l uksouth --sku Premium --capacity 1 --zone-redundant true --disable-local-auth true --public-network-access Disabled
az eventhubs eventhub create -g rg --namespace-name evh-telemetry-prod -n device-events --partition-count 32 --retention-time-in-hours 168 --cleanup-policy Delete
az eventhubs eventhub consumer-group create ... --eventhub-name device-events -n analytics ; ... -n archive-check
az eventhubs eventhub update ... -n device-events --enable-capture true --capture-interval 300 --capture-size-limit 314572800 --destination-name EventHubArchive.AzureBlockBlob \
  --storage-account <st-id> --blob-container raw-events --archive-name-format "{Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}" --skip-empty-archives true
```
- Retention: default 1 hour; maximum 7 days Standard, 90 days Premium/Dedicated; **compacted** hubs (`--cleanup-policy Compact`) keep the latest event per key (Kafka log compaction); compaction is not available on Basic and compacted size is limited per partition (1 GB Standard, 250 GB Premium/Dedicated).

## 2. Producers
- SDK `EventHubProducerClient` with batches (`CreateBatchAsync`; maximum publication size is 1 MB on Standard and Premium, 256 KB Basic, 20 MB Dedicated), partition key or explicit partition ID (avoid).
- **Kafka endpoint**: `bootstrap.servers=evh-telemetry-prod.servicebus.windows.net:9093`, `security.protocol=SASL_SSL`, `sasl.mechanism=OAUTHBEARER` (Entra) or `PLAIN` with `$ConnectionString` (if local auth allowed); Event Hubs supports Apache Kafka 1.0 and later (Standard, Premium and Dedicated tiers) and idempotent producers; Kafka transactions are in public preview on Premium and Dedicated.
- Throttling: alert on `ThrottledRequests` (and `QuotaExceededErrors`); turn on auto-inflate (Standard) or add PUs.
- Schema: **Schema Registry** in the namespace (Avro, JSON Schema, Protobuf) → events carry a schema ID instead of the schema; the registry stores schema groups and versions (limits per tier: for example 25 MB and 25 versions on Standard).

## 3. Consumers
- **EventProcessorClient** (for example the .NET `EventProcessorClient` or `EventHubConsumerClient` with a blob checkpoint store): one client per consumer group across N instances → partitions balanced automatically (lease per partition in a blob container); **checkpoint** by storing the offset/sequence number after processing a batch — not every event (storage calls), not never (replay storms on restart). At-least-once: make handlers idempotent by `(partitionId, sequenceNumber)` or event ID.
- Scale = partitions: 32 partitions → at most 32 active consumers in a group; more instances sit idle. Azure Functions Event Hubs triggers checkpoint per batch.
- Start position per consumer group: earliest/latest/by time or offset; **lag** = latest sequence number in the partition − checkpointed sequence number; expose it as a metric and alert on growth.
- Stream processors: Stream Analytics, Databricks/Spark Structured Streaming (`kafka` source), Flink, Fabric Eventstreams — all consume via Kafka or AMQP.

## 4. Capture and lake
Capture writes Avro (Parquet is available through the Stream Analytics no-code editor) per partition every N seconds/MB (60-900 s, 10-500 MB, first wins) to Blob/ADLS Gen2 — your replayable raw archive and the input for batch ETL (ADF/Synapse read the folder structure). Capture bypasses the TU/PU/CU egress quotas; use a managed identity for the storage destination (`--mi-system-assigned`).

## 5. Security and ops
- Entra: *Azure Event Hubs Data Sender/Receiver/Owner* at namespace/hub scope; `--disable-local-auth true`; private endpoint with the `privatelink.servicebus.windows.net` private DNS zone; CMK (Premium/Dedicated); IP firewall rules (Standard and above).
- Metrics: `IncomingMessages`, `OutgoingMessages`, `IncomingBytes`, `ThrottledRequests`, `ServerErrors`, `CaptureBacklog`, `CapturedMessages`, `QuotaExceededErrors`, `ActiveConnections`, `Size` (retained bytes); Premium `NamespaceCpuUsage`/`NamespaceMemoryUsage`; resource-specific log tables AZMSArchiveLogs, AZMSOperationalLogs, AZMSKafkaCoordinatorLogs, AZMSKafkaUserErrorLogs, AZMSRunTimeAuditLogs (runtime audit logs are Premium and Dedicated only).
- **Geo-replication** (Premium/Dedicated, data replicated to a secondary region, promote on failure) vs **Geo-DR** (metadata alias only; Standard and above). Availability zones are supported in all tiers.

## Gotchas
- Partition count on Standard is forever; 4 partitions "to start" caps a consumer group at 4 active readers (the Standard maximum is 32 partitions), so size for expected parallelism.
- Checkpointing every event adds a storage call per event and slows consumers; checkpoint per batch or every N seconds.
- Consumer group `$Default` shared by two apps = they steal partitions from each other; one consumer group per application.
- Kafka transactions are in public preview on Premium and Dedicated only; do not rely on them on Standard.
- Capture produces one file per partition per interval: 32 partitions × 5 min = 9 216 files/day; downstream readers must handle small files (compact nightly) or set a larger interval.
- Event storage is limited per unit (84 GB per TU on Basic and Standard, 1 TB per PU on Premium, 10 TB per CU on Dedicated); retention beyond what the storage allows is not guaranteed.

## Verify
- [ ] `az eventhubs namespace show --query "{sku:sku.name,cap:sku.capacity,zr:zoneRedundant,local:disableLocalAuth,pna:publicNetworkAccess}"`; hub partition count as designed; consumer groups one per app.
- [ ] Load test at target rate: `ThrottledRequests` 0; consumer lag per partition stays below the SLO; killing one consumer instance rebalances its partitions to the others with no gaps (sequence-number continuity check).
- [ ] Restart all consumers: processing resumes from the last checkpoint with bounded replay (duplicates handled idempotently).
- [ ] Capture: Avro files appear in `raw-events/<ns>/<hub>/<partition>/...` within the interval; `CaptureBacklog` ≈ 0; a Kafka producer with OAUTHBEARER publishes successfully and `KafkaUserErrorLogs` is empty.

## Checked
Checked 2026-10-24 against azure-docs Event Hubs pages (tier limits, tier features and common limits includes, scalability, premium overview, features, Apache Kafka overview, Kafka transactions, log compaction, schema registry overview, capture overview, monitoring reference) and the azure-docs-cli eventhubs reference. Confirmed: partitions 32/100/1,024 per event hub; consumer groups 20/100/1,000; publication size 256 KB/1 MB/1 MB/20 MB; retention 7 and 90 days; 84 GB per TU, 1 TB per PU, 10 TB per CU; PU choices 1, 2, 4, 6, 8, 10, 12, 16; 40 TU maximum; Kafka 1.0+, port 9093, SASL_SSL with OAUTHBEARER or PLAIN; metric names; log tables. Found wrong and fixed: PU range (not a continuous 1-16), consumer-group limit counting, idempotent producers (supported; only transactions are preview on Premium and Dedicated), capture counted against egress (it bypasses egress quotas), Premium partitions can only be added dynamically. Removed unconfirmed: per-partition throughput figure, storage request limit, 30 s rebalance, KEDA and Functions setting names, Dedicated sizing threshold, cleanup-policy immutability.

Method: documentation only; no commands were run.
