---
id: computing-software.software-engineering.nim.times-durations-and-arithmetic
name: times-durations-and-arithmetic
category: computing-software
field: software-engineering
product: nim
tags: [times-durations-and-arithmetic, stdlib-times, duration, timeinterval, initduration, days, months, date-arithmetic, difference, nim]
level: practitioner
status: docs-checked
description: "Add and subtract durations and calendar intervals, compare times, and compute differences and month arithmetic."
sources:
  - https://nim-lang.org/docs/times.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duration, TimeInterval and date arithmetic

Goal: do date math without off-by-one bugs.

- `Duration` is stored as seconds and nanoseconds and is always normalised (`initDuration(hours = 1)` equals `initDuration(minutes = 60)`); a day is exactly 86400 seconds. Use `initDuration(hours=2, minutes=30)`, `d.inSeconds`, `d.inMilliseconds`, `d.toParts`. The docs say to prefer `Duration`, which is faster and easier to understand.
- `TimeInterval` uses calendar units (`initTimeInterval(months=1)`, `1.months`, `3.days`, `2.hours`); its arithmetic can be slow because it needs timezone information, so avoid it unless you need calendar units.
- Across a daylight-saving change, `TimeInterval` says one calendar day has passed while `Duration` says 90000 seconds (25 hours) between 2018-03-25T12:00+02:00 and 2018-03-26T12:00+01:00.
- Helpers: `getDaysInMonth(month, year)`, `isLeapYear`, `getDaysInYear`.


Verify: `getDaysInMonth(mFeb, 2001)` is 28 and `getDaysInMonth(mFeb, 2000)` is 29.

## Checked

2026-11-02. Confirmed against lib/pure/times.nim (module overview on Duration, TimeInterval and day length; `getDaysInMonth` examples). Fixed: `daysInYear` is `getDaysInYear`. Removed: the month-clamping example, `cmp`/`toTime` comparison line, and the UTC-storage and mixed Time/DateTime gotchas.
Method: documentation only; no commands were run.
