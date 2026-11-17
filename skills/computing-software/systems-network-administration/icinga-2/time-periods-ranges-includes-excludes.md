---
id: computing-software.systems-network-administration.icinga-2.time-periods-ranges-includes-excludes
name: time-periods-ranges-includes-excludes
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, timeperiod, ranges, excludes, includes, check-period, across-midnight, dst]
level: practitioner
status: docs-checked
description: Define Icinga 2 TimePeriod objects - ranges syntax and precedence, windows across midnight, date spans, includes, excludes, prefer_includes and DST handling.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/08-advanced-topics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# time periods: ranges, includes, excludes
Time periods control when checks run (`check_period`) and notifications go out (`period`, `notification_period` on Notification and User). If unset, `24x7` is assumed. Dependency objects also take `period`.

`ranges` can mix weekdays, month days and dates. Descending precedence: calendar date (2008-01-01), specific month date (January 1st), generic month date (day 15), offset weekday of a month (2nd Tuesday in December), offset weekday (3rd Monday), normal weekday.

Examples:
```
object TimePeriod "workhours" {
  ranges = { "monday" = "09:00-17:00" "tuesday" = "09:00-17:00" }
}
object TimePeriod "do-not-disturb" {
  ranges = { "saturday" = "22:00-06:00" }
}
object TimePeriod "standby" {
  ranges = { "2016-09-30 - 2016-10-30" = "00:00-24:00" }
}
```
Across midnight, the single-range form `22:00-06:00` is said to work starting with v2.11; before, split into two days. Spaces around the dash in a date span are mandatory. Multiple time windows are comma-separated, e.g. `00:00-09:00,18:00-24:00`.

Special dates: `"january 1"`, `"monday -1 may"` (last Monday in May), `"thursday 4 november"`.

`includes` and `excludes` take arrays of period names (e.g. `excludes = [ "holidays", "weekends-excluded" ]`); `prefer_includes` chooses which wins.

Time zone: the OS time zone including DST is used, and times inside a DST change are interpreted as before it. For Europe/Berlin, 02:30 on 2020-10-25 means 02:30 CEST; on 2021-02-28 the nonexistent 02:30 refers to CET and means 03:30 CEST.

## Checked

2026-11-04. Confirmed against the Icinga 2 advanced topics chapter: ranges, across-midnight form since v2.11, mandatory spaces around the dash in date spans, special dates, includes, excludes, prefer_includes and the CEST/CET DST examples.

Method: documentation only; no commands were run.
