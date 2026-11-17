---
id: computing-software.it-support-helpdesk.servicenow.service-desk-telephony-ivr-and-continuity
name: service-desk-telephony-ivr-and-continuity
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, ivr, service-desk-continuity, acd, call-flow, outage-message, business-continuity]
level: practitioner
status: draft
description: "Design service desk IVR and ACD call flows, and keep the desk running during major outages with outage messages, overflow, remote working and fallback ticketing."
sources:
  - "https://learn.microsoft.com/en-us/microsoftteams/plan-auto-attendant-call-queue"
  - "https://docs.aws.amazon.com/connect/latest/adminguide/connect-contact-flows.html"
  - "https://www.thinkhdi.com/certification/support-center-manager"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# service-desk-telephony-ivr-and-continuity

## IVR design for a service desk
- Keep it shallow: greeting, one menu of at most 4-5 options, then queue. Every extra
  layer adds abandonment.
- Put a **dynamic outage message first** ("We know email is down; updates at
  status.example.com") so callers with that issue can hang up.
- Options by need, not org chart: "password or account locked", "new problem", "existing
  ticket", "everything else". Password option can point to SSPR before queueing.
- Collect an ID (employee or ticket number) if the ACD can pass it to the agent screen
  (CTI pop); otherwise don't ask.
- After-hours routing: P1-only option to on-call; everything else to voicemail/portal.

## ACD queue settings
- Routing: longest-idle agent or skills-based; priority boost for VIP lines.
- Queue announcements every 60-90 s with position or estimated wait, and an offer of
  callback after a threshold.
- Overflow: after N minutes or N callers, overflow to a secondary group or vendor.
- Report abandon rate, ASA, and calls per option weekly; prune options nobody picks.
Examples: Teams auto attendant + call queue; Amazon Connect contact flows; Genesys.

## Continuity during major outages
Prepare before you need it:
| Scenario | Fallback |
|---|---|
| ITSM tool down | Shared spreadsheet or form with incident fields; back-enter later |
| Telephony down | Divert number to mobiles; status page and email announcement |
| Office unusable | Agents work from home with softphone; tested quarterly |
| Call surge from outage | Outage IVR message, raise overflow, pause non-urgent work |
| Identity/SSO down | Break-glass accounts for the desk; offline contact list |
- Keep an offline copy of key contacts, escalation lists and the continuity plan.
- During a surge, assign one person to update the IVR message and status page every
  30 minutes.

## Verify
Test the IVR monthly end to end, including after-hours path; the continuity plan has been
exercised in the last 6 months with lessons recorded.
