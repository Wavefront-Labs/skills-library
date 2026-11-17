---
id: computing-software.data-engineering.druid.druid-multitenancy-datasource-design
name: druid-multitenancy-datasource-design
category: computing-software
field: data-engineering
product: druid
tags: [multitenancy, tenant-id, datasource-per-tenant, shared-datasource, partitioning]
level: practitioner
status: docs-checked
description: "Decide between a datasource per tenant and shared datasources."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/multitenancy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Multitenant workloads can use one datasource per tenant, or share datasources with a `tenant_id` dimension.

Datasource per tenant: each can have its own schema, backfills, partitioning rules, loading and expiration rules; queries can be faster because fewer segments are examined; and it is the most flexible.

Shared datasources: each datasource needs its own JVMs for real-time indexing and its own segment files on disk, so a very large number of small datasources is wasteful.

A compromise is several datasources, fewer than tenants. For example, tenants with partitioning rules A go to one datasource and tenants with rules B to another.

With shared datasources most queries filter on `tenant_id`, which performs best when data is well partitioned by tenant. In batch indexing use multi-dimension range partitioning on tenant_id: Druid always partitions by time first, with the secondary partition on tenant_id. In realtime indexing partition the stream itself, for example by having a Kafka producer partition the topic by a hash of tenant_id.

Data distribution: Historicals can be grouped into tiers and rules decide which segments go to which tier, for example recent, frequently queried segments on more powerful hardware, with a second copy on a cheaper tier that also holds older segments.

High concurrency: a segment is the unit of computation and a process scans up to `druid.processing.numThreads` segments at once. Size segments so computing over any one takes at most 500ms (monitor the `query/segment/time` metric), so that resources are yielded often and no query is starved. Set the `priority` query context flag to de-prioritize slow download or reporting queries. Brokers can be dedicated to a tier, such as one set for interactive and one for reporting queries, and the Router can route queries to Brokers by datasource, interval and similar parameters.

## Checked

2026-11-08. Read querying/multitenancy.md in full. Added shared datasource partitioning, tiering and the high concurrency guidance (500ms segment computation target, priority flag).

Method: documentation only; no commands were run.
