---
id: computing-software.cloud-infrastructure-engineering.aws.ssm-change-calendar-and-change-manager
name: ssm-change-calendar-and-change-manager
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, systems-manager, ssm, change-calendar, change-manager, change-freeze, change-templates]
level: practitioner
status: docs-checked
description: "Enforce change windows and freezes with SSM Change Calendar (open/closed states checked by automation) and note Change Manager's availability change."
sources: ["https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-change-calendar.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/change-calendar-create.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-change-calendar-integration.html", "https://docs.aws.amazon.com/systems-manager/latest/userguide/change-manager-availability-change.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSM Change Calendar and Change Manager

## Change Calendar
A calendar is an SSM document of type `ChangeCalendar` (text format) holding iCalendar 2.0 data. Date and time
ranges in it are called events. A calendar has one of two types:
- `DEFAULT_OPEN`: actions run except during events, when the state is CLOSED (use for freezes: holidays, promotions).
- `DEFAULT_CLOSED`: actions are blocked except during events, when the state is OPEN (use for maintenance windows).

A calendar neither blocks nor allows anything until it has at least one event.
```bash
aws ssm create-document --name prod-freeze --document-type ChangeCalendar \
  --document-format TEXT --content file://freeze.ics
aws ssm get-calendar-state --calendar-names prod-freeze
```
You can also create it in the console and import an `.ics` file exported from Google Calendar, Outlook or iCloud
Calendar. Names can contain letters, numbers, periods, dashes and underscores and cannot be changed later.
`GetCalendarState` returns the current state, the state at a given time, or the next scheduled change; its quota is
10 requests per second.

## Make automation respect it
- Automation: in the Automation console, Preferences, Edit, turn on Change Calendar integration and choose the calendar; principals in the account can then run automations only in allowed periods.
- Change Calendar can also gate Change Manager change requests, maintenance windows and State Manager associations.
- Pipelines and other tooling outside Systems Manager: call `get-calendar-state` in a pre-deploy step and fail on CLOSED.

## Change Manager
Change Manager is closed to new customers from 7 November 2025; existing customers can continue to use it.
AWS recommends AWS Partner Network solutions for enterprise change management. Check status before adopting it.

## Gotchas
- A calendar blocks only tooling that checks it; console changes and Terraform runs ignore it unless your pipeline enforces it.

## Verify
- [ ] `get-calendar-state` returns CLOSED during a test event on a `DEFAULT_OPEN` calendar.
- [ ] A pipeline pre-check fails a deploy during the freeze.

## Checked
2026-10-28. Confirmed in the Systems Manager User Guide pages in `sources` (Change Calendar overview, creating a calendar, Automation change controls, Change Manager availability change); command flags checked with check_commands.
Removed (not confirmed on fetched pages): the State Manager `--calendar-names` association flag, the `aws:assertAwsResourceProperty` runbook step, the sample output, Change Manager template and approval details, delegated administrator, cross-account sharing, time zone and emergency-change notes.
Method: documentation only; no commands were run.
