---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.incident-management
name: incident-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, operational-excellence, incident-management, incident-commander, severity-levels, incident-roles, status-communication, on-call]
level: practitioner
status: draft
description: "Set up an incident management process: severity definitions, roles (commander, ops, comms), declaration, communication cadence, escalation and handover."
sources: ["https://sre.google/sre-book/managing-incidents/", "https://response.pagerduty.com/", "https://learn.microsoft.com/azure/well-architected/operational-excellence/incident-response"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Incident management process

## Severity (example)
| Sev | Definition | Response |
|---|---|---|
| 1 | Critical flow down for many users / data loss / security breach | Page immediately, IC assigned, exec + status page |
| 2 | Major degradation or a critical flow down for a subset | Page, IC, stakeholder updates |
| 3 | Minor impact, workaround exists | Business hours ticket |

## Roles
- **Incident commander (IC)**: coordinates, decides, delegates; does not debug.
- **Operations / subject experts**: investigate and mitigate.
- **Communications lead**: internal updates and status page on a fixed cadence (e.g. every 30 min Sev1).
- **Scribe**: timeline in the incident channel/doc.

## Flow
1. Declare early (cheap to downgrade); create channel/bridge via tooling.
2. Assess impact; set severity.
3. **Mitigate first** (rollback, failover, feature flag off, scale) - root cause later.
4. Communicate: what's affected, what we're doing, next update time.
5. Hand over explicitly on long incidents (state, hypotheses, next steps).
6. Resolve; schedule post-incident review.

## Gotchas
- Too many people debugging without coordination.
- Waiting for certainty before declaring.
- Status page updated late or with jargon.

## Verify
- [ ] Time to declare and time to mitigate tracked per incident.
- [ ] Practice incidents run quarterly for new on-callers.
