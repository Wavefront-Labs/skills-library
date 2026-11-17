---
id: computing-software.messaging-and-integration.redpanda.space-management-phases-and-local-cache
name: space-management-phases-and-local-cache
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [space-management, tiered-storage, disk-reservation, cache, retention-local-strict, eviction]
level: advanced
status: docs-checked
description: "How Redpanda space management treats local disk as a cache for Tiered Storage topics: reserved, cache and log areas and the five eviction phases."
sources:
  - https://docs.redpanda.com/streaming/current/manage/cluster-maintenance/disk-utilization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Space management uses local disk as a cache alongside Tiered Storage. Disk is split into areas:
- **Reserved** (`disk_reservation_percent`): space Redpanda does not use; a buffer against alerts and SSD slowdown near capacity.
- **Cache storage**: the lower of `cloud_storage_cache_size_percent` and `cloud_storage_cache_size`.
- **Log storage**: the lower of `retention_local_target_capacity_percent` and `retention_local_target_capacity_bytes`.

Cache and log percentages apply to the disk left after the reservation (on a 100 GiB disk with 20% reserved they apply to 80 GiB). They are configured independently, so the combined target can exceed 100%, which is safe only when they use separate disks.

`space_management_enable` controls phases 2 to 5; new clusters since v23.3.2 default it to true, and upgraded clusters should be checked.

**Eviction phases** run until log storage falls below target.
1. **Follow retention policy** (all topics). With `retention_local_strict` false (default) housekeeping removes data above the log storage reservation; with true it uses local retention settings (true on clusters upgraded from 23.1 or earlier).
2. **Trim to local retention** (Tiered Storage only): with strict true, fair removal until each topic hits its local retention target.
3. **Default local retention topics**: trimmed to the low-space level of two segments, only data safely in object storage.
4. **Explicit retention topics**: same, down to two segments.
5. **Trim to the active segment**. The active segment cannot be removed until it rolls (`segment.bytes` or `segment.ms`).

Phases 2 to 5 only touch Tiered Storage topics, since only they are already stored in object storage.

## Checked

2026-11-08. Read the whole Disk Utilization page. Confirmed: reserved, cache and log areas, the 100 GiB example, independent percentages and the combined-target caveat, space_management_enable default, all five phases and the retention_local_strict behavior. Nothing removed.

Method: documentation only; no commands were run.
