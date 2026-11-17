---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.runbook-maintenance-and-freshness
name: runbook-maintenance-and-freshness
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [runbook-maintenance, runbook-freshness, runbooks, ownership]
level: practitioner
status: docs-checked
description: "Keep playbooks current: update on every page, expect details to age as fast as production changes, and promote repeated manual steps into automation."
sources: ["https://sre.google/workbook/on-call/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runbook maintenance and freshness

Per the SRE Workbook, details in playbooks go out of date at the same rate as production environment changes: with daily releases, a playbook may need an update on any given day. Writing good documentation is hard, so decide how you will maintain it.

## Practices from the Workbook
- On-call engineers should update the playbook with fresh information when the corresponding page fires.
- Read and update the on-call playbooks as part of preparing a team for on-call (the Workbook's Connection team did this as an onboarding step).
- Keep entries general if your team prefers slow-changing documents (one entry for all "RPC Errors High" alerts, read with an architecture diagram), or step-by-step to reduce human variability and MTTR. If the team disagrees, entries get pulled in different directions, so settle the minimal structured details each entry must have.
- When an entry grows beyond those structured details, pencil in a project to turn the hard-won production knowledge into automation or monitoring consoles. If an entry is a deterministic list of commands run every time an alert fires, implement automation.
- Review each new alert together with its playbook entry; each alert should have a corresponding entry.
- Run "Wheel of Misfortune" exercises, role-playing recent incidents, to share debugging techniques; these exercises exercise the same knowledge the entries hold.

## Verify
- [ ] Each alert has an entry, and the responder updates it after the page fires.

## Checked
Method: docs-checked 2026-11-09 against the SRE Workbook chapter "On-Call" (maintaining playbooks, identification delay, alerting and onboarding sections). The SRE Book "Being On-Call" page and the lychee link checker repo were not used and were dropped. Removed the docs-as-code layout, CI shell checks, last-verified dating, quarterly re-verification and CODEOWNERS advice, none of which are stated on the page read.
