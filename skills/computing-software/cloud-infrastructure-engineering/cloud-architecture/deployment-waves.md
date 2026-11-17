---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.deployment-waves
name: deployment-waves
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, fault-isolation, deployment-waves, progressive-rollout, bake-time, one-box, regional-rollout, blast-radius]
level: practitioner
status: draft
description: "Roll out changes in waves to limit blast radius: one-box, single zone, single region, then wider, with bake times, automated health gates and rollback."
sources: ["https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/", "https://learn.microsoft.com/azure/well-architected/operational-excellence/safe-deployments", "https://sre.google/workbook/canarying-releases/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deployment waves to limit blast radius

## Wave structure (example for a multi-region service)
1. Pre-production with integration and load tests.
2. **One-box**: single instance/pod in one zone of the lowest-traffic region.
3. **One zone** of that region.
4. Rest of the region.
5. Next region(s) in increasing size; never two regions at once early on.
6. Remaining regions in larger batches as confidence grows.

## Gates
- **Bake time** per wave (e.g. 1 h one-box, several hours per region), longer for first waves.
- Automated health checks: error rate, latency, saturation, business metrics compared to baseline;
  auto-rollback on regression.
- Time-of-day windows: deploy when engineers are online; avoid peak traffic.
- Same artefact promoted through all waves (no rebuilds).

## Also apply to
Config changes, feature flags, infrastructure changes and certificate rotations - outages are
often caused by global config pushed everywhere at once.

## Gotchas
- Waves that are only one region deep then "all the rest".
- Gates on technical metrics only; a bug corrupting orders passes CPU checks.
- Emergency fixes bypassing waves entirely; use faster waves, not none.

## Verify
- [ ] Pipeline shows waves, bake times and automated rollback for every production change type.
