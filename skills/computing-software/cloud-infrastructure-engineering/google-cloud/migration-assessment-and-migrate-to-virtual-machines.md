---
id: computing-software.cloud-infrastructure-engineering.google-cloud.migration-assessment-and-migrate-to-virtual-machines
name: migration-assessment-and-migrate-to-virtual-machines
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, migration, migration-assessment, migration-center, migrate-to-virtual-machines, migrate-for-compute, m4ce, discovery-client, tco-report, wave-planning, lift-and-shift, replatform, rehost, cutover, test-clone, vmware-migration, aws-to-gcp, migrate-to-containers, migration-waves]
level: advanced
status: draft
description: "Plan and run a migration to GCP: Migration Center discovery and TCO, the 6R decision per workload, wave planning, Migrate to Virtual Machines replication, test clones and cutover, prerequisites."
sources: ["https://cloud.google.com/migration-center/docs/migration-center-overview", "https://cloud.google.com/migration-center/docs/discovery-client-overview", "https://cloud.google.com/migrate/virtual-machines/docs/5.0/concepts/architecture", "https://cloud.google.com/migrate/virtual-machines/docs/5.0/migrate/migration-flow", "https://cloud.google.com/architecture/migration-to-gcp-getting-started", "https://cloud.google.com/architecture/migration-to-google-cloud-assessing-and-discovering-your-workloads", "https://cloud.google.com/migrate/containers/docs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration assessment and Migrate to Virtual Machines

**Goal:** an inventory with real utilisation, a per-workload decision (rehost, replatform,
refactor, retire…), waves that respect dependencies, and VM cutovers that take minutes because replication ran for days.

## 1. Discover and assess (Migration Center)
- Deploy the **discovery client** (VM/appliance in the datacentre) to collect inventory from vSphere/Hyper-V/physical via guest collection, or upload RVTools/CSV exports; AWS/Azure via API-based discovery.
- Collect **performance data for ≥ 2 weeks** (CPU/mem/disk/network percentiles) — sizing on peak-of-provisioned is why cloud costs "more".
- Group assets into **applications** (tags from discovery, network dependency data), set **preference sets** (region, machine family, sizing percentile p95, CUD/Spot assumptions, licensing BYOL vs on-demand) and generate the **TCO report** (compare on-prem/AWS cost vs GCP by scenario). Export to BigQuery/Sheets for finance.
- Output of this phase: catalogue (owner, env, criticality, dependencies, OS, licence, data size, RPO/RTO), target architecture per app, and the waves.

## 2. Decide per workload (6 R)
| R | When | GCP landing |
|---|---|---|
| **Rehost** (lift-and-shift) | stable, well-understood, time-boxed migration | Compute Engine via Migrate to VMs |
| **Replatform** | easy wins with managed services | Cloud SQL (DMS), GKE Autopilot (Migrate to Containers), Cloud Run, Filestore, Memorystore |
| **Refactor** | app will change anyway, needs elasticity | Cloud Run/GKE, Spanner/Firestore, Pub/Sub |
| **Repurchase** | SaaS exists | Marketplace/SaaS |
| **Retire** | nobody owns it | delete (10-20 % of inventories) |
| **Retain** | hardware/licence/latency bound | on-prem + Interconnect (Google Distributed Cloud for edge) |
Rehost first, modernise after cutover ("migrate then modernise") unless the app is unsupported on GCE (unsupported OS, hardware dongles, >3 TB memory, exotic storage).

## 3. Prerequisites (do before wave 1)
Landing zone (`landing-zone-bootstrap`), Shared VPC with on-prem routable ranges and hybrid connectivity sized for replication (`hybrid-connectivity-vpn-and-interconnect`), identity (`cloud-identity-and-groups`, OS Login), image/patch standards, logging/monitoring, **quota** in the target region for the biggest wave (`quotas-and-quota-management`), backup policy (`backup-and-dr-service`), cost tags/labels per app, and a **runbook template** per wave.

## 4. Migrate to Virtual Machines (M2VM)
Sources: vSphere (Migrate Connector appliance on-prem), AWS EC2, Azure VMs (cloud connectors), physical/other via disk import. Flow:
1. **Register the source** (`gcloud migration vms sources create`) and inventory VMs in the console.
2. **Create a migration** per VM or group. Most teams drive this from the console (bulk CSV for target details) or the VM Migration API; `gcloud migration vms` covers sources and groups, and Terraform support is partial — check the current provider before planning full IaC.
3. **Start replication**: continuous, incremental, agentless (vSphere snapshots / EBS snapshots); first sync hours-days, then deltas every few minutes; watch *replication cycle* status and lag.
4. **Test clone**: create a clone in an **isolated VPC/subnet** while replication continues — boot, run app tests, measure performance, fix startup issues (drivers are injected automatically: VirtIO, guest environment, licensing).
5. **Cut over**: freeze app writes → final sync → `cut-over` creates the production VM (target details: project, zone, machine type, network, service account, labels, Shielded VM, disk type) → validate → update DNS/LB → **finalize** (stops replication, frees source snapshots). Rollback = power the source back on until finalize.
- Groups let you cut over a wave together; `--target-details` in bulk via CSV in console.
- OS adaptation: Windows licensing switched to GCP (or BYOL on sole-tenant), SUSE/RHEL licence conversion options, old kernels may need pre-migration updates for VirtIO.
- Bandwidth: replication uses the hybrid link; throttle per source (`--replication-bandwidth`) during business hours.

## 5. Waves and cutover hygiene
- Wave 0: non-critical, few dependencies, proves the runbook. Waves grouped by application dependency (the discovery dependency map), same cutover window, rollback plan per wave.
- Cutover checklist: freeze window agreed, backups taken, DNS TTL lowered 24 h before, monitoring on both sides, go/no-go at a fixed time, hypercare rota for 2 weeks, source decommission date.
- Track: VMs migrated / planned, cutover duration vs target, incidents per wave, cost vs TCO model; feed deviations back into sizing for later waves.

## Gotchas
- Oversized VMs from "as-is" sizing are the #1 cost complaint; use p95 utilisation and right-size again 30 days after cutover with Recommender.
- Applications with hard-coded IPs/hostnames break at cutover; discover those in the test clone, not in prod.
- Replication of VMs with high churn (databases) never converges — migrate DBs with DMS/native replication, not M2VM.
- Test clones in the same VPC as prod with the same hostname/IP cause conflicts; isolate them.
- Licence terms (Windows, SQL Server, Oracle) decide sole-tenant vs shared before the target machine type is chosen (see `sole-tenant-nodes-and-licensing`).

## Verify
- [ ] Migration Center shows ≥ 2 weeks of performance data for every in-scope asset; TCO report signed off by finance.
- [ ] Every workload has an R decision and a wave; dependencies map shows no cross-wave hard dependencies.
- [ ] Wave 0 test clones pass app tests; cutover of the wave completes within the window with rollback untested-but-ready.
- [ ] 30 days post-cutover: right-sizing applied, sources decommissioned, monitoring/backup/labels present on every migrated VM.
