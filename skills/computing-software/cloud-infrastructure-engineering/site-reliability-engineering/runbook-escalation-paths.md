---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.runbook-escalation-paths
name: runbook-escalation-paths
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, runbooks, runbook-escalation-paths, escalation-policy, vendor-support, incident-commander]
level: practitioner
status: draft
description: "Write escalation sections in runbooks: when to escalate, to whom (teams, IC, vendors), how to reach them, what information to bring, and keeping contacts current."
sources: ["https://sre.google/sre-book/managing-incidents/", "https://response.pagerduty.com/during/during_an_incident/", "https://sre.google/workbook/on-call/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Runbook escalation paths

**Goal:** responders escalate early to the right people with the right information.

## When to escalate (state explicitly)
- Time-based: not mitigated within N minutes (for example 30 min for SEV2, 15 min for SEV1).
- Scope-based: impact exceeds one service/team, data loss suspected, security involvement.
- Knowledge-based: the runbook's mitigations failed or do not apply.
- Severity upgrade criteria met: declare an incident / page the IC.
Escalating is not failure; the runbook should say so.

## Escalation table
| Situation | Escalate to | How | Bring |
|---|---|---|---|
| Mitigation failed | Service secondary on-call, then team lead | Paging policy `payments-escalation` | Alert, actions tried, current graphs |
| Multi-team or SEV1 | Incident commander rotation | `/incident declare sev1` | Impact summary |
| Database issue | DBA on-call | Paging service `dba` | Query/latency evidence |
| Cloud provider | Provider support (severity A / critical) | Support portal, plan ID, TAM contact | Resource IDs, region, timestamps (UTC), request IDs |
| Third-party API | Vendor status page + support | Contract escalation contacts | Request IDs, error samples |
| Security | Security on-call | Paging `secops`, never only email | Indicators observed |

## Keep current
- Reference paging policies/teams, not personal phone numbers (people change).
- Vendor contract numbers and support plan level recorded and checked quarterly.
- Test escalation paths in drills; dead contacts found in an incident are an action item.

## Verify
- [ ] Each paging alert's runbook has an escalation section with time-based triggers; quarterly contact audit done.
