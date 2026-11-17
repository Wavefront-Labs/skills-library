---
id: computing-software.systems-network-administration.patch-management.writing-a-request-for-change
name: writing-a-request-for-change
category: computing-software
field: systems-network-administration
product: patch-management
tags: [rfc, request-for-change, change-record, backout-plan, implementation-plan, change-enablement]
level: practitioner
status: draft
description: "Write a request for change that gets approved and executed cleanly: scope, justification, step-by-step implementation, test and backout plans with triggers, risk and comms."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-change-enablement
  - https://www.servicenow.com/docs/bundle/xanadu-it-service-management/page/product/change-management/concept/c_ITILChangeManagement.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing a request for change (RFC)

**Goal:** an RFC that a reviewer can approve in one read and an on-call engineer could execute.

## Sections
1. **Summary**: one line, what and where. "Apply October 2026 cumulative update to SQL cluster SQLCLU01 (2 nodes)."
2. **Justification**: why now; link advisories (CVEs, KEV status) or the incident/problem record.
3. **Scope**: exact CIs from the CMDB, services affected, out-of-scope items.
4. **Schedule**: start/end, timezone, inside an approved window; dependencies on other changes.
5. **Implementation plan**: numbered steps with commands or runbook links, owner per step, expected duration.
6. **Test / verification plan**: how success is proven (service checks, synthetic transactions, app owner sign-off).
7. **Backout plan**: steps to restore, time needed, and the **trigger**: a concrete point or condition ("if the cluster role fails to come online within 15 minutes of step 6", "go/no-go at 23:30").
8. **Risk and impact**: risk rating with reasoning, expected user impact (outage, degraded), single points of failure during the change.
9. **Communication**: who is told before, during and after; service desk briefing.
10. **Resources and contacts**: implementer, approver, vendor support case if pre-opened.

## Patch-specific details worth including
Package/KB list and hashes or repository snapshot ID, pre-change backup/snapshot reference, reboot sequence for clusters, monitoring suppression window.

## Style
Write steps in the imperative, include actual hostnames, avoid "etc.", and put anything executed by automation as a job/pipeline link with its version.

## Gotchas
- "Backout: restore from backup" without timing or trigger is not a plan.
- Changes outside window or scope must be re-approved, not improvised.

## Verify
A peer unfamiliar with the system can read the RFC and explain what will happen and when to roll back.
