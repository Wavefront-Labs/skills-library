---
id: computing-software.it-support-helpdesk.servicenow.shift-left-to-l0-and-l1
name: shift-left-to-l0-and-l1
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, service-desk, tiered-support, shift-left, l0-self-service, first-contact-resolution, knowledge-enablement]
level: practitioner
status: draft
description: "Shift work left from L2/L3 to L1 and self-service: pick candidates from escalation data, give L1 knowledge, tools and RBAC, automate L0, and track FCR and escalation rate."
sources:
  - "https://www.thinkhdi.com/"
  - "https://www.serviceinnovation.org/kcs/"
  - "https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# shift-left-to-l0-and-l1
Goal: issues get resolved at the cheapest level that can do it well:
automation (L0), self-service, L1, then specialists only for the rest.

## Find candidates
- Report escalated tickets by category and resolution code for the last
  quarter; sort by volume.
- For each high-volume type ask: is the fix documented? does L1 have the
  permission? is it scriptable?
- Typical wins: BitLocker recovery keys, MFA method reset, group
  membership adds, mailbox permission grants, Intune sync/retire,
  printer mapping, Outlook profile rebuild.

## Enable L1
- **Knowledge**: a tested KB article written by L2 with L1 review.
- **Permissions**: least-privilege roles (Entra Helpdesk Administrator,
  Authentication Administrator, Intune custom role with remote tasks
  only, Exchange recipient management) rather than global admin.
- **Tools**: approved scripts or runbooks behind a button (ServiceNow
  catalog item running Flow/Orchestration, Intune remote actions).
- **Training**: a 30-minute session and shadowing; sign off competence.

## Move to L0
- Self-service catalog items with automated fulfilment (group join with
  owner approval, software install from Company Portal).
- SSPR, virtual agent topics, proactive remediation scripts that fix
  before the user calls.

## Guard rails
- Agree with L2 owners; they keep accountability for the procedure.
- Audit L1 actions (Entra audit logs, Intune audit) for the first month.
- Keep an escalation route when the article does not fit.

## Measure
- Escalation rate per category before/after.
- L1 FCR for the shifted type.
- Reopen rate (premature fixes) and CSAT.

## Verify
For each shifted item: KB article, role/permission granted, trained
agents listed, and escalation rate for that category clearly lower.
