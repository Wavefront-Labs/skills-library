---
id: computing-software.it-support-helpdesk.servicenow.raising-and-running-a-problem-record
name: raising-and-running-a-problem-record
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, problem-management, problem-record, problem-states, root-cause-analysis, problem-tasks, fix-in-progress, itil-4]
level: practitioner
status: draft
description: "Run a ServiceNow problem record through its states: logging with impact data, assessing, root cause analysis tasks, fix via change, and keeping linked incidents informed."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# raising-and-running-a-problem-record

Goal: a problem record that moves from "this keeps happening" to a deployed
fix, with an owner and visible progress.

## Raising
From an incident: **Create Problem** (copies short description/CI and links
the incident), or new from the Problem module. Include:
- Clear problem statement (what, where, since when, how often).
- Linked incidents (impact evidence), affected CI/service.
- Business impact estimate.
- Priority (impact × urgency of the problem, not of each incident).

## States (ServiceNow Problem Management, ITIL 4 aligned)
| State | Activities |
|---|---|
| New | logged, awaiting assessment |
| Assess | problem coordinator confirms it's valid, assigns owner/group |
| Root Cause Analysis | investigation; **problem tasks** for parallel work (log collection, vendor case, test) |
| Fix in Progress | cause known; change request raised for the fix; known error/workaround published |
| Resolved | fix deployed; monitoring period |
| Closed | verified no recurrence |
Also: "Accept risk" (closed without fix — business accepts) and "Duplicate".

## Investigation practice
- Timeline + data: when incidents started, changes around then, common
  factors (model, OS build, site, app version).
- Techniques: 5 whys, Kepner-Tregoe is/is-not, fishbone, change
  correlation (see RCA skills).
- Vendor involvement: open a vendor case, record its number, set follow-up
  dates.
- Update the record weekly even if "no progress" — silence reads as
  abandoned.

## Fix
- Raise the change from the problem (related list) so the link is kept.
- After implementation, watch linked incident inflow for an agreed period
  (e.g. 2–4 weeks) before closing.

## Gotchas
- Problems owned by the service desk but needing engineering effort stall —
  owner should be in the team that can fix.
- Incidents shouldn't wait for problem resolution; resolve them with the
  workaround.

## Verify
Problem shows owner, RCA summary, linked change, and post-fix incident
counts; ageing problems reviewed in a monthly problem board.
