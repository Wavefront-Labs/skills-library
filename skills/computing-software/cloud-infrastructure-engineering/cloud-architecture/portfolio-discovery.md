---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.portfolio-discovery
name: portfolio-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-assessment, portfolio-discovery, discovery-tools, application-inventory, cmdb]
level: practitioner
status: draft
description: "Discover and inventory a portfolio for migration: agent and agentless discovery tools, data collected, grouping servers into applications, and validation."
sources: ["https://docs.aws.amazon.com/application-discovery/latest/userguide/what-is-appdiscovery.html", "https://learn.microsoft.com/azure/migrate/migrate-services-overview", "https://cloud.google.com/migration-center/docs/migration-center-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Portfolio discovery and inventory

## Tools
- **Azure Migrate** appliance (agentless for VMware/Hyper-V/physical; dependency analysis).
- **AWS Application Discovery Service** (agentless connector or agents) feeding AWS Migration
  Hub; **AWS Transform / Migration Evaluator** for business case data.
- **Google Migration Center** (discovery client, StratoZone-based).
- Third parties (Flexera, device42, Cloudamize) when multi-cloud neutral output is needed.

## Steps
1. **Collect**: hostnames, OS and version, CPU/memory/disk allocation and utilisation
   (at least 30 days including month-end peaks, p95), installed software, databases,
   network connections (for dependencies), storage IOPS.
2. **Combine sources**: CMDB, virtualisation manager, licensing records, monitoring tools,
   firewall logs, owner interviews. Discovery alone cannot tell you business owner or criticality.
3. **Group into applications**: use dependency data plus naming and owner input; every server
   belongs to exactly one application or is flagged shared infrastructure.
4. **Enrich**: business owner, criticality, data classification, compliance scope, change
   windows, licence constraints, end-of-life dates.
5. **Validate** with owners; reconcile counts against CMDB; chase unknown servers (often the most risky).

## Gotchas
- Too-short collection windows miss quarterly batch peaks.
- Agentless dependency mapping misses traffic through NAT or load balancers; confirm critical flows.

## Verify
- [ ] >95% of servers grouped into an application with an owner.
- [ ] Utilisation data covers at least one month-end.
