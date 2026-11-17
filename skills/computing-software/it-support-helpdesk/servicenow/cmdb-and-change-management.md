---
id: computing-software.it-support-helpdesk.servicenow.cmdb-and-change-management
name: cmdb-and-change-management
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, cmdb, configuration-item, ci-relationships, change-management, cab, change-advisory-board, standard-change, normal-change, emergency-change, risk-assessment, change-collision, itil]
level: practitioner
status: draft
description: "Use the CMDB and change management workflow in ServiceNow-style ITSM: CI relationships and impact analysis, CAB process, standard vs normal vs emergency change risk."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# cmdb-and-change-management

Goal: link an incident to the right configuration item for real impact
analysis, and know which change category a fix needs before making it —
this builds on `ticket-lifecycle-and-queue-management` (which covers
incident/request states) into the CMDB and change layer underneath.

## CMDB basics for helpdesk (not CMDB administration)
- A **CI (Configuration Item)** is any tracked component — a server, an
  application, a network device, even a business service. Helpdesk's job
  is usually to *link* tickets to the right CI, not to build the CMDB
  itself, but linking wrong actively corrupts impact analysis for
  everyone downstream.
- **Relationships** (depends on / used by, runs on, contains) are what
  make the CMDB useful beyond a glorified asset list — when an incident
  is logged against "Email Service" and it has a dependency map to
  Exchange servers, a load balancer, and DNS, a tech can check the
  **related CIs' own open incidents/changes** before troubleshooting from
  scratch; a known change to a dependency explains the symptom faster
  than fresh diagnosis.
- Stale CMDB data (a decommissioned server still marked "operational," a
  CI never linked to its real dependencies) is extremely common — treat
  the CMDB as a strong hint, not ground truth, and flag discrepancies
  (there's usually a "CMDB data issue" or similar request category) when
  found rather than silently working around them.

## Change categories and why the category matters
- **Standard change**: pre-approved, repeatable, low-risk, documented
  procedure (e.g. a password reset for a locked service account, adding
  a user to an existing distribution list). No CAB review needed each
  time — that's the entire point of pre-approval; using the standard
  template wrong (applying it to a case that doesn't actually match the
  approved scope) is a process violation even if the individual change
  seems harmless.
- **Normal change**: anything with real risk or novelty, goes through
  assessment and (usually) **CAB (Change Advisory Board)** approval
  before the scheduled implementation window. Needs a risk/impact
  assessment, a backout plan, and a planned implementation
  date/time — missing a backout plan is the most common reason a normal
  change gets bounced back by CAB.
- **Emergency change**: for fixing an active major incident/outage where
  waiting for the normal CAB cycle would cause unacceptable harm — gets
  an expedited approval path (often a smaller emergency-CAB or a single
  authorized approver), but still requires retrospective documentation;
  "we didn't have time to log it properly" is not an acceptable outcome
  even for emergencies, log it during or immediately after.

## Change collision and the change calendar
- Before scheduling or approving a normal change, check the **change
  calendar**/schedule for overlapping changes on related CIs — two teams
  independently patching systems that share a dependency in the same
  maintenance window is how "simple" changes cause unrelated outages;
  this is exactly what CI relationship mapping exists to catch.
- Freeze periods (e.g. no non-emergency changes during a retail peak
  season, financial close, or a known high-traffic event) are usually
  enforced at the change-request level — a normal change submitted
  during a freeze gets rejected or needs special exception approval;
  check the calendar for active freezes before planning implementation
  dates.

## Risk and impact assessment
- Risk is typically scored from a combination of: how many
  users/services are affected (impact), how reversible the change is
  (backout plan quality), and how tested the change is (has it been done
  before, in a lower environment first). A change touching a CI with
  many dependents should automatically be flagged higher risk regardless
  of how "simple" the actual steps are — the blast radius, not the
  effort, drives the category.
- Link the change request to the CIs it touches, not just a free-text
  description — this is what lets the next person's impact analysis
  actually work; a change record with no CI link is close to useless for
  anyone doing collision-checking later.

## Gotchas
- A change marked "Implemented successfully" but never verified against
  actual post-change monitoring/incident volume is an audit gap — closing
  a change record is supposed to include a post-implementation review
  (PIR), at least informally, confirming it achieved the intended outcome
  without a spike in related incidents.
- Helpdesk raising an incident that turns out to actually be an
  unauthorized/undocumented change someone made off-process ("unauthorized
  change") should be flagged as such, not just resolved quietly — this
  is a process/compliance finding, not just a technical fix.

## Verify
- The incident/problem record links to the correct CI (verified by
  checking the CI's own relationship map matches the actual
  infrastructure), and a change made to resolve it has the right
  category, an approved CAB record (or standard-change template
  reference) if required, a backout plan, and a closure note confirming
  post-implementation state.
