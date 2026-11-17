---
id: computing-software.cybersecurity-defensive.identity-access-management.joiner-mover-leaver-process
name: joiner-mover-leaver-process
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [identity-lifecycle, joiner-mover-leaver, jml, hr-driven-provisioning, deprovisioning, access-revocation, birthright-access, offboarding]
level: practitioner
status: draft
description: "Run joiner-mover-leaver identity processes driven by HR data: birthright access, mover access removal, timely leaver deprovisioning and the checks behind them."
sources: ["CIS Controls 5.3 and 6.1-6.2 (disable dormant accounts, establish access granting and revoking processes)", "NIST SP 800-53 AC-2 Account Management", "CSF 2.0 PR.AA-01 and PR.AA-05"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Joiner-mover-leaver process

**Goal:** people get the access their role needs on day one, lose access they no longer need
when they move, and lose all access promptly when they leave.

## Source of truth
HR system (Workday, SuccessFactors, etc.) drives identity: hire, transfer, termination events
feed the IdP/IGA (Entra ID inbound provisioning, Okta HR-as-a-source, SailPoint, Saviynt).
Contractors and vendors need an equivalent sponsor-owned record with an end date.

## Joiner
- Account created from HR record before start date, enabled on start date.
- **Birthright access** by attributes (department, location, job code): email, intranet, role-based groups.
- Additional access by request and approval, not by copying a colleague ("make me like Bob" copies years of accumulated access).
- MFA enrolment at first sign-in with verified identity (temporary access pass handed over in person or via verified channel).

## Mover
- Transfer event triggers recalculation of birthright groups and a **review of non-birthright access**: manager confirms what to keep; default removal after 30 days.
- Privileged access never carries over automatically.

## Leaver
- Termination event disables the account at the end of the last day (immediately for involuntary terminations, coordinated with HR).
- Revoke sessions and tokens (Entra `Revoke-MgUserSignInSession`, Okta clear sessions), disable in SaaS via SCIM, remove from privileged groups, rotate shared secrets they knew, collect devices, wipe or retire mobile devices.
- Mailbox/OneDrive handover to manager per retention policy; delete account after a defined period (e.g. 30-90 days).

## Controls and checks
- Daily reconciliation: HR terminated list vs enabled accounts in IdP and key apps (non-SSO apps are the usual gap).
- Alert on sign-ins by accounts of terminated employees.
- Metrics: time from termination to disablement (target same day), orphaned accounts count.

## Gotchas
- Local accounts in apps without SSO/SCIM are missed by IdP disablement: inventory them.
- Rehires and name changes create duplicate identities; match on immutable employee ID.
- Long-lived API keys and personal access tokens survive account disablement in some SaaS.

## Verify
- [ ] Reconciliation report shows zero enabled accounts for leavers older than 24 hours.
- [ ] Sample of movers shows old-role access removed within 30 days.
