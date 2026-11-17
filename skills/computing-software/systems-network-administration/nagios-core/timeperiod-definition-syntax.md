---
id: computing-software.systems-network-administration.nagios-core.timeperiod-definition-syntax
name: timeperiod-definition-syntax
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, timeperiod, define-timeperiod, weekday-directives, date-exceptions, exclude, time-ranges, skip-interval]
level: practitioner
status: docs-checked
description: "Syntax of Nagios Core timeperiod objects: weekday HH:MM-HH:MM ranges, date and day exceptions, skip intervals with /, and exclude."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/objectdefinitions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timeperiod definition syntax

`timeperiod_name` is the short name; `alias` is a longer description.

## Weekdays
`sunday` ... `saturday`, each a comma-separated list of `HH:MM-HH:MM` (24h). `00:15-24:00` is 12:15 AM to midnight. A day left out is excluded entirely.

```
define timeperiod {
    timeperiod_name  nonworkhours
    alias            Non-Work Hours
    sunday           00:00-24:00
    monday           00:00-09:00,17:00-24:00
    saturday         00:00-24:00
}
```

## Exceptions (from the page's examples)
- Calendar date: `1999-01-28`
- Generic day of month: `day 2`
- Nth weekday: `monday 3` (3rd Monday), `friday -2`
- Month day: `february 10`, `february -1` (last day)
- Weekday in month: `thursday -1 november`
- Ranges: `2007-01-01 - 2008-02-01`, `day 20 - -1`, `april 10 - may 15`
- Skip intervals: `day 1 - 15 / 5` (every 5 days)

Time ranges follow each exception, e.g. `2016-10-01 / 2   00:00-24:00`.

## exclude
`exclude other1,other2` removes those periods' ranges.

Precedence between forms is covered in `computing-software.systems-network-administration.nagios-core.timeperiod-usage-precedence`.

## Checked

2026-11-04. Confirmed against the Time Period Definition section of the object definitions page: weekday directives sunday to saturday with HH:MM-HH:MM ranges, 00:15-24:00 example, omitted day excluded, every exception form listed (calendar date, day N, monday 3, february -1, thursday -1 november, ranges, skip intervals with /), and exclude. Removed the 'required' wording, which the text version of the page does not show.

Method: documentation only; no commands were run.
