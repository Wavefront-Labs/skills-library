---
id: computing-software.it-support-helpdesk.servicenow.logging-incidents-and-outage-records
name: logging-incidents-and-outage-records
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, incident-logging, outage-record, affected-ci, incident-management, mass-impact, channels]
level: practitioner
status: gated
description: "Log incidents consistently from phone, email, chat, portal and monitoring events, set the CI and affected CIs, and record mass-impact outages with linked incidents."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/incident-management/concept/c_IncidentManagementProcess.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-operations-management/page/product/event-management/concept/c_EM.html"
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-foundation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# logging-incidents-and-outage-records

A ticket is only as useful as what was captured at logging. Every channel should land
the same minimum data, so reports, SLAs and problem trends work regardless of source.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Minimum data at logging (all channels)
| Field | Why |
|---|---|
| Caller (validated, not "service desk") | Contact, VIP flag, location, entitlement |
| Channel (`contact_type`) | Phone, email, self-service, chat, walk-in, event |
| Short description: symptom + scope | "Outlook won't open for one user" beats "email issue" |
| Category / subcategory | Routing and trend reporting |
| Configuration item | The service or device actually failing |
| Impact + urgency (priority computed) | Never set priority directly if the matrix exists |
| Assignment group | First owner, even if it is you |

## Channel specifics
- **Phone / walk-in**: log while talking; read the short description back to the caller.
- **Email**: inbound actions create the incident; the agent fixes caller, category and CI
  during triage instead of trusting the subject line.
- **Chat / virtual agent**: the conversation transcript attaches; summarise it in the
  description so nobody has to read 80 lines.
- **Events**: Event Management raises alerts and auto-creates incidents via alert rules;
  the CI comes from the binding, caller is a system account. Check for duplicates before
  working an event incident.

## Configuration item vs affected CIs
- **Configuration item** (`cmdb_ci`): the single CI the fault is on (e.g. the laptop, or
  the "Email" business service). Pick the most specific CI you can confirm.
- **Affected CIs** related list (`task_ci`): every other CI impacted, used for impact
  analysis and change collision. Add them when one fault touches many services (e.g. a
  database server behind three applications).
- **Impacted services** are calculated from the CI relationships when the CMDB is healthy;
  when it is not, add the services manually rather than leaving it blank.

## Outage records
When a service is degraded or down for many users, record an **outage** (`cmdb_ci_outage`)
against the business service: type (outage, degradation, planned), begin and end times,
and the task it came from. Outages drive availability reporting and the service status
page; the major incident is the work record, the outage is the availability record.
1. Create the parent incident (major incident if criteria are met).
2. From the parent, create the outage with the actual begin time (first reported or first
   alert, not when someone noticed).
3. Link every new caller's incident as a child; do not log separate outages per caller.
4. On restoration set the outage end time; children resolve with the parent.

## Pitfalls
- "Service desk" or the agent as caller destroys user-impact reports.
- Priority set to P1 by an angry caller with no matrix check inflates major-incident load.
- Outage end time left open makes availability for the month look terrible.

## Verify
A random sample of tickets from each channel has caller, CI, category and impact filled;
last month's outages all have end times and linked incidents.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
