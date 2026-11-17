---
id: computing-software.cloud-infrastructure-engineering.azure.bcdr-design-rto-rpo-region-pairs-and-composite-sla
name: bcdr-design-rto-rpo-region-pairs-and-composite-sla
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bcdr, business-continuity, disaster-recovery, rto, rpo, region-pairs, paired-regions, multi-region, active-active, active-passive, warm-standby, pilot-light, composite-sla, sla, availability-targets, reliability-targets, zone-redundant, zonal, cross-region, geo-replication, failover-runbook, dr-tiers, recovery-tiers, azure-sla-calculator]
level: advanced
status: draft
description: "Design BCDR on Azure from the numbers: RTO/RPO tiers, zone-redundant vs multi-region patterns (active-active, warm standby, pilot light), region pairs, per-service geo features, SLA math."
sources: ["Microsoft Learn - Azure Well-Architected Framework: Reliability pillar (RE:04 targets, RE:05 redundancy, RE:09 DR)", "Microsoft Learn - Azure cross-region replication and region pairs", "Microsoft Learn - Azure reliability guides per service (reliability.azure.com / reliability docs)", "Microsoft Learn - Multi-region design patterns (Azure Architecture Center: active-passive/active-active, mission-critical)", "Microsoft Service Level Agreements for Online Services (SLA documents per Azure service)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BCDR design — RTO/RPO tiers, region strategy and the SLA arithmetic

**Goal:** every workload sits in a named tier with a recovery pattern that matches
its RTO/RPO at a cost the business signed off, and the availability number you quote
is the product of the chain, not the best link.

## 1. Tiers before technology
| Tier | RTO | RPO | Pattern | Examples |
|---|---|---|---|---|
| 0 | < 15 min | ~0 | **Active-active multi-region**, data geo-replicated synchronously-ish (Cosmos multi-write, SQL failover group with auto-failover, Front Door) | payments, auth |
| 1 | < 1 h | < 15 min | **Warm standby** (hot data replica, compute scaled down in secondary) | core APIs, order systems |
| 2 | < 8 h | < 1 h | **Pilot light / ASR** (data replicated, compute built on demand from IaC + ASR) | internal apps |
| 3 | < 72 h | < 24 h | **Backup + redeploy** (geo-redundant backups, pipeline redeploy) | batch, dev tools |
Zone redundancy within a region is the baseline for Tier 0–2 regardless of the multi-region choice; it handles the far more common datacentre failure with no runbook.

## 2. Region strategy
- **Region pairs** (e.g. UK South ↔ UK West, West Europe ↔ North Europe): sequenced platform updates, prioritised recovery, GRS target, data residency kept in the geography. Some newer regions have **no pair** — then multi-region means your own replication (ZRS + manual secondary) or accept single-region + zones.
- Choose the secondary by: pair first, then service availability (not every SKU/service exists in the pair — check *Products available by region*), data-residency law, latency to users, and capacity (ask your account team for reserved capacity if you intend to fail over big fleets).
- Per-service geo-features you combine (don't reinvent):
  Storage GRS/RA-GZRS + account failover; SQL DB/MI **auto-failover groups**; Cosmos DB multi-region writes/automatic failover; Key Vault (auto-replicated in pair); Event Hubs/Service Bus **geo-DR** (metadata) or geo-replication (data, newer); Redis Enterprise active geo-replication; AKS = cluster per region + GitOps; App Service/Functions = deploy per region; Container Registry geo-replication; Front Door/Traffic Manager for routing; ASR for IaaS; Azure DNS is global; Entra ID is global; Log Analytics workspace replication (newer) for observability DR.
- Global services (Entra, DNS, Front Door, Resource Manager) have their own global SLAs; a regional outage can still break *management* (ARM throttled) — don't make failover depend on creating resources in the failed region.

## 3. Patterns in Azure terms
- **Active-active**: Front Door → two regional stacks; data tier either multi-master (Cosmos) or single-writer with reads local and writes forwarded (SQL failover group listener; app tolerates write latency); session state externalised (Redis geo or stateless tokens); idempotent writes for retries across regions.
- **Warm standby**: same IaC deployed in both regions, secondary compute at minimum scale, data replicated continuously (SQL FOG, Storage GRS, Cosmos), Front Door priority routing; failover = promote data + scale up + flip priority (scripted, < 1 h).
- **Pilot light**: only data replicated; compute deployed by pipeline on failover (pre-staged images in geo-replicated gallery/ACR, capacity reservations if RTO is tight); ASR for lift-and-shift VMs.
- **Backup/restore**: cross-region restore from vault; longest RTO, cheapest.
- Decide **failover triggers** (automatic for data tiers only where the app can handle it; manual for the whole workload with a named decision-maker) and **failback** (planned, off-peak, often harder than failover).

## 4. Composite SLA arithmetic
- Serial dependencies multiply: Front Door 99.99 % × App Service 99.95 % × SQL DB 99.99 % × Key Vault 99.99 % ≈ **99.92 %** (~7 h/yr).
- Parallel independent paths: 1 − (1 − A)(1 − B): two regions at 99.95 % each (with a 99.99 % router) ≈ 99.99 %+ for the compute layer — but the shared data tier and the router cap it.
- Zone-redundant SKUs usually carry a higher SLA line (VMs: 99.9 % single → 99.95 % set → 99.99 % zones; SQL DB zone-redundant Business Critical 99.995 %).
- Write the chain down per user-facing flow, use the current SLA documents (they change), and compare with the SLO: if the composite is below target, the only fixes are removing a serial dependency, caching/degrading gracefully, or adding redundancy. The SLA is a credit mechanism, not your availability — measure actual uptime from synthetic tests.

## 5. Runbooks and drills
- One runbook per tier: detection (Service Health + synthetic test from outside), decision (who, within how many minutes), execution (ordered steps with commands: promote SQL FOG `az sql failover-group set-primary`, storage failover, Front Door priority flip, ASR plan), validation (smoke tests), communication, failback plan.
- Game day at least annually per Tier 0–1 workload; Tier 2 restore drill quarterly (see backup/ASR skills); Chaos Studio zone-down experiments for the zone layer.
- Dependencies outside Azure (SaaS, on-prem AD, payment providers, DNS registrar) go in the runbook too — they're usually the actual weak link.
- Cost: present the business with the cost of each tier (secondary compute, replication egress, duplicated licences) next to the hourly cost of downtime; tiers get chosen honestly when both numbers are on the page.

## Gotchas
- "GRS" ≠ DR: storage account failover is customer-initiated and loses the last minutes; apps still need to be redirected to the account after failover — and after failover the account is LRS until re-enabled.
- Auto-failover groups fail over *data*; connection strings via the FOG listener are fine, but the app in the primary region keeps writing cross-region unless you also move compute.
- Key Vault's paired-region replication is read-only in the secondary during an outage — you can't create secrets during DR; plan rotations accordingly.
- Private DNS zones, private endpoints and ExpressRoute are regional constructs: the secondary region needs its own, pre-built, or "warm standby" is cold networking.
- Quotas in the secondary are separate; a 2 000-vCPU failover into a subscription with a 200-vCPU quota fails. Pre-raise.
- Multi-write Cosmos without a conflict policy and idempotent clients produces silent data divergence under partition.

## Verify
- [ ] Tier register: every production workload has tier, RTO/RPO, pattern, owner, last drill date.
- [ ] Composite SLA sheet per flow matches current SLA documents; gap to SLO explained or closed.
- [ ] Secondary region: quotas raised, capacity reservations where required, networking/DNS/private endpoints pre-provisioned via the same IaC.
- [ ] Last game day: failover of a Tier-1 workload completed within RTO with measured data loss ≤ RPO; failback executed.
