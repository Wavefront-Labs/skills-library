---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.migration-sizing
name: migration-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-assessment, migration-sizing, rightsizing, utilisation-based-sizing, performance-based-sizing]
level: practitioner
status: draft
description: "Size cloud targets from utilisation data instead of on-prem allocation: percentile choice, headroom, instance mapping, storage IOPS and validation."
sources: ["https://learn.microsoft.com/azure/migrate/concepts-assessment-calculation", "https://docs.aws.amazon.com/migrationhub/latest/ug/ec2-recommendations.html", "https://cloud.google.com/migration-center/docs/create-asset-reports"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Target sizing from utilisation data

## Steps
1. **Collect performance data** for at least 30 days at 5-15 minute granularity: CPU, memory,
   disk IOPS and throughput, network. Include month-end and seasonal peaks.
2. **Choose a percentile**: p95 is common (Azure Migrate performance-based sizing supports
   p50/p90/p95/p99); use p99 for latency-critical or bursty workloads.
3. **Apply a comfort factor / headroom**: e.g. 1.3x (Azure Migrate default comfort factor is
   1.3) for growth and measurement error.
4. **Normalise CPU** across processor generations: an old 2.0 GHz core is not a modern vCPU;
   use benchmark ratios (SPECint-based) where tools support it. Remember vCPU = hyperthread
   on most x86 instance types.
5. **Map to instance families**: memory-to-vCPU ratio drives family (general, compute,
   memory optimised); consider ARM where software supports it.
6. **Storage**: size disks by capacity and IOPS/throughput separately; managed disk tiers cap IOPS by size.
7. **Licensing constraints**: per-core licences (SQL Server, Oracle) push towards fewer
   faster cores or constrained-vCPU instance types.
8. **Validate after migration**: rightsizing review after 2-4 weeks of cloud metrics.

## Gotchas
- As-is sizing from allocation typically overprovisions by 30-50%.
- Memory utilisation is often missing from agentless data (needs guest access); without it, sizes default to allocated memory.

## Verify
- [ ] Sizing basis (percentile, comfort factor, period) documented per wave.
- [ ] Post-migration rightsizing review scheduled.
