---
id: computing-software.it-support-helpdesk.device-provisioning.hr-driven-provisioning-triggers
name: hr-driven-provisioning-triggers
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, hr-driven-provisioning, inbound-provisioning, workday, successfactors, lifecycle-workflows, joiners-movers-leavers]
level: practitioner
status: draft
description: "Drive account lifecycle from the HR system: Entra inbound provisioning from Workday/SuccessFactors or API, matching and scoping, attribute mappings, pre-hire timing, and logs."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/app-provisioning/plan-cloud-hr-provision"
  - "https://learn.microsoft.com/en-us/entra/identity/app-provisioning/inbound-provisioning-api-concepts"
  - "https://learn.microsoft.com/en-us/entra/id-governance/what-are-lifecycle-workflows"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# hr-driven-provisioning-triggers

## Why
HR is the source of truth for who works here. When HR changes drive account create,
update and disable, joiners get access on day one and leavers lose it on their last day
without a ticket.

## Options
- Entra provisioning apps for **Workday** or **SAP SuccessFactors** to on-prem AD (via the
  provisioning agent) or directly to Entra ID.
- **API-driven inbound provisioning** for any other HR system: the HR export posts SCIM
  bulk requests to the Entra provisioning endpoint.
- Lifecycle Workflows (Entra ID Governance) run tasks relative to `employeeHireDate` and
  `employeeLeaveDateTime`: generate TAP and email the manager before day one, add groups,
  disable and remove licences on leave.

## Design decisions
- **Matching attribute**: `employeeId` (worker ID) links HR record to account; set it
  on existing accounts before go-live or the service creates duplicates.
- **Scoping filters**: which workers to provision (employee types, countries, active
  status).
- **Attribute mappings**: name, UPN generation (with uniqueness expressions), department,
  manager, job title, `accountEnabled` from worker status.
- **Pre-hire window**: create accounts disabled N days before start.

## Operations
- Provisioning logs (Entra > Monitoring > Provisioning logs) show each create/update/skip
  with the reason; quarantine status means repeated failures.
- Test in a sandbox tenant or with a narrow scoping filter first; use "Provision on demand"
  for a single worker.
- Late HR entries are the top cause of "account not ready on day one"; agree an SLA with HR.

## Gotchas
- HR data quality becomes your directory quality (typos in names, missing managers).
- Rehires and conversions (contractor to employee) need explicit handling rules.

## Verify
A test hire flows from HR to an account with correct attributes and groups within the
expected window, and a test termination disables it on the leave date.
