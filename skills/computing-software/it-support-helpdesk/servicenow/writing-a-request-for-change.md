---
id: computing-software.it-support-helpdesk.servicenow.writing-a-request-for-change
name: writing-a-request-for-change
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, change-management, change-enablement, request-for-change, rfc, change-risk, normal-change, itil-4, change-risk-assessment]
level: practitioner
status: draft
description: "Write an RFC a CAB can approve first time: scope, business reason, risk and impact, test evidence, implementation steps, backout and comms, filled in ServiceNow Change."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# writing-a-request-for-change
Goal: a request for change (RFC) that an approver can judge in two minutes
and an implementer can execute without phoning the author.

## Pick the right change model first
- **Standard**: pre-approved, low-risk, repeatable (e.g. add a printer queue
  from the approved template). Use the standard change template; no CAB.
- **Normal**: everything else; goes through risk assessment and approval.
- **Emergency**: restoring service now; approved by the ECAB after the fact
  within the agreed window, linked to the incident that justified it.
Raising a normal change as emergency to skip CAB is the commonest abuse;
change managers audit emergency rate monthly.

## The fields that matter (ServiceNow `change_request`)
- **Short description**: verb + object + where: "Upgrade VPN concentrator
  firmware 9.18 to 9.20 on vpn-fw-01/02".
- **Justification**: the business reason and what happens if not done
  (vendor CVE, end of support date, incident/problem number).
- **Configuration item**: the actual CI, so impacted services and
  conflicts are calculated (see ci-impact-analysis skill).
- **Implementation plan**: numbered steps with owner and expected duration;
  include pre-checks ("confirm last backup < 24h").
- **Risk and impact analysis**: answer the risk assessment questionnaire
  honestly; state user impact in plain words ("VPN users disconnected for
  ~10 minutes per node; nodes done one at a time").
- **Backout plan**: trigger, steps and time needed (see backout-plan skill).
- **Test plan**: what proves success after the change and who checks.
- **Planned start/end**: inside an approved maintenance window; the
  conflict checker flags blackout or overlapping changes on the same CI.

## Before submitting
- Run **Conflict detection** (Conflicts tab) and resolve or justify.
- Attach evidence: lab test output, vendor release notes, peer review.
- Name the communications: who is told, when, which channel (link the
  outage notification draft).

## Gotchas
- "Low risk" with no test evidence gets rejected; show the test.
- Implementation window shorter than implementation + verification +
  backout time means you cannot back out inside the window.
- Bundling unrelated work into one RFC hides risk; one change per
  logical unit that can be backed out alone.

## Verify
A colleague who did not write it can read the RFC and say what will be
done, by whom, when, what users will notice, and how to undo it.
