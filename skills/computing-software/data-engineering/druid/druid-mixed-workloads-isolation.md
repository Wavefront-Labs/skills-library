---
id: computing-software.data-engineering.druid.druid-mixed-workloads-isolation
name: druid-mixed-workloads-isolation
category: computing-software
field: data-engineering
product: druid
tags: [mixed-workloads, query-laning, service-tiering, priority, broker-http-threads]
level: advanced
status: docs-checked
description: "Protect interactive queries from heavy ones with query laning and service tiering."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/mixed-workloads.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each query uses processing threads, memory buffers for intermediate results and HTTP threads between Brokers and data servers. Heavy queries returning large results use more than short light ones, and can take every available HTTP thread, slowing later queries and causing timeouts.

Druid offers two isolation strategies:
- Query laning: set a limit on the number of long-running queries executed on each Broker.
- Service tiering: define separate groups of Historicals and Brokers that receive different query assignments according to query priority.

To find out which resource is affected, profile with query metrics, JVM thread dumps or flame graphs. The largest bottleneck is likely the Broker HTTP threads, and the docs say to mitigate that with query laning. Mixed workloads also affect other resources such as processing threads and buffers.

The two strategies can be combined: laning limits long-running queries per Broker, while tiering gives separate Historical and Broker groups to different priorities. The page lists the resources a query consumes, namely processing threads, memory buffers and HTTP threads, so you can map observed contention to one of those.

## Checked

Method: 2026-11-09 docs-only read of the cited source page in full. All claims match the page; unchanged.
