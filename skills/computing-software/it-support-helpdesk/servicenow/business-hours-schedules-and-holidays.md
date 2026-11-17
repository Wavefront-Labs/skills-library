---
id: computing-software.it-support-helpdesk.servicenow.business-hours-schedules-and-holidays
name: business-hours-schedules-and-holidays
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, sla, service-level-management, business-hours-schedule, cmn-schedule, holiday-schedule, timezone, sla-timezone-source, 24x7]
level: practitioner
status: gated
description: "Make SLA clocks follow real support hours: ServiceNow schedules and holiday child schedules, SLA timezone source (caller vs location), 24x7 for P1, and multi-region desks."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://developer.servicenow.com/dev.do"
  - "https://www.axelos.com/certifications/itil-service-management"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# business-hours-schedules-and-holidays

Goal: a ticket logged Friday 17:55 before a bank holiday isn't counted as
breached on Monday morning — unless the agreement says it should be.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Schedules (cmn_schedule)
- Create a schedule per support-hours pattern: e.g. "UK Business 08:00–18:00
  Mon–Fri", "US Eastern 08:00–20:00", "24x7".
- **Schedule entries** define working spans (repeat weekly).
- **Holidays**: a separate schedule of type Exclude (e.g. "UK Bank Holidays
  2026") added as a **child schedule** to the business-hours schedule, so
  holidays are excluded from working time.
- Maintain holiday schedules yearly (put a reminder/change in December).

## Attaching to SLAs
- SLA definition → **Schedule** field (or "schedule source" from a field
  such as the CI's or company's schedule).
- **Timezone source**: caller's timezone, location's timezone, SLA
  definition's timezone, or the instance's — choose deliberately. For a
  London desk serving Singapore users, the desk's hours matter (SLA
  timezone/desk location), not the caller's.
- P1 often 24×7 even if P3/P4 are business hours.

## Multi-region desks
Follow-the-sun: either one 24×5 schedule for global teams, or SLA
definitions per region with region conditions (caller country) and their
own schedules/holidays. Avoid one global calendar of all countries'
holidays (excludes too much).

## Checking
On a task SLA: business elapsed vs actual elapsed; "business duration" is
the schedule-aware figure. Use the SLA timeline to confirm holiday
exclusion worked.

## Gotchas
- Daylight saving: schedules use their timezone; mismatched timezone
  settings produce hour-off breaches twice a year.
- Changing a schedule retroactively affects in-flight SLAs' calculations
  (recalc on update) — announce it.
- Users see due dates in their own timezone in the portal — confusing if
  hours differ; communicate in user time.

## Verify
Test ticket created just before a holiday shows its due time on the next
working day at the right hour; business vs actual elapsed differ as
expected.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, developer.servicenow.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
