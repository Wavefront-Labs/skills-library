---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.migration-factory
name: migration-factory
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-execution, migration-factory, migration-at-scale, wave-cadence, runbook-automation, migration-pods]
level: advanced
status: draft
description: "Run a migration factory for hundreds of servers: pods and roles, standard runbooks, automation, wave cadence, metadata tracking and continuous improvement."
sources: ["https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-factory-cloudendure/welcome.html", "https://aws.amazon.com/solutions/implementations/cloud-migration-factory-on-aws/", "https://learn.microsoft.com/azure/cloud-adoption-framework/migrate/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration factory operating model

## Structure
- **Portfolio/planning team**: discovery, wave planning, scheduling with app owners.
- **Migration pods** (3-6 people each): execute rehost/replatform with the standard runbook.
- **Platform/landing-zone team**: networks, accounts, shared services ready ahead of waves.
- **Testing and business liaison**: UAT coordination, go/no-go.
- **Factory lead/PMO**: metrics, risks, cadence.

## Mechanics
1. Standard runbook per pattern (rehost Windows, rehost Linux, DB replatform), checklists and
   pre-approved change templates.
2. Metadata store of every server/app: wave, status, target specs, owner, test result
   (spreadsheet at small scale; Cloud Migration Factory on AWS or migration tool projects at scale).
3. Automation: agent install, replication start, launch template config, post-launch scripts,
   DNS change, CMDB update.
4. Cadence: e.g. weekly waves; T-4 weeks plan, T-2 build/replicate, T-1 test, T cutover,
   T+2 weeks hypercare.
5. Metrics: servers migrated per week, rollback rate, defects per wave, cycle time, cost per server.
6. Retrospective each wave; update runbooks.

## Gotchas
- Factory speed outruns landing-zone or business test capacity - capacity plan all of them.
- Exceptions (complex apps) clogging the line; route them to a separate specialist track.

## Verify
- [ ] Throughput target met for three consecutive waves.
- [ ] Rollback rate trending down.
