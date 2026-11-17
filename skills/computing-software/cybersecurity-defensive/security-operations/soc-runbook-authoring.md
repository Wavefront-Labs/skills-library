---
id: computing-software.cybersecurity-defensive.security-operations.soc-runbook-authoring
name: soc-runbook-authoring
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soc-management, runbook-authoring, playbooks, runbooks, standard-operating-procedure, decision-tree, alert-response-guide, soc]
level: practitioner
status: draft
description: "Write SOC runbooks per alert type: purpose, triage questions, queries, decision points, containment actions and closure criteria that a tier-1 analyst can follow."
sources: ["NIST SP 800-61r3 (playbooks and procedures)", "CISA Federal Government Cybersecurity Incident and Vulnerability Response Playbooks", "Palantir Alerting and Detection Strategy framework (response section)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SOC runbook authoring

**Goal:** a consistent, fast, correct response to each alert type regardless of which analyst
is on shift, and a document that improves after every incident.

## One runbook per detection or alert family. Template:
```
Title: Suspicious OAuth consent grant (Entra ID)
Detection IDs: SEN-0123, SEN-0124      ATT&CK: T1528
Purpose: what the alert means and why it matters (2-3 lines)
Severity guidance: default Medium; High if app has Mail.ReadWrite or user is privileged
Triage (answer each, with the query):
  1. Which app, publisher verified?        query: AuditLogs | where OperationName == "Consent to application" ...
  2. Which permissions, delegated or app?  ...
  3. Did the user report a phishing email? ...
Decision points:
  - Publisher verified AND in approved app list -> benign, close with disposition BTP
  - Unverified app with mail or file scopes -> escalate to Tier 2, go to Containment
Containment (pre-authorised):
  - Revoke consent: Remove-MgOauth2PermissionGrant ...; disable the service principal
  - Revoke user sessions
Evidence to attach: grant details, sign-in logs, emails
Closure criteria: disposition set, IOC added, user informed
Owner / last reviewed / changelog
```

## Writing rules
- Every triage question has a ready-to-run query or console path; no "check the logs".
- Decision points are binary and explicit, with the outcome for each branch.
- Containment steps state who is pre-authorised to run them and how to undo them.
- Keep under two screens; link out to deeper references.
- Store runbooks next to detections (same repo, linked IDs) so a detection change prompts a runbook review.

## Lifecycle
- New detection does not go live without a runbook.
- After each true-positive incident, the analyst records what was missing; owner updates within a week.
- Review date on every runbook (e.g. every 6 months); flag stale ones on the SOC dashboard.

## Gotchas
- Runbooks that encode one tool's UI break on the next UI change; prefer queries and APIs.
- Too many branches make a flowchart nobody follows; split into two runbooks.
- SOAR playbooks and runbooks drift apart: generate one from the other or review together.

## Verify
- [ ] A new analyst can work an alert end to end from the runbook in a shadowed session.
- [ ] Each runbook has an owner and a review date within the last 6 months.
