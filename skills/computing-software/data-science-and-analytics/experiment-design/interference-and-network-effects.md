---
id: computing-software.data-science-and-analytics.experiment-design.interference-and-network-effects
name: interference-and-network-effects
category: computing-software
field: data-science-and-analytics
product: experiment-design
tags: [network-interference, switchback-test, cluster-randomisation]
level: advanced
status: draft
description: "Recognise SUTVA violations in marketplaces and networks and choose cluster, geo or switchback designs instead of user-level splits."
sources:
  - https://experimentguide.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interference
- User-level A/B assumes one user's treatment does not affect another's outcome.
- Violations: shared inventory, ride/delivery supply, social feeds.
- Alternatives: randomise clusters (geo, graph communities); switchback (alternate treatment over time blocks); budget-split in ads.
- Analyse at the cluster level (cluster-robust SE); power falls with fewer clusters.
## Gotchas
- Time-block designs need wash-out gaps for carry-over.
## Verify
- [ ] Spillover check: compare control users with high vs low exposure to treated neighbours.
