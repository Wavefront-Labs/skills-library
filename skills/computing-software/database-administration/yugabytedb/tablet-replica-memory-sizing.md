---
id: computing-software.database-administration.yugabytedb.tablet-replica-memory-sizing
name: tablet-replica-memory-sizing
category: computing-software
field: database-administration
product: yugabytedb
tags: [memory, tablet-limits, sizing, memory-defaults, tablet-replicas, ysql-connections, memory-limit-hard-bytes]
level: advanced
status: docs-checked
description: "Size tserver memory and tablet replicas per node, with the per-1000-replica cost, the RAM table, and the flags that set memory limits and YSQL-optimised defaults."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/checklist.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/smart-defaults.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-tserver.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tablet replica and memory sizing

Cost model from the deployment checklist: every 1000 tablet replicas on a tserver need about 0.4 vCPU and 800 MiB of memory, plus about 6200 MiB extra for caches.

Reference points (RAM, supportable tablet replicas, YSQL connections):
- 8 GiB: 530 replicas, 65 connections
- 16 GiB: 1250 replicas, 130 connections
- 64 GiB: 5500 replicas, 370 connections

Memory flags:
- `--default_memory_limit_to_ram_ratio` (0.85) sets the process share of RAM; `--memory_limit_hard_bytes` overrides it with an absolute value.
- `--use_memory_defaults_optimized_for_ysql` is false by default for a bare tserver but true under yugabyted and YugabyteDB Anywhere. Set it to false on YCQL-only clusters so memory is not reserved for YSQL.
- `--db_block_cache_size_percentage` and `--tablet_overhead_size_percentage` divide the budget.
- `--ysql_max_connections` defaults to a value between 50 and 300 depending on RAM.

On Kubernetes the memory limit is derived from the pod limit, for example 4Gi becomes `--memory_limit_hard_bytes=4294967296`.

Enforce limits with the tablet-limit flags described in the tablet replica limits skill.

## Checked

2026-11-04. Confirmed against the deployment checklist (0.4 vCPU and 800 MiB per 1000 replicas, extra 6200 MiB, the RAM/replica/connection table rows for 8, 16 and 64 GiB), the yb-tserver reference (memory flag defaults, ysql_max_connections range, use_memory_defaults_optimized_for_ysql) and the Helm chart page (4Gi becomes 4294967296). Removed the block cache default, which the reference does not give as a plain number.

Method: documentation only; no commands were run.
