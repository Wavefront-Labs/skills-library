---
id: computing-software.database-administration.clickhouse.hardware-sizing-disk-cpu-memory
name: hardware-sizing-disk-cpu-memory
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, sizing, hardware, cpu, disk, memory, iops]
level: practitioner
status: docs-checked
description: "Size open-source ClickHouse servers by workload: disk type, CPU family, cores-to-memory ratios, memory-to-storage ratio and replicas."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/sizing-and-hardware-recommendations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hardware sizing disk cpu memory
Factors to weigh: concurrency (requests per second), throughput (rows per second), data volume, retention policy, hardware costs and maintenance costs. The guide is for open-source users; ClickHouse Cloud scales automatically.

Disk: for performance, directly attach provisioned-IOPS SSD volumes (or the cloud equivalent). For lower cost, use general-purpose SSD EBS volumes, tier hot/warm/cold on SSD and HDD, or use S3 to separate compute and storage.

CPU family:
- Latency in the tens of milliseconds, customer-facing: EC2 i3 or i4i (IO-optimised) or equivalent.
- High concurrency (100+ queries per second): compute-optimised C series.
- Data warehousing and ad-hoc analytics: memory-optimised R series.
There is no standard CPU utilisation target; for ad-hoc analytical use the guide says to target 10-20%. More concurrent queries, more data processed, or compute-intensive UDFs need more cores.

Memory-to-core ratios: M-type 4 GB:1, R-type 8 GB:1, C-type 2 GB:1 (e.g. 100 GB per 25 cores on M-type). Memory-to-storage: 1:1 for low volumes (but not below 8 GB total), 1:100 to 1:130 for long retention or high volume (100 GB RAM per replica for 10 TB), 1:30 to 1:50 for frequently accessed customer-facing workloads. Lower memory is possible by enabling `max_bytes_before_external_group_by` and `max_bytes_before_external_sort` to spill to disk, at a possibly significant performance cost.

Replicas: at least three per shard (two with Amazon EBS); scale vertically before adding replicas. ClickHouse does not shard automatically and re-sharding is expensive, so the guide suggests the largest server available.

## Checked
2026-11-03. Confirmed everything above against the "Sizing and hardware recommendations" page. Removed: the load-test and `system.query_log` process, the "no single right size" gotcha wording and the Verify step, which are not on the page.
Method: documentation only; no commands were run.
