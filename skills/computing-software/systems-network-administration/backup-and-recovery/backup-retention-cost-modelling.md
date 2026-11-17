---
id: computing-software.systems-network-administration.backup-and-recovery.backup-retention-cost-modelling
name: backup-retention-cost-modelling
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [retention-cost, capacity-planning, storage-cost, gfs, deduplication, object-storage-tiers, retention-policy]
level: practitioner
status: draft
description: "Model backup storage and cost for a retention policy: fulls, increments and GFS points, change rate, data reduction, cloud tier pricing with minimum durations, and restore egress."
sources:
  - https://aws.amazon.com/s3/pricing/
  - https://azure.microsoft.com/en-us/pricing/details/storage/blobs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retention cost modelling

**Goal:** know what a retention policy costs before agreeing to it, and compare options honestly.

## Inputs
- Source data size `S` (used, not provisioned).
- Daily change rate `c` (typically 2-10% for servers; measure from job stats).
- Data reduction ratio `r` (compression + dedupe; 1.5-2x for compression only, more on dedupe appliances).
- Policy: daily points `D`, weekly `W`, monthly `M`, yearly `Y` (GFS).
- Whether GFS fulls are space-efficient (block cloning/dedupe) or physical copies.

## Formula (forward incremental, physical fulls)
```text
Fulls     = (1 + W + M + Y) x S / r
Increments = D x S x c / r
Total     ~ Fulls + Increments  (+ ~10-20% working space for merges/transforms)
```
With block cloning or dedupe, each extra GFS full costs only its unique changed data since the previous full (roughly `S x c_period / r`), not a whole `S`.

## Worked example
S = 20 TB, c = 5%, r = 2, D = 14, W = 4, M = 12, Y = 0, physical fulls:
Fulls = 17 x 20 / 2 = 170 TB; Increments = 14 x 20 x 0.05 / 2 = 7 TB; total ~177 TB plus working space.
Same policy with block cloning (monthly change ~25%, weekly ~15%): roughly 10 + 4x1.5 + 12x2.5 + 7 ~ 53 TB.

## Cloud costs beyond GB-month
- **Minimum storage durations** (cool/cold/archive tiers charge early-deletion fees: e.g. 30, 90 or 180 days depending on tier and provider).
- **Retrieval and egress** charges on restore; archive tiers add rehydration delay (hours).
- **Request/API costs** for small-object backup formats.
- **Immutability** extends effective retention to at least the lock period.

## Use the model
Compare policies (e.g. 12 monthly vs 6 monthly + archive), show cost per extra retention point, and agree with data owners on which points have value.

## Verify
Compare model predictions with actual repository consumption after 3 months; recalibrate change rate and reduction ratio.
