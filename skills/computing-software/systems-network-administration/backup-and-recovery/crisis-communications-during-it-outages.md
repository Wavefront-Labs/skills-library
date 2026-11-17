---
id: computing-software.systems-network-administration.backup-and-recovery.crisis-communications-during-it-outages
name: crisis-communications-during-it-outages
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [crisis-communications, contingency-plan, incident-communications, status-page, stakeholder-notification, business-continuity]
level: practitioner
status: docs-checked
description: "Crisis communications in a major IT outage: audiences, contact lists, a communications lead, pre-approved templates, regular updates and an agreed channel."
sources:
  - https://www.ready.gov/crisis-communications-plan
  - https://sre.google/workbook/incident-response/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crisis communications during an outage

**Goal:** the right people hear accurate, timely updates through channels that still work, and nobody
improvises a public statement.

## Audiences and contacts (Ready.gov)
- Possible audiences: employees, customers, suppliers, management, and government officials and
  regulators. Each has its own information needs: identify each, decide what it needs, and assign
  the person best able to reach it.
- Compile contact details for each audience in advance (organisation, contact name, phone, cell,
  email), keep them accessible during an incident, update them regularly and keep them secured.

## Roles (Google SRE Workbook)
- The Incident Commander (IC) leads the response; the person who declares the incident usually
  becomes the IC. The Operations Lead applies operational tools to mitigate or resolve.
- The Communications Lead (CL) is the public face of the response team, reports to the IC, and:
  gives periodic updates to the response team and stakeholders, manages inquiries, and reports
  accurate information to different audiences (company leaders, affected teams, external customers,
  customers who filed tickets). In a small incident the CL role can fold back into the IC.
- The IC can hand off the role; PagerDuty's example rotated the IC and on-call engineers every four
  hours during an 8+ hour incident.

## Spokesperson and messages (Ready.gov)
- Decide in advance who speaks to the media, and prepare that spokesperson with plain-language
  talking points. Prioritise information requests.
- Keep messages consistent across audiences. Pre-script templates with blanks to fill as facts
  emerge, have the management team approve them, and store them on a remotely accessible server.
- Use a coordinated review and distribution process, since early information may be limited, and
  plan messaging for each phase from response through recovery.
- Communication is two-way: equip and staff a contact centre with scripts and an FAQ so answers are
  consistent, and use existing channels (website, call centre) to push information out.

## Updates and channels (Google SRE Workbook)
- Give regular status updates; without them people assume nothing is being done. Announce when
  the response is called off, or people assume it is still ongoing.
- Prepare a contact list and two or three ready-to-use update templates in advance.
- Agree on the communication channel before an incident and pick one the team already knows.
  Examples in the workbook: an IRC channel or video call as a war room, a shared working document
  when discussion gets dense, and PagerDuty's static conference bridge plus a dedicated Slack
  channel where decisions are made on the call and recorded.
- If corporate email or chat could be down or compromised, plan the alternative channel and a
  status page hosted outside the affected platform (design advice; the cited pages do not say this).

## Verify
- [ ] Contact lists and templates exist, are approved and are reachable without the affected systems.
- [ ] In each exercise, check who sent each update, how often, and that messages used the approval path.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Ready.gov crisis communications plan page and the Google SRE Workbook "Incident Response" chapter. Removed because the cited pages do not state them: the audience/channel/owner table, the 15-30 minute and 1 hour first-notice targets, the 30-60 minute update cadence, the specific holding-statement categories, and the legal approval rule for suspected breaches. The NIST SP 800-34 page was not used and was dropped from sources.
