---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.data-minimisation
name: data-minimisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-sustainability, data-minimisation, data-retention, sustainable-data, storage-efficiency]
level: practitioner
status: draft
description: "Minimise stored and moved data for sustainability and cost: retention schedules, deleting redundant copies, compression, efficient formats and lifecycle."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/data.html", "https://learn.microsoft.com/azure/well-architected/sustainability/sustainability-storage", "https://gdpr-info.eu/art-5-gdpr/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data minimisation and retention for sustainability

Every stored byte consumes energy and embodied hardware, replicated across zones and backups.
Minimisation also lowers cost and privacy risk (GDPR Article 5 data minimisation and storage limitation).

## Steps
1. **Inventory large data**: biggest buckets, databases, log groups, snapshots and backups by
   owner (Storage Lens, Azure storage insights, GCS usage).
2. **Retention schedule** per data class from legal and business need; default deletion
   rather than default keep. Apply lifecycle expiry rules (logs 30-90 days hot, archive or delete).
3. **Remove redundancy**: duplicate copies across environments, orphaned snapshots and
   volumes, old AMIs/images, unused replicas, full-copy dev databases (use subsets or synthetic data).
4. **Store efficiently**: compression and columnar formats (Parquet + ZSTD), deduplication,
   right durability (do not multi-region replicate reproducible data), cold tiers for rarely read data.
5. **Move less**: process data where it lives, cache, avoid cross-region replication without need,
   send deltas not full copies.
6. **Logging**: sample debug logs, drop noisy fields, reduce metric cardinality.
7. **Track**: total TB stored per business unit of output; trend down.

## Gotchas
- Legal holds must override lifecycle deletion; integrate hold flags before automation.
- Backups that outlive the source data's retention violate retention policies.

## Verify
- [ ] Every large data store has a lifecycle or retention rule.
- [ ] Orphaned snapshot/volume report reviewed monthly.
