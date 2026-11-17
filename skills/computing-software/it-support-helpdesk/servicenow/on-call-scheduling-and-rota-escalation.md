---
id: computing-software.it-support-helpdesk.servicenow.on-call-scheduling-and-rota-escalation
name: on-call-scheduling-and-rota-escalation
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, on-call-scheduling, on-call-rota, escalation-policy, out-of-hours, assignment-group, major-incident]
level: practitioner
status: gated
description: "Set up and run ServiceNow On-Call Scheduling: rotas, rosters, escalation steps and overrides, who-is-on-call lookups, and fixing pages that reach nobody out of hours."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/administer/on-call-scheduling/concept/c_OnCallScheduling.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/administer/on-call-scheduling/concept/escalation-policies.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/administer/on-call-scheduling/task/t_CreateAShiftOverride.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# on-call-scheduling-and-rota-escalation

Out-of-hours P1s fail most often because the rota is wrong, not because the engineer is
slow. On-Call Scheduling (plugin `com.snc.on_call_rotation`) ties a schedule to an
assignment group and pages through an escalation policy.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Model
- **Shift** (formerly rota, `cmn_rota`): coverage window and time zone for a group (e.g.
  weekdays 18:00-08:00 and weekends, Europe/London).
- **Roster** (`cmn_rota_roster`): ordered members who rotate (weekly, daily) within a shift.
  Primary and secondary are separate rosters.
- **Escalation policy/steps**: who to notify, how (email, SMS, voice via Notify), and after
  how many minutes to move to the next step if nobody acknowledges.
- **Overrides / time off**: swaps and cover for one person and a date range.

## Build checklist
1. Group manager owns the schedule; at least 2 people per roster or nobody can take leave.
2. Shift times in the *group's* time zone; check DST transitions (an 08:00 handover can
   leave a one-hour gap or overlap twice a year).
3. Escalation steps: primary (0 min) -> secondary (15 min) -> group manager (30 min) ->
   duty manager (45 min). Require acknowledgement by reply or the mobile app.
4. Members need a working mobile number in `cmn_notif_device` and the right notification
   preferences; test each device.
5. Trigger: assignment of a P1/P2 to the group outside business hours (flow or business
   rule calling the on-call escalation), or the major incident process.

## Desk use
- **Who is on call**: Service Desk > On-Call: Current Schedule, or the on-call widget in
  Agent Workspace. Script: `new OnCallRotation().whoIsOnCall(groupSysId)` returns the
  current on-call users.
- Page through the tool so acknowledgement and escalation are recorded; phoning someone's
  personal mobile from a spreadsheet loses the audit trail.
- If nobody acknowledges within the policy, follow the manual escalation list and record
  each attempt in work notes with times.

## Gotchas
- An empty roster slot (leaver still on it, or new joiner not added) means pages go
  nowhere silently. Monthly check: report shifts whose roster members are inactive users.
- Overrides entered in the wrong time zone shift by hours.
- SMS via email-to-SMS gateways is unreliable; prefer Notify/voice or the Now Mobile app.

## Verify
Create a test P1 assigned to the group out of hours (or use the escalation preview), and
confirm primary is paged, the step escalates after the timeout, and acknowledgement stops it.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
