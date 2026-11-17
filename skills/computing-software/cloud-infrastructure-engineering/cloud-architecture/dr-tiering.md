---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.dr-tiering
name: dr-tiering
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, disaster-recovery, dr-tiering, backup-and-restore, pilot-light, warm-standby, cost-vs-resilience-tradeoffs]
level: practitioner
status: draft
description: "Tier applications for DR by business impact: map tiers to RTO/RPO and strategy (backup, pilot light, warm standby, active-active) and cost the trade-off."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html", "https://learn.microsoft.com/azure/well-architected/reliability/disaster-recovery", "https://cloud.google.com/architecture/dr-scenarios-planning-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DR tiering and cost trade-off

## Steps
1. **Business impact analysis**: cost of downtime per hour and data loss per hour for each
   application; regulatory obligations; dependencies (a tier-1 app depending on a tier-3
   service is really tier-3 until fixed).
2. **Define 3-4 tiers** with targets, for example:
   - Tier 0/1: RTO minutes, RPO near zero, multi-site active-active or hot standby.
   - Tier 2: RTO under 4 h, RPO under 15 min, warm standby (scaled-down running copy).
   - Tier 3: RTO under 24 h, RPO hours, pilot light (data replicated, compute off).
   - Tier 4: RTO days, backup and restore.
3. **Cost each strategy** per app: standby compute, replicated storage, cross-region transfer,
   licences for DR copies, and test effort. Present cost vs downtime cost.
4. **Assign tiers** with business owners' sign-off; they must accept the RTO/RPO they pay for.
5. **Align dependencies**: shared services (identity, DNS, network) must be at the highest
   tier they support.
6. **Test frequency per tier** (tier 1 quarterly failover, tier 4 yearly restore).

## Gotchas
- Everything declared tier 1 makes DR unaffordable; force-rank with impact data.
- Restore time for large backups is often far longer than assumed; measure it.

## Verify
- [ ] Tier assignment signed by business owners.
- [ ] Dependencies' tiers match or exceed dependants'.
