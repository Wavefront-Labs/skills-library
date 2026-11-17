---
id: computing-software.it-support-helpdesk.servicenow.emergency-change-and-ecab
name: emergency-change-and-ecab
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, emergency-change-ecab, emergency-change, ecab, retrospective-change, change-enablement, major-incident]
level: practitioner
status: gated
description: "Raise and run an emergency change: when it qualifies, ECAB approval by phone or chat, retrospective changes after a fix, and the review that follows."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/change-management/concept/c_ITILChangeManagement.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/change-management/concept/emergency-change.html"
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-change-enablement"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# emergency-change-and-ecab

An emergency change is one that must be implemented as soon as possible to restore
service or prevent imminent harm (active exploit, P1 outage). It trades assessment time
for speed, so it needs fast but real authorisation.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Qualifies
- Restoring a P1/P2 major incident where the fix modifies a CI.
- Actively exploited vulnerability with vendor emergency patch.
- Imminent failure (disk array at 98% with growth, certificate expiring in hours).

## Doesn't qualify
- Missed the CAB deadline. Late planning is not an emergency; take the next CAB or a
  documented expedited change if your policy has one.
- A business manager wants a feature today.

## Procedure (ServiceNow emergency model)
1. Create Change > **Emergency**. Minimum fields: CI, justification (link the incident or
   security advisory), implementation steps, backout plan, test/verification, who
   implements.
2. Request approval: the emergency model routes to the **ECAB** approval group (change
   manager + service owner + technical lead on duty). Approval can be given in the tool
   on mobile or by phone/bridge with the change manager recording it in work notes.
3. Implement, verify, record actual start/end.
4. Close with close code and notes; link the incident(s) the change fixed.

## Retrospective (fix already applied)
During a P1 the engineer sometimes changes config to restore service before any record
exists. Policy usually allows it if: the incident commander authorised it, and an
emergency change is raised **within one business day** marked retrospective (many
instances use a checkbox or a "retrospective" type) with exact times and what was changed.

## After every emergency change
- Reviewed at the next CAB: was it truly an emergency, did it work, does it need a
  follow-up normal change to make it permanent or to tidy up?
- Track the ratio of emergency to total changes; a rising trend means planning problems.

## Gotchas
- Backout plans get skipped under pressure; even "revert the config file from backup at
  path X" is enough, but write it.
- Emergency changes still need CI conflict awareness; check the change schedule for
  overlapping work on the same CI.
- An emergency change that fails becomes a new incident; link it as Caused by change.

## Verify
Change record shows ECAB approval (in tool or recorded with name/time), actual times,
linked incident, successful close, and an entry on the next CAB agenda.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
