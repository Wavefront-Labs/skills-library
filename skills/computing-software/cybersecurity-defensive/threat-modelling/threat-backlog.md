---
id: computing-software.cybersecurity-defensive.threat-modelling.threat-backlog
name: threat-backlog
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-backlog, security-backlog, jira, security-user-stories, threat-modelling, risk-acceptance]
level: practitioner
status: draft
description: "Turn threat model findings into backlog items that get done: ticket format, labels, acceptance criteria, prioritisation, risk acceptance and keeping the model in sync."
sources: ["https://www.threatmodelingmanifesto.org/", "https://owasp.org/www-project-samm/", "https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracking threats in the backlog

A threat model whose mitigations live only in a PDF has no effect. Mitigations must become normal work items
in the team's tracker, prioritised against features.

## Ticket format
- **Title**: action, not threat: "Validate webhook signature on /payments/callback".
- **Threat reference**: threat model ID (e.g. TM-PAY-07), STRIDE category, affected element.
- **Risk**: severity from the model's rating method (e.g. OWASP risk rating High).
- **Acceptance criteria** written as testable statements, ideally referencing ASVS IDs: "Requests with invalid
  or missing signature return 401 and are logged (ASVS 13.x)".
- **Labels**: `security`, `threat-model`, system name; a custom field linking back to the model.

## Prioritisation
- Agree severity-based SLAs with product owners up front (e.g. critical before release, high within two
  sprints, medium within a quarter).
- Design-level mitigations are cheapest before the code exists; flag them as blockers on the related feature
  epic rather than separate debt.
- Bundle small mitigations into the story that touches the same code.

## Risk acceptance
If the team will not fix: record a risk acceptance with the business owner's name, rationale, compensating
controls and an expiry date (e.g. 6-12 months). Expired acceptances reopen automatically.

## Keep model and backlog in sync
- Threat model entries hold the ticket key; tickets hold the model ID. Tools like IriusRisk, Threat Dragon
  exports or as-code models (Threagile, pytm) can generate tickets via API.
- When a ticket closes, update the threat status to mitigated and record the evidence (PR, test).
- Report open threat tickets by severity and age in the team's normal dashboard, not a separate security one.

## Gotchas
- Vague tickets ("improve auth security") rot; one control per ticket.
- Security-only backlogs owned by the security team get ignored; tickets must live in the delivery team's
  backlog.
- Do not lose the "why": link the threat description so later engineers do not undo the control.

## Verify
Every open threat with severity at or above medium has a ticket or a dated risk acceptance, and closed
tickets have evidence linked.
