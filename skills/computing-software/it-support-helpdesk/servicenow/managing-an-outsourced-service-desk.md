---
id: computing-software.it-support-helpdesk.servicenow.managing-an-outsourced-service-desk
name: managing-an-outsourced-service-desk
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, service-desk-outsourcing, vendor-management, managed-service-provider, contract-kpis, service-credits]
level: practitioner
status: draft
description: "Manage an outsourced service desk provider: contract KPIs, knowledge and access handover, governance meetings, quality sampling, service credits and exit planning."
sources:
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-foundation"
  - "https://www.thinkhdi.com/certification/support-center-manager"
  - "https://www.gov.uk/government/publications/the-sourcing-and-consultancy-playbooks"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# managing-an-outsourced-service-desk

## Contract essentials
- Scope: channels, hours, languages, which ticket types L1 resolves vs escalates, VIP
  handling, out-of-scope list.
- KPIs with definitions: ASA, abandon rate, FCR, SLA attainment, CSAT, quality score,
  reopen rate, KB contribution. Measured from **your** ITSM tool, not their spreadsheet.
- Service credits tied to a few KPIs that matter (not 30); earn-back for sustained
  recovery.
- Security: background checks, access via least privilege, identity verification
  procedure, data residency, right to audit.
- Exit: knowledge, scripts and data ownership remain yours; transition assistance period.

## Onboarding the provider
- Give them the KB, not tribal knowledge: run a knowledge harvest of top contact types.
- Access: named accounts in your ITSM and identity tools with scoped roles; no shared
  admin accounts. MFA mandatory.
- Run in parallel (shadow) for 2-4 weeks before cutover.

## Governance
| Meeting | Cadence | Content |
|---|---|---|
| Operational | Weekly | Backlog, escalations, KB gaps, upcoming changes |
| Service review | Monthly | KPI scorecard, credits, improvement plan |
| Executive | Quarterly | Contract, strategy, risks |

## Quality oversight
- Sample tickets and call recordings yourself monthly (not only their QA).
- Track escalation quality: tickets bounced back for missing info.
- User complaints routed to you as well as them.
- Watch for metric gaming: premature closures, splitting tickets, closing on no reply.

## Pitfalls
- Outsourcing a broken process: the provider inherits bad categorisation and KB.
- No internal owner with time to manage the contract.

## Verify
The monthly scorecard is produced from your system, credits are applied when earned,
and a sample of tickets passes your own quality rubric.
