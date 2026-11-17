---
id: computing-software.it-support-helpdesk.servicenow.ci-relationships-for-impact-analysis
name: ci-relationships-for-impact-analysis
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, cmdb, configuration-item, ci-impact-analysis, dependency-view, service-mapping, business-service, itil-4]
level: practitioner
status: gated
description: "Use CI relationships for impact: dependency views from a failed CI to affected business services, impacted-services on incidents and changes, and fixing missing relationships."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ci-relationships-for-impact-analysis
Goal: when a server, switch or app fails (or is about to be changed), you
can say within minutes which business services and users are affected.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Relationship model
- Business service / application service at the top ("Payroll", "VPN").
- Depends on: application, database, servers, load balancer, network.
- Relationship types matter: `Depends on::Used by`, `Runs on::Runs`,
  `Hosted on::Hosts`. Wrong types break traversal.
- Populate via Service Mapping (top-down from an entry point URL), via
  Discovery (bottom-up), or manually for small estates.

## Doing impact analysis
- On the CI form open **Dependency Views** (map icon): shows upstream
  services; filter by relationship depth.
- On an incident set the CI; the **Impacted Services/CIs** related list
  is filled (via the "Impacted services" business rule / BSM). Use it to
  set impact and to decide whether this is a major incident.
- On a change, **Refresh impacted services** to see what the change
  touches; the conflict checker and approvers use this.
- For a network device: check which servers/sites hang off it; one access
  switch may be "every desk on floor 3".

## Practical support use
- Five incidents on different laptops with the same "Outlook can't connect"
  symptom → check the email service map for a common upstream CI.
- Before rebooting a server for a user, check what else runs on it.

## Fixing missing relationships
- If impact shows nothing for a known-critical CI, raise a CMDB task to
  the service owner; agents should not draw relationships ad hoc.
- Reconcile Service Mapping and manual relationships; duplicates double-
  count impact.

## Gotchas
- Dependency views over large maps are slow and noisy; limit depth to 2-3.
- Shared infrastructure (domain controllers, DNS) relates to everything;
  impact shows "all services", which is true but not actionable — use
  service-level monitoring to confirm actual user impact.

## Verify
Selecting a production server's CI on a test incident lists the business
services it supports, matching what the service owner expects.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
