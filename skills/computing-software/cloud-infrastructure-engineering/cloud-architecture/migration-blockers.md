---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.migration-blockers
name: migration-blockers
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-assessment, migration-blockers, compatibility-assessment, unsupported-os, hardware-dependencies, licensing-constraints, latency-dependencies]
level: practitioner
status: draft
description: "Identify technical blockers before migration: unsupported OS/DB versions, hardware dongles, multicast, shared disks, hard-coded IPs, licensing and latency-sensitive links."
sources: ["https://learn.microsoft.com/azure/migrate/migrate-support-matrix", "https://docs.aws.amazon.com/mgn/latest/ug/Supported-Operating-Systems.html", "https://cloud.google.com/migrate/virtual-machines/docs/5.0/migrate/supported-os-versions"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Technical compatibility and migration blockers

## Blocker checklist
| Blocker | Detection | Typical resolution |
|---|---|---|
| Unsupported OS (e.g. very old Windows/Linux) | Discovery inventory vs replication tool support matrix | Upgrade in place first, replatform, or extended-support offerings |
| Unsupported DB version | DB assessment tools (DMA, AWS SCT) | Upgrade, managed engine version supported |
| Hardware dongles / serial / USB licences | Interview, device inventory | Network licence server, vendor licence change |
| Multicast/broadcast | Network capture, app docs | Redesign (unicast), overlay, or keep on-prem |
| Shared disks / clustering (WSFC, RAC) | Config review | Cloud shared disk options, managed HA, or redesign |
| Hard-coded IPs / hosts files | Config scan, grep | DNS names, keep IPs via IP planning |
| Latency-sensitive chatty links to on-prem | Flow analysis, APM | Move together (move group) |
| Licensing mobility | Licence terms | BYOL eligibility, dedicated hosts, licence-included |
| Large data volumes | Storage inventory | Offline transfer, CDC replication |
| Kernel modules / custom drivers | Agent pre-checks | Rebuild image, replatform |

## Steps
1. Run the replication/assessment tool's readiness report on all servers.
2. Merge with interview findings and dependency data.
3. Classify: blocker / needs remediation / OK; assign owners and remediation.
4. Feed into 7 R disposition and wave planning.

## Verify
- [ ] Every in-scope server has a readiness status.
- [ ] Blockers have remediation tasks before their wave date.
