---
id: computing-software.systems-network-administration.backup-and-recovery.backup-repository-capacity-forecasting
name: backup-repository-capacity-forecasting
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [repository-capacity, capacity-planning, backup-storage, growth-forecast, retention]
level: practitioner
status: draft
description: "Forecast backup repository capacity: measure change rate and data reduction, model retention and GFS, project growth, and set thresholds that leave time to buy storage."
sources:
  - https://helpcenter.veeam.com/docs/one/reporter/capacity_planning_for_backup_repositories.html
  - https://www.veeam.com/calculators/simple/vbr/machines
  - https://bp.veeam.com/vbr/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Repository capacity forecasting

## Inputs to measure (not guess)
- **Source size** protected per tier (used space, not provisioned).
- **Daily change rate**: incremental size / source size from job statistics; typical 2-5% for servers, much higher for databases and file servers with churn.
- **Data reduction**: compression + dedupe ratio from job statistics (often 1.5-2x for mixed VMs).
- **Retention**: daily points, GFS weekly/monthly/yearly fulls, immutability padding.
- **Growth**: month-on-month source growth from 6-12 months of history.

## Simple model (forward incremental with weekly synthetic fulls on block-clone file systems)
Space ≈ (Full × reduction) + (Daily inc × days kept × reduction) + GFS fulls (block-cloned fulls on ReFS/XFS share blocks, so they cost roughly one incremental each). Without block cloning each GFS full costs a full.
Add 20% working space for merges/synthetic operations and immutability padding.

Cross-check with the vendor calculator (Veeam calculator) and Veeam ONE "Capacity Planning for Backup Repositories" which extrapolates trend to a "days left" figure.

## Thresholds
- Warn at 75% used or under 120 days left; act at 85% or under 90 days (procurement lead time).
- Immutable repositories cannot be emptied quickly; the only fast fixes are adding extents or pausing jobs, so warn earlier.

## Gotchas
- Retention changes (e.g. from 14 to 30 days) take full effect only after the new window fills; forecast the step change.
- Object storage padding: immutable blocks live up to the lock period plus generation padding.
- A ransomware event inflates change rate dramatically; leave headroom so encrypted-data backups do not push out good points.

## Verify
Compare last quarter's forecast with actual usage; adjust the change-rate assumption if off by more than 10%.
