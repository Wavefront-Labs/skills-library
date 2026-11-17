---
id: computing-software.software-engineering.objective-c.nsdate-calendar
name: nsdate-calendar
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-data, nsdate-calendar]
level: practitioner
status: draft
description: "Do date arithmetic with NSCalendar and NSDateComponents, format dates with NSDateFormatter, ISO 8601 and fixed locales."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NSDate, NSCalendar and formatters
**Goal:** handle dates without time zone and locale bugs.

```objc
NSCalendar *cal = [NSCalendar currentCalendar];
NSDate *tomorrow = [cal dateByAddingUnit:NSCalendarUnitDay value:1 toDate:[NSDate date] options:0];
NSDateComponents *c = [cal components:NSCalendarUnitYear | NSCalendarUnitMonth fromDate:tomorrow];

NSDateFormatter *f = [NSDateFormatter new];
f.locale = [NSLocale localeWithLocaleIdentifier:@"en_US_POSIX"];     // for fixed machine formats
f.dateFormat = @"yyyy-MM-dd'T'HH:mm:ssXXXXX";
f.timeZone = [NSTimeZone timeZoneForSecondsFromGMT:0];
NSString *ui = [NSDateFormatter localizedStringFromDate:d dateStyle:NSDateFormatterMediumStyle timeStyle:NSDateFormatterShortStyle];
NSISO8601DateFormatter *iso = [NSISO8601DateFormatter new];
```
- `NSDate` is an absolute instant (seconds since 2001-01-01 UTC), not a calendar date.
- Use calendar APIs for day/month math; adding `86400` seconds fails across DST.
- Fixed wire formats use `en_US_POSIX`; user-facing text uses styles or `dateFormatFromTemplate:options:locale:`.
- Use `yyyy` not `YYYY` (week-year) in patterns.
- Formatters are expensive to create; cache them (NSDateFormatter is thread-safe for use on modern OS releases per Apple docs).

## Gotchas
- `currentCalendar` follows user settings, which may not be Gregorian.
- Parsing returns nil for mismatched input; check.

## Self-check
Add one day across a DST change and verify the local hour is unchanged.
