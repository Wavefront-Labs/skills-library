---
id: computing-software.cloud-infrastructure-engineering.google-cloud.high-availability-and-disaster-recovery-design
name: high-availability-and-disaster-recovery-design
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, high-availability, disaster-recovery, rpo-rto, regional-vs-zonal, multi-region, dr-tiers, cold-warm-hot-standby, active-active, zone-failure, region-failure, global-load-balancer-failover, cross-region-replication, dr-runbook, dr-testing, dual-region-storage, failover-automation, resilience]
level: advanced
status: draft
description: "Design GCP for the failure you plan to survive: zonal vs regional vs multi-region blocks, RPO/RTO-driven DR tiers (cold, warm, hot, active-active), per-service replication, tested DR runbooks."
sources: ["https://cloud.google.com/architecture/disaster-recovery", "https://cloud.google.com/architecture/dr-scenarios-planning-guide", "https://cloud.google.com/architecture/dr-scenarios-for-applications", "https://cloud.google.com/architecture/dr-scenarios-for-data", "https://cloud.google.com/architecture/framework/reliability", "https://cloud.google.com/compute/docs/regions-zones", "https://cloud.google.com/architecture/infra-reliability-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# High availability and disaster recovery design

**Goal:** each tier of the system has a stated RPO/RTO, every component's scope (zonal,
regional, multi-regional) matches that promise, and the failover has been executed — not just drawn.

## 1. Start from the numbers
| Tier | RPO | RTO | Typical pattern | Relative cost |
|---|---|---|---|---|
| 3 | hours-day | day | backups to another region, rebuild from IaC (cold) | 1× + storage |
| 2 | minutes | hours | warm standby: data replicated, compute scaled to zero/min in region B | ~1.3× |
| 1 | seconds | minutes | hot standby: full stack in B, DNS/LB failover, async DB replica | ~2× |
| 0 | ~0 | ~0 | active-active multi-region with Spanner/multi-region DBs and global LB | 2-3× + engineering |
Most systems are tier 2-3; only the revenue path is tier 1. Write RPO/RTO per service into the SLO doc and let the business sign the cost.

## 2. Scope of each building block
| Zonal (dies with a zone) | Regional (survives a zone) | Multi-/global |
|---|---|---|
| VM, zonal PD, zonal MIG, zonal GKE, Memorystore basic, Filestore basic/zonal, local SSD | regional MIG, regional GKE, regional PD / Hyperdisk Balanced HA, Cloud SQL HA, AlloyDB, Memorystore standard, Filestore regional, regional Spanner, regional GCS, Cloud Run, Pub/Sub (global service, regional storage), internal LBs | multi-region Spanner, multi-/dual-region GCS, Firestore multi-region, BigQuery multi-region, Bigtable replicated, global external ALB, Cloud DNS, Cloud CDN, Cloud Armor, KMS multi-region keys |
Rule: **zone failure must be invisible** (regional everything in prod); **region failure** is the DR tier decision. Three zones per region; design MIGs/GKE node pools across all of them with `EVEN`/regional distribution and PDBs.

## 3. Region-failure patterns
- **Stateless compute**: deploy the same Cloud Run service / GKE workloads in regions A and B; **global external ALB** with backends in both (serverless NEGs or MIG/NEG backends); health checks drain a dead region automatically; `--capacity-scaler` to keep B warm at low capacity (tier 2) or full (tier 1). Internal: cross-region internal ALB or Cloud DNS failover routing policies.
- **Data**:
  - Cloud SQL: cross-region read replica → `promote-replica` (tier 1-2, RPO = replication lag); Enterprise Plus switchover for planned moves. AlloyDB secondary cluster.
  - Spanner: multi-region config (tier 0) — no failover to run.
  - GCS: dual-region bucket with **turbo replication** (15-min RPO SLA) or multi-region; versioning + Backup and DR for ransomware.
  - Firestore/BigQuery: multi-region locations; Bigtable: replicated clusters + multi-cluster app profile.
  - Memorystore: cache — rebuild; Valkey cross-region replication where available.
  - Pub/Sub: global; subscriptions survive, but consumers must run in B; message storage policy per region matters for residency.
  - Secrets/KMS: multi-region or replicated secrets; keys in both regions (CMEK on B's resources needs B keys — plan this before, not during).
- **Config and pipelines**: Terraform can recreate B from scratch (tier 3) but DR day is not the day to discover a region-specific hardcode; keep region as a variable and run `plan` for B monthly. Artifact Registry multi-region; Cloud Build regional triggers in both.
- **Entry point**: DNS TTL ≤ 60 s for anything you will repoint; global anycast IP removes the DNS step entirely.

## 4. Runbook and automation
Failover runbook per tier-1/2 system: decision criteria (who declares, after how long), pre-checks (replica lag, B capacity/quota), steps (promote DB, scale B, shift LB capacity / update DNS, re-enable writers, rotate KMS/secrets if needed), validation (synthetic transactions), failback steps (re-establish replication A←B, planned switchover). Automate the mechanical steps in Workflows with a human approval gate; never auto-fail-over databases on a single health signal.

## 5. Test it (or you do not have it)
- Quarterly: zone drain in prod (cordon/drain a GKE zone, `simulate-maintenance-event` on a MIG zone) — should be a non-event.
- Twice a year: regional DR exercise in staging with prod-sized data; annually in prod for tier 1 in a maintenance window: measure actual RTO/RPO, record in the reliability report, fix the gaps.
- Chaos lite: kill the primary Cloud SQL (`failover`), delete a Memorystore instance in staging, revoke a region's quota in a sandbox.

## Gotchas
- Quota in region B is **separate**; a warm standby with 10 % capacity cannot scale to 100 % unless B's quotas were raised in advance (see `quotas-and-quota-management`).
- Cross-region replicas, dual-region buckets and multi-region Spanner all bill inter-region egress; tier 1 costs more than the compute line suggests.
- Global LB + regional backends: a backend that *returns 200 while broken* keeps traffic — health checks must hit a dependency-aware endpoint.
- Cloud SQL promote is one-way; failback is a new replica build (hours for large DBs) — schedule it.
- Multi-region GCS protects data, not availability of your *readers* in a dead region; compute must exist elsewhere.
- Org-level resources (org policies, folders, IAM, Cloud Identity) are global and not a DR concern, but **your** Terraform state bucket and CI must not be single-region if you need them to rebuild B.

## Verify
- [ ] Every production service has RPO/RTO, tier and scope documented; no zonal resource backs a tier ≤ 2 service.
- [ ] Zone drain exercise shows zero SLO impact; MIG/GKE rebalance within minutes.
- [ ] DR exercise log shows measured RTO/RPO within target, including DB promotion and LB/DNS shift, with the failback completed.
- [ ] Region B quotas, KMS keys, secrets, images and a successful `terraform plan` for B are checked monthly by automation.
