---
id: computing-software.systems-network-administration.patch-management.post-implementation-review-emergency-patching
name: post-implementation-review-emergency-patching
category: computing-software
field: systems-network-administration
product: patch-management
tags: [post-implementation-review, pir, emergency-patching, lessons-learned, blameless-review, change-enablement]
level: practitioner
status: draft
description: "Run a post-implementation review after emergency patching: timeline reconstruction, speed and coverage metrics, what broke, root causes and tracked improvements."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-change-enablement
  - https://csrc.nist.gov/pubs/sp/800/61/r3/final
  - https://sre.google/sre-book/postmortem-culture/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-implementation review of emergency patching

**Goal:** make the next emergency faster and safer.

## When
Within one to two weeks after every emergency patch campaign, and after any emergency change that caused an incident.

## Reconstruct the timeline
| Milestone | Timestamp source |
|---|---|
| Vendor release / public disclosure | Advisory |
| Our awareness | Triage log, ticket created |
| Decision to act | Change record |
| Exposure assessed (asset list complete) | Inventory query time |
| First host patched (pilot) | Deployment logs |
| 90% / 100% of in-scope patched | Compliance report |
| Verified by rescan | Scanner |

Derive: time to awareness, to decision, to first deploy, to 90% coverage, to verification.

## Questions
- Did inventory find every affected asset? Which were missed and why?
- What blocked or slowed deployment (approvals, packaging, maintenance windows, owners unreachable)?
- What broke? Was rollback needed and did it work?
- Were mitigations applied where patching lagged?
- Was communication timely and clear?

## Output
Blameless report with root causes and actions, each with owner and due date, tracked to closure in the problem/improvement register. Update runbooks, pre-authorised change models and contact lists.

## Gotchas
- Reviews that produce actions nobody tracks are theatre; review open actions at the next PIR.
- Measure against the previous emergency to show improvement.

## Verify
Actions from the last PIR are closed or in progress, and the speed metrics improve across successive emergencies.
