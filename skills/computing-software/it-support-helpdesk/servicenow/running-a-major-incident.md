---
id: computing-software.it-support-helpdesk.servicenow.running-a-major-incident
name: running-a-major-incident
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, incident-management, major-incident-procedure, major-incident-manager, bridge-call, incident-commander, parent-incident, communications-cadence, itil-4, major-incident-review]
level: advanced
status: draft
description: "Run a major incident from the service desk: declaration criteria, roles, bridge call, parent incident and child linking, communication cadence, and handover into problem and PIR."
sources:
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.servicenow.com/docs/"
  - "https://response.pagerduty.com/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# running-a-major-incident

Goal: when something big breaks, one person is in charge, the right people
are on a call within minutes, users are told, and nobody fixes it twice.

## Declare
Criteria agreed in advance, e.g. a P1 service down for many users, a VIP
critical system, a security incident with business impact, or a call spike
of N similar tickets in 15 minutes. Any agent can propose; the **major
incident manager (MIM)** on rota declares. ServiceNow: Promote to major
incident (Major Incident Management plugin) or set the MI flag.

## Roles
| Role | Does |
|---|---|
| MIM / incident commander | runs the call, decides, keeps timeline — doesn't troubleshoot |
| Technical lead(s) | diagnose and fix |
| Communications lead | user/stakeholder updates on cadence |
| Service desk lead | links child tickets, updates banner/IVR, feeds symptoms |
| Scribe | timeline in the incident work notes |

## First 15 minutes
1. Open the bridge (Teams/Zoom) and post its link in the incident and the
   on-call channel; page resolver groups.
2. State known facts: symptoms, start time, scope, recent changes (change
   calendar — the most common cause).
3. First user communication (see outage notification skill).
4. Service desk: create/identify the **parent incident**; link incoming
   tickets as **children** (they auto-resolve with the parent); add a
   portal banner and IVR message to cut call volume.

## During
- Cadence: technical check-ins every 15–30 min; user updates at the promised
  times.
- Favour restoring service (rollback, failover, workaround) over finding
  root cause.
- Record decisions and actions with timestamps.
- Escalate to management/vendor per thresholds (time without progress).

## Close
- Confirm restoration with affected users (sample), resolve parent → children
  close with the resolution notes.
- Send resolution communication.
- Open a **problem record**, schedule the **post-incident review** within
  ~5 business days; MIM writes the timeline.

## Gotchas
- Too many people on the bridge talking at once — MIM controls the floor;
  side-channels for deep debugging.
- Don't let the desk keep troubleshooting individual child tickets.
- Forgetting the all-clear keeps calls coming.

## Verify
Time from first call to declaration, to first comms, to restoration are
recorded; children linked; problem and PIR scheduled.
