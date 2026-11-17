---
id: computing-software.systems-network-administration.nagios-core.oncall-rotation-timeperiods
name: oncall-rotation-timeperiods
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, oncall, on-call-rotation, timeperiod, contact-notification-period, holidays, vacation, alternating-days]
level: practitioner
status: docs-checked
description: "Model on-call rotations in Nagios Core with per-contact timeperiods: weekday/weekend split, alternating days or weeks via skip intervals, and vacation exclusion."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/oncallrotation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-call rotations with timeperiods

Approach: define one timeperiod per admin for their on-call hours, then set each contact's `host_notification_period` and `service_notification_period` to it.

## Scenarios from the docs
1. **Weekdays vs weekends/holidays.** `weekdays` (Mon-Fri 00:00-24:00), `weekends`, `holidays` (dated entries; Easter entries are year-specific and need updating). `john-oncall`: `use weekdays` + `exclude holidays`. `bob-oncall`: `use weekends,holidays`.
2. **Alternating days.** Date entry with step 2: John starts 2016-10-01, Bob 2016-10-02, each `00:00-24:00`.
3. **Alternating weeks.** One 14-day-step entry per weekday; John starts Sunday 2016-07-29 through Saturday 2016-08-04, Bob starts 2016-08-05 through 2016-08-11.
4. **Vacation.** `john-out-of-office` lists days (`day 15`, `day -1`, `january 2`, `june 1 - july 5`, a one-off date range). `john-oncall` is Mon-Fri with `exclude john-out-of-office`; `bob-oncall` is `use john-out-of-office`.

## Caveat
The doc's Scenario 4 example misspells `timeperiod_name`; use the correct key. The page advises erring toward giving someone else more on-call time when unsure.

Syntax: `computing-software.systems-network-administration.nagios-core.timeperiod-definition-syntax`.

## Checked

2026-11-04. Read all four scenarios on the on-call rotation page and confirmed the weekday/weekend/holiday timeperiods, the 'date / 2' and 'date / 14' skip-interval entries with the stated start dates, the vacation timeperiod entries (day 15, day -1, january 2, june 1 - july 5, a dated range), the misspelt timeperod_name in Scenario 4, and the advice to err toward giving someone else more on-call time. Renamed the body 'Method:' lead-in to 'Approach:' so it is not confused with the checked line.

Method: documentation only; no commands were run.
