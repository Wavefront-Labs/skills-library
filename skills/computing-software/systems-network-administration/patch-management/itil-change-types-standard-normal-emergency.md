---
id: computing-software.systems-network-administration.patch-management.itil-change-types-standard-normal-emergency
name: itil-change-types-standard-normal-emergency
category: computing-software
field: systems-network-administration
product: patch-management
tags: [standard-change, normal-change, emergency-change, change-model, change-enablement, itil-4]
level: practitioner
status: draft
description: "Classify changes as standard, normal or emergency under ITIL 4, define change models, and promote repeatable patching work to pre-authorised standard changes."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-change-enablement
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standard, normal and emergency changes

**Goal:** route each change to the lightest control that keeps risk acceptable, so routine patching flows and risky work gets scrutiny.

## The three types
| Type | Definition | Authorisation | Patching example |
|---|---|---|---|
| Standard | Low risk, well understood, documented procedure, pre-authorised | None per instance; logged | Monthly OS cumulative update to Tier 3 servers via the automated ring process |
| Normal | Needs assessment and authorisation each time; authority depends on risk | Change authority (peer, manager, CAB) | Major version upgrade, first patch of a new platform, firmware on core storage |
| Emergency | Must be implemented as soon as possible (exploitation, outage) | Emergency change authority, expedited; documentation may follow | KEV patch on internet-facing VPN |

## Change models
A **change model** is the predefined path for a class of change: steps, required evidence, authority, and lead time. Typical patching models: "Routine OS patch (standard)", "Application update (normal-low)", "Network OS upgrade (normal-high)", "Emergency security patch".

## Promoting to standard
Criteria a change class must meet:
1. Documented, repeatable procedure (ideally automated) with pre/post checks and rollback.
2. Track record, e.g. at least 5-10 successful implementations with no incidents.
3. Bounded impact (limited scope per execution, redundancy maintained).
4. Approved by the change authority as a standard change template; reviewed periodically.
Any failure of a standard change triggers review of the template.

## Gotchas
- Calling high-risk changes "standard" to dodge review shifts risk; audit standard changes by outcome.
- Too many emergencies indicates a planning or patch-latency problem.

## Verify
Monthly change report shows the mix by type, success rate per model, and standard change templates with their last review date.
