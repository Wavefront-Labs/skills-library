---
id: computing-software.cloud-infrastructure-engineering.azure.cosmos-db-partitioning-throughput-and-consistency
name: cosmos-db-partitioning-throughput-and-consistency
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, cosmos-db, cosmosdb, nosql-api, partition-key, hierarchical-partition-keys, request-units, ru, provisioned-throughput, autoscale, serverless, consistency-levels, session-consistency, bounded-staleness, multi-region-writes, automatic-failover, change-feed, ttl, indexing-policy, hot-partition, 429-throttling, continuous-backup, point-in-time-restore, analytical-store, synapse-link, cosmos-rbac]
level: advanced
status: docs-checked
description: "Design Cosmos DB that scales without 429s: partition and hierarchical keys, RU budgeting with autoscale/serverless, consistency levels, failover and RBAC."
sources: ["https://learn.microsoft.com/azure/cosmos-db/partitioning", "https://learn.microsoft.com/azure/cosmos-db/consistency-levels", "https://learn.microsoft.com/azure/cosmos-db/concepts-limits", "https://github.com/Azure/azure-cli/tree/dev/src/azure-cli/azure/cli/command_modules/cosmosdb"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cosmos DB - partitioning, RUs and consistency decided before the first write

**Goal:** a container whose partition key spreads writes and answers the top queries
in one partition, throughput sized from measured RU/op, and a consistency level chosen for
the app's semantics.

## 1. Partition key (the hard-to-change decision)
- A partition key can't be changed in place: moving to a different key means copying data to a new container (container copy jobs), or using global secondary indexes for other query patterns (NoSQL API).
- Pick a property with a wide range of values (high cardinality) whose value doesn't change, that spreads request units and storage evenly, and that your main queries filter on. Partition key values are immutable.
- Each logical partition can store up to **20 GB** and is limited to **10,000 RU/s** (a physical partition provides up to 10,000 RU/s and 50 GB).
- Low-cardinality keys (`status`, `type`, `country`) create few logical partitions and risk hot partitions. A high-cardinality key that queries never filter on makes most reads cross-partition. `/id` gives excellent distribution and cheap point reads but no query locality.
- **Hierarchical partition keys** allow up to three levels, so a first-level key can exceed 20 GB while queries on the leading levels stay targeted.
- Reads by `id` plus partition key are point reads; a cross-partition query adds roughly 2-3 RU per physical partition checked.
- Maximum item size is 2 MB; partition key values are limited to 2,048 bytes (101 bytes without large partition keys).
```bash
az cosmosdb create -g rg -n cos-orders-prod --kind GlobalDocumentDB \
  --locations regionName=uksouth failoverPriority=0 isZoneRedundant=true \
  --locations regionName=ukwest failoverPriority=1 \
  --default-consistency-level Session --enable-automatic-failover true \
  --backup-policy-type Continuous --public-network-access Disabled
az cosmosdb sql database create -a cos-orders-prod -g rg -n orders
az cosmosdb sql container create -a cos-orders-prod -g rg -d orders -n orders \
  --partition-key-path /tenantId --max-throughput 10000 --ttl -1 --idx @indexing-policy.json
```
Hierarchical partition keys are defined when the container is created through the portal, SDKs or templates; the CLI container command takes a single `--partition-key-path`.

## 2. Throughput
- Provisioned throughput is divided evenly among physical partitions, so one hot key can be rate limited while the container as a whole is under-used.
- **Manual** throughput: minimum 400 RU/s per container. **Autoscale**: you set a maximum RU/s (minimum maximum 1,000); the system scales between 10 % and 100 % of it and bills per hour on the highest RU/s reached or 10 % of the maximum, whichever is higher. **Serverless** is consumption based and limited to a single region.
- A database with shared throughput can hold at most 25 containers at the base minimum; more containers raise the minimum.
- Limits: maximum 1,000,000 RU/s per container by default (raise via support ticket); the request-unit charge is returned with every response, so measure RU per operation in load tests.
- Request rate too large errors (HTTP 429) are returned when you exceed provisioned throughput; use the Insights and metrics for normalized RU consumption per partition key range to find hot partitions.

## 3. Consistency
| Level | Behaviour | Read cost |
|---|---|---|
| Strong | linearizable reads | reads use two replicas: half the read throughput per RU |
| Bounded staleness | lag bounded by K versions or T time | same as Strong |
| **Session** | read-your-writes within a session token | single replica |
| Consistent prefix | ordered, possibly stale | single replica |
| Eventual | no ordering guarantee | single replica |
- The account default applies to all reads and queries; a request can override it (an override affects SDK client reads only). Recreate the SDK client after changing the default.
- Strong consistency is not available on accounts with multiple write regions, and strong consistency across regions more than 5,000 miles (8,000 km) apart is blocked by default.
- Session tokens are partition-bound; share the latest token between clients if a chain of requests must read its own writes.
- For a single-region account, minimum bounded staleness is 10 write operations or 5 seconds; for multi-region accounts 100,000 operations or 300 seconds.

## 4. Multi-region and failover
- Multiple write regions suit apps that tolerate conflicts; single write region with service-managed (automatic) failover is the simpler default. Production workloads should enable service-managed failover.
- `az cosmosdb failover-priority-change` changes the failover priorities; zone redundancy is set per region (`isZoneRedundant=true`).
- Configure the SDK with preferred regions so reads go to the nearest region.

## 5. Security
- Data-plane RBAC with managed identities: `az cosmosdb sql role assignment create --role-definition-name <name> --principal-id <object-id> --scope /` (see the Cosmos DB RBAC documentation for built-in role names). Key-based authentication can be disabled on the account (`--disable-local-auth`).

## Gotchas
- Autoscale never goes below 10 % of its maximum, so a large maximum bills a large minimum even when idle.
- Cross-partition aggregates over large containers cost RUs on every partition.
- `id` is unique per partition key value, not globally, unless `/id` is the partition key.

## Verify
- [ ] Load test: normalized RU consumption per partition key range is balanced and 429s are rare.
- [ ] Top queries measured for RU per operation and checked for cross-partition fan-out.
- [ ] `az cosmosdb show` reflects the intended default consistency, automatic failover and backup policy.

## Checked

2026-10-24, against the Azure Cosmos DB articles on partitioning (updated 2026-10-05), consistency levels, and service quotas (2026-08-25), plus the Azure CLI source for the cosmosdb module (azure-cli dev branch): 20 GB logical partition, 10,000 RU/s and 50 GB physical partition, three-level hierarchical keys, 2-3 RU per extra physical partition on cross-partition queries, 2 MB item and 2,048-byte key limits, manual minimum 400 RU/s, autoscale minimum maximum 1,000 and 10 percent floor, 25-container shared-database threshold, 1,000,000 RU/s default container maximum, serverless single region, consistency read-cost and bounded-staleness minimums, strong consistency restrictions, CLI parameters (`--locations` keys regionName, failoverPriority, isZoneRedundant; `--enable-automatic-failover`, `--backup-policy-type`, `--public-network-access`, `--partition-key-path`, `--max-throughput`, `--ttl`, `--idx`, `az cosmosdb failover-priority-change`, `az cosmosdb sql role assignment create`, `--disable-local-auth`). Removed unconfirmed write-RU costs, serverless burst figure, retry counts, burst-capacity minutes, change feed, TTL billing and continuous-backup tier details, indexing recommendations and the Synapse Link, private endpoint and diagnostic-log remarks.

Method: documentation only; no commands were run.
