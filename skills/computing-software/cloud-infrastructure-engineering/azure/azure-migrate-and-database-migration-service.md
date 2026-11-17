---
id: computing-software.cloud-infrastructure-engineering.azure.azure-migrate-and-database-migration-service
name: azure-migrate-and-database-migration-service
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-migrate, migration, migration-assessment, discovery-appliance, dependency-analysis, business-case, server-migration, agentless-migration, replication-appliance, test-migration, cutover, database-migration-service, dms, data-migration-assistant, sql-migration-extension, azure-sql-migration, online-migration, offline-migration, managed-instance-link, migration-waves, rehost, replatform, cloud-adoption-framework, sizing-assessment]
level: practitioner
status: draft
description: "Migrate to Azure end to end: Azure Migrate discovery/assessment with dependency analysis, wave planning, agentless server migration with test migrations and cutover, DMS for SQL/PostgreSQL."
sources: ["Microsoft Learn - Azure Migrate overview, appliance discovery and assessments", "Microsoft Learn - Dependency analysis and Business case in Azure Migrate", "Microsoft Learn - Migrate VMware/Hyper-V/physical servers to Azure (agentless and agent-based), test migration and cutover", "Microsoft Learn - Azure Database Migration Service (Azure SQL migration extension, online/offline) and Managed Instance link", "Microsoft Cloud Adoption Framework - Migrate methodology (waves, readiness, landing zone)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Migrate and Database Migration Service — discover, assess, rehearse, cut over

**Goal:** an inventory you trust, assessments that size and price the target, waves
grouped by real dependencies, and every server/database migrated through a test
migration before a cutover with a known rollback.

## 1. Discover
- Create an **Azure Migrate project** (region = where metadata lives, not the target) in the landing zone subscription.
- Deploy the **appliance** (OVA for VMware vCenter, VHD for Hyper-V, Windows installer for physical/other clouds) with a read-only vCenter account / WinRM-SSH guest credentials; it discovers VMs, performance (every 20 s → averages), installed apps, **SQL Server instances/databases**, web apps (IIS/Tomcat), and — with guest credentials — **dependency analysis** (agentless: netstat-style connections; agent-based via AMA/Dependency agent for process-level maps).
- Alternatives: CSV/RVTools import for quick-and-dirty, or discovery from other tools (Cloudamize, Device42, Flexera) via the ISV integration.
- Run discovery ≥ 2–4 weeks (a month-end in it) so performance-based sizing sees peaks.

## 2. Assess
```text
Assessment types: Azure VM (rehost), Azure SQL (SQL DB / MI / SQL on VM readiness + SKU), Azure App Service / AKS (web apps), AVS (VMware Solution)
Settings: target region, sizing = Performance-based (95th percentile × comfort factor 1.3) vs As on-premises, pricing (reserved 3-yr, Hybrid Benefit, Dev/Test), VM series allow-list, storage type
Output per server: readiness (Ready / Conditionally / Not ready with reasons: unsupported OS, boot type, disk > 32 TB), recommended SKU + disks, monthly compute/storage cost, confidence rating (1-5 stars — low = not enough perf data)
```
- **Business case**: TCO/ROI comparing on-prem (hardware, licences, power, labour assumptions you can edit) vs Azure, with sustainability and "quick wins" — the artefact for the funding decision.
- **Dependency groups**: use the map to form **waves** — servers that talk to each other migrate together; an app tier split across waves is a latency and firewall problem.
- Export to Excel; the assessment feeds the landing zone capacity (vCPU quotas per family/region) and the reservation plan.

## 3. Migrate servers
- **Agentless VMware** (via the appliance, snapshot-based replication; concurrent-replication limits per appliance and scale-out appliances apply — check the current scale guide) / **Hyper-V** (host provider) / **agent-based** (replication appliance + Mobility service; physical, AWS/GCP VMs, VMware without vCenter access).
- Steps per wave:
  1. *Replicate*: pick VMs, target subscription/RG/VNet/subnet, availability (zone/set), VM size (from assessment), disk type, **Hybrid Benefit**, tags; initial replication (hours–days by data/bandwidth: throttle via appliance settings or ExpressRoute).
  2. *Test migration* into an **isolated test VNet** — boots a copy, no impact on source; validate login, services, app; delete test VM.
  3. Remediate: static IPs (Azure assigns DHCP — set in guest to DHCP, reserve in Azure), hostnames/DNS, licensing, agents, monitoring, backup policy, NSG/UDR, dependency firewalls.
  4. *Migrate* (cutover): shutdown source (option), final delta, create Azure VM; **complete migration** stops replication. Rollback = power on the source (keep it ≥ 1–2 weeks).
- Post-migration automation: enable Backup/Update Manager/Defender via tag-driven Policy; VM Insights; right-size after 2 weeks of metrics (Advisor).
- Migrations needing conversion (Gen1→Gen2/Trusted Launch, OS upgrades) are easier as **rebuild from image** than lift-and-shift; `.vhd` upload (`az disk create --source` / `azcopy`) + `az vm create --attach-os-disk` for one-offs.

## 4. Migrate databases
| Source → Target | Tool |
|---|---|
| SQL Server → **Azure SQL MI** | Azure SQL migration extension (Azure Data Studio) / DMS: **online** via log shipping from backups in blob (continuous restore, minimal cutover) or **offline**; or **Managed Instance link** (distributed AG, near-zero downtime, 2016+) |
| SQL Server → **SQL DB** | DMS offline (schema via `SqlPackage`/DACPAC, data via DMS), or transactional replication, or BACPAC for small DBs |
| SQL Server → **SQL on VM** | native backup/restore to URL, or Azure Migrate server migration of the whole VM |
| PostgreSQL/MySQL → flexible server | DMS (offline for both, online for PostgreSQL via logical replication / MySQL via binlog), `pg_dump`/`pg_restore`, `mydumper/myloader` |
| Oracle → PostgreSQL/SQL | Ora2Pg / SSMA + DMS data load |
```bash
az datamigration sql-managed-instance create --managed-instance-name sqlmi-prod --resource-group rg --target-db-name orders \
  --source-sql-connection '{"authentication":"WindowsAuthentication","dataSource":"sql01.corp.example.com","userName":"<DOMAIN>\\svc-dms","password":"<from KV>","encryptConnection":true,"trustServerCertificate":true}' \
  --offline-configuration last-backup-name=orders-full.bak --source-location '{"fileShare":{"path":"\\\\fs01\\backups","username":"<DOMAIN>\\svc-dms","password":"<from KV>"}}' \
  --target-location '{"storageAccountResourceId":"<st-id>","accountKey":"<key>"}' --migration-service <dms-resource-id> --scope <mi-id>
```
- **Pre-migration**: Data Migration Assistant / the ADS extension *assessment* finds blocking features (cross-DB queries, CLR, Agent jobs, SQL logins/SIDs, linked servers, `xp_cmdshell`), compatibility level issues, and recommends SKU from perf counters.
- Logins, jobs, linked servers, credentials are **instance-level**: script them (`dbatools` `Copy-DbaLogin`, `Export-DbaLogin`) or use MI link; SQL DB needs contained users.
- Cutover checklist: stop writes (read-only / app down), final backup/log restore, compare row counts/checksums, update connection strings (listener DNS!), re-enable writes, keep source read-only for rollback window.

## 5. Program mechanics
- Readiness per server: OS supported in Azure, boot type (UEFI → Gen2/Trusted Launch), disks, in-guest agents (remove old AV/backup agents), licensing (Windows/SQL Hybrid Benefit, RHEL/SLES BYOS), time sync, local accounts.
- Landing zone first (networking, identity, policy, monitoring) — migrating into a sandbox and "fixing later" is how the estate ends up untagged and unbacked-up.
- Track waves in a register: server, app, owner, wave, test-migration date, cutover date, rollback plan, decommission date; measure RTO of each cutover; decommission on-prem within 30 days to realise savings.
- Modernise selectively: web apps → App Service (Azure Migrate App Service assessment + *App Service migration assistant*), SQL → MI/SQL DB, file servers → Azure Files/File Sync, AD → keep DCs as VMs + Entra Connect.

## Gotchas
- Assessment confidence 1–2 stars = sizing is a guess (short discovery, powered-off VMs); extend discovery before buying reservations.
- Agentless VMware replication needs vCenter snapshot capacity and 443 from the appliance to Azure; CBT-disabled VMs replicate full each cycle.
- A VM migrated with its on-prem static IP inside the guest and no matching Azure subnet is unreachable after cutover — fix NIC settings in the test migration.
- DMS online SQL→MI needs the backups in a share/blob **with checksum** (`WITH CHECKSUM`) and the full/diff/log chain unbroken; a stray native backup job on the source breaks the chain.
- Target MI/SQL DB collation/time zone are set at creation; mismatch surfaces as app bugs weeks later.
- Decommission the Azure Migrate appliance and replication appliances; they hold vCenter/guest credentials.

## Verify
- [ ] Assessment report: 100 % of in-scope servers *Ready* or remediated; confidence ≥ 4; cost within the business-case envelope; quotas raised for the wave's families.
- [ ] Each wave had a test migration with a signed app validation before cutover; cutover RTO recorded; source kept for the rollback window then decommissioned.
- [ ] Database cutover: row counts/checksums match, logins/jobs recreated, app connected via the new endpoint; DMS activity shows `Succeeded`.
- [ ] Post-migration: every migrated VM shows Backup, Update Manager, Defender, AMA and tags via Policy compliance; right-sizing review scheduled at +14 days.
