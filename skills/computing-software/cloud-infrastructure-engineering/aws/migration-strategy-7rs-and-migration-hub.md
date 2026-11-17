---
id: computing-software.cloud-infrastructure-engineering.aws.migration-strategy-7rs-and-migration-hub
name: migration-strategy-7rs-and-migration-hub
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, migration, 7rs, migration-hub, application-discovery, rehost, replatform, refactor, repurchase, retire, retain, relocate, discovery-agent, agentless-collector, wave-planning, migration-evaluator, strategy-recommendations, mgn, dms, landing-zone, cutover]
level: practitioner
status: draft
description: "Plan an AWS migration end to end: Application Discovery Service inventory, 7 Rs disposition per application, wave planning and tracking in Migration Hub, and the tool each R maps to."
sources: ["AWS Prescriptive Guidance - Migration strategy (the 7 Rs) and mobilize phase", "AWS Application Discovery Service User Guide - Discovery agent and agentless collector", "AWS Migration Hub User Guide - Strategy Recommendations and migration tracking", "AWS Migration Evaluator documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration strategy — discover, decide the R per app, then run it in waves

**Goal:** an inventory with dependencies, a disposition for every application, a wave plan
ordered by risk and dependency, and a single tracker (Migration Hub) that shows where each
server is. (Trade-off reasoning between lift-and-shift and replatform lives in
`computing-software.cloud-infrastructure-engineering.cloud-architecture.migration-strategy-lift-and-shift-vs-replatform`.)

## 1. The 7 Rs and the AWS tool for each
| R | Meaning | Tool | When |
|---|---|---|---|
| **Rehost** | lift and shift VM → EC2 | MGN (`…aws.elastic-disaster-recovery-and-mgn`) | Fast exit from a data centre; optimise later |
| **Relocate** | move hypervisor-level | VMware Cloud on AWS / EKS Anywhere to EKS | Large VMware estates, no app change tolerated |
| **Replatform** | small changes for managed services | DMS to RDS, EC2 → Elastic Beanstalk/ECS, self-managed → MSK/ElastiCache | Clear win from managed DB/queue |
| **Refactor** | re-architect | Containers, serverless, microservices | High-change, high-value apps |
| **Repurchase** | move to SaaS | Marketplace | Commodity apps (CRM, HR) |
| **Retire** | switch off | — | Unused/duplicate (typically 10–20 % of an estate) |
| **Retain** | leave for now | Outposts/hybrid connectivity | Compliance, latency, end-of-life soon |
Default to rehost for the long tail, replatform where a managed service is obvious
(databases), refactor only the handful that pay for it.

## 2. Discovery
- **Application Discovery Service**:
  - **Agentless collector** (VMware OVA): inventory, utilisation, no in-guest install; no process-level dependencies.
  - **Discovery agent** (per server, Linux/Windows): processes, network connections → dependency map; 2 weeks minimum of data to capture monthly peaks.
  - Import CSV from CMDB for what you cannot instrument.
- Data lands in Migration Hub; **Athena data exploration** on it for custom queries (network
  connections grouped by port → "who talks to this DB").
- **Migration Evaluator** (formerly TSO Logic): business case/TCO from collected utilisation and licensing; produces the "what it will cost on AWS" number leadership needs.
- **Strategy Recommendations** (Migration Hub): analyses collected data + source code/DB
  (optional) and recommends an R per app with effort; treat as a first draft.

## 3. Group into applications and waves
- Group servers → **applications** in Migration Hub by dependency clusters, not org chart.
- Wave rules: (1) pilot wave of 5–10 low-risk, low-dependency apps to prove tooling and
  landing zone; (2) move tightly coupled servers in the same wave; (3) shared services
  (AD, DNS, monitoring, file shares) early or extended across hybrid connectivity; (4) big
  databases get their own cutover window with DMS CDC running ahead.
- Per app, record: owner, R, target architecture, data size, cutover window, rollback
  plan, test plan, go/no-go criteria. Migration Hub **Orchestrator** workflows template the
  steps for rehost/replatform (SAP, SQL Server templates exist).

## 4. Prerequisites: mobilise phase
- Landing zone (Control Tower/Organizations, accounts per environment, SSO, logging,
  networking via Transit Gateway, hybrid link via Direct Connect/VPN) **before** wave 1.
- Migration factory: standard runbook, MGN replication templates, tagging standard
  (`migration-wave`, `source-host`), CloudWatch agent/SSM baked into post-launch actions.
- Licensing: Windows/SQL BYOL needs Dedicated Hosts (License Manager); Oracle/SAP rules reviewed.
- Operational readiness: backup, patching, monitoring, cost allocation apply on day 1 in AWS.

## 5. Track and finish
- Migration Hub home region holds status across tools (MGN, DMS, partner tools) by server
  and application: `Not started / In progress / Completed`. Update status via API for
  manual moves.
- Weekly: servers migrated vs plan, cutover incidents, rollbacks, cost run-rate vs the
  Migration Evaluator case.
- After each wave: **decommission** source hardware/licences (the savings), rightsize
  (Compute Optimizer after 14 days), convert to Savings Plans once stable.
- **Migration Acceleration Program (MAP)** credits require tagging migrated resources with
  `map-migrated=<id>` — set it in launch templates from the start or lose the credits.

## Gotchas
- Discovery with only agentless data underestimates dependencies; the first wave will find
  the undocumented NFS mount and the hard-coded IP.
- Hard-coded IPs: plan to preserve private IPs (MGN can) or run a DNS cutover with
  short TTLs weeks ahead.
- Over-rotating to refactor stalls the programme; the data-centre exit date wins. Rehost,
  then modernise with the money saved.
- Databases are the critical path: licensing, size, CDC lag, and app connection strings.
- Latency between migrated apps and not-yet-migrated dependencies over the hybrid link
  breaks chatty apps; group them.
- Unconfirmed: current Strategy Recommendations language/DB coverage and Orchestrator templates — check the console.

## Verify
- [ ] Every server in the inventory has an application, an owner, an R and a wave.
- [ ] Dependency map reviewed for wave 1 apps; no cross-wave synchronous dependency without a hybrid-link latency test.
- [ ] Pilot wave cut over with measured downtime and a documented rollback that was rehearsed.
- [ ] Migration Hub status matches reality for 100 % of wave 1 servers.
- [ ] Source decommission tickets exist for completed waves; `map-migrated` tags present on launched resources.
