---
id: computing-software.software-engineering.dart.dart-datetime-intl
name: dart-datetime-intl
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-date-time, datetime-intl]
level: practitioner
status: docs-checked
description: "Use DateTime in UTC for storage and day arithmetic, Duration for differences and intl DateFormat for display."
sources: ["https://dart.dev/libraries/dart-core", "https://pub.dev/packages/intl"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DateTime, Duration, time zones and intl formatting
- A `DateTime` is a point in time whose zone is either UTC or the local zone (core Dart has no named time zones). Create with `DateTime.now()`, `DateTime.utc(2000)`, `DateTime.fromMillisecondsSinceEpoch(ms, isUtc: true)`, or `DateTime.parse('2000-01-01T00:00:00Z')` (ISO 8601, here in UTC); `copyWith` adjusts selected fields. `millisecondsSinceEpoch` counts from 1970-01-01 UTC.
- `add(Duration(days: 366))`, `subtract(...)` and `difference` (a `Duration`, `inDays` etc.) work, but shifting by days can misbehave across DST clock shifts: use UTC dates if you must shift days. DateTime operations may give unexpected results around DST and other non-standard time adjustments.
- Formatting comes from `package:intl`: `DateFormat.yMd('ar')`, `DateFormat('EEEEE', 'en_US').format(d)`, `DateFormat.jm().format(DateTime.now())`; formats can be built from ICU/CLDR skeletons or explicit patterns, and `DateFormat` can also `parse`.
- Locale data needs async initialisation before formatting for a locale: `initializeDateFormatting('de_DE', null).then(formatDates);`. The package has one global `defaultLocale`; pass a locale per format or use `Intl.withLocale` to override for one operation.

Verify: test around DST changes using UTC values.

## Checked

Checked 2026-11-08 against the "Dates and times" section of https://dart.dev/libraries/dart-core and the intl package page on pub.dev (current locale, number and date formatting sections). Removed (not confirmed): the `toUtc()` and `isUtc` mentions, `package:timezone`, the claim that `inDays` truncates, and the `'yyyy-MM-dd HH:mm'` pattern example.

Method: documentation only; no commands were run.
