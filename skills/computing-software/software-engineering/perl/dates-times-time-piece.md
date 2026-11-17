---
id: computing-software.software-engineering.perl.dates-times-time-piece
name: dates-times-time-piece
category: computing-software
field: software-engineering
product: perl
tags: [perl, time-piece, datetime-module, strftime, time-zones, dates-times-time-piece]
level: practitioner
status: docs-checked
description: "Parse, format and compute dates with Time::Piece (core), DateTime and POSIX::strftime, including time zones, strptime pitfalls and month arithmetic."
sources: ["https://perldoc.perl.org/Time::Piece", "https://metacpan.org/pod/DateTime", "https://perldoc.perl.org/POSIX"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dates and times with Time::Piece, DateTime and POSIX

**Goal:** correct time arithmetic and formatting.

```perl
use Time::Piece; use Time::Seconds;
my $t = localtime;                                  # object (replaces localtime in scalar context); gmtime too
say $t->ymd, ' ', $t->hms, ' ', $t->strftime('%Y-%m-%dT%H:%M:%S');
my $p = Time::Piece->strptime('2026-11-02 10:30', '%Y-%m-%d %H:%M');   # class method: GMT object
my $later = $p + ONE_DAY * 3;  my $diff = ($later - $p)->days;          # difference is a Time::Seconds
use POSIX qw(strftime floor);  my $s = strftime('%a %b %e %Y', localtime);

use DateTime;                                       # CPAN: named time zones
my $dt = DateTime->new(year => 2026, month => 11, day => 2, hour => 9, time_zone => 'Australia/Sydney');
my $later_dt = $dt->clone->add(months => 1);        # the DateTime docs clone before add_duration
$dt->clone->set_time_zone('UTC');
my $dur = $dt2->delta_days($dt);  DateTime->now(time_zone => 'UTC')->iso8601;
```

## Time::Piece facts (perldoc)
- `mon` is 1 = January, `_mon` is 0 = January; `year` is the full year, `_year` is year minus 1900; `wday` is 1 = Sunday, `_wday` and `day_of_week` are 0 = Sunday; `yday` is 0 = Jan 01.
- `$t->datetime` gives ISO 8601 without a zone (`2000-02-29T12:34:56`).
- `strptime` called as a class method returns a GMT object. For a local object use `localtime()->strptime(...)` or `strptime($s, $f, { islocal => 1 })` (the `islocal` and `defaults` options need Time::Piece 1.37).
- `%z` parsing (numeric offsets, applied to convert to UTC) was added in 1.38 and the docs call it "somewhat alpha". `%Z` only recognises `GMT` and `UTC` (case-sensitive); other zone names are parsed and ignored, and the docs advise DateTime beyond GMT/UTC.
- `strptime` parses English day and month names unless you call `Time::Piece->use_locale()` (a global change). `%f` is parse-only; `%c`, `%x`, `%X` are unsupported.
- Arithmetic uses epoch seconds. `add_months` / `add_years` keep the day-of-month number, so Jan 31 + 1 month = Mar 3, and they preserve wall-clock time across DST. Subtracting across a DST change may differ from wall-clock expectation.
- `strftime` calls the platform's `strftime`, so some flags (`%e %k %l %P %s %u %V %z %Z` and others) vary by platform.
- Perl before 5.12 lacks times beyond 2^31 seconds, so Time::Piece fails past 2038 there; DateTime does not.

## DateTime facts (metacpan)
- Named zones: pass `time_zone => 'America/Chicago'` etc.; `floating` and `UTC` also exist. A good way to avoid ambiguous local times is to construct in UTC and call `set_time_zone`.
- Stringification uses the object's formatter, defaulting to `iso8601` (which has no zone).
- For calendar-day differences use `delta_days` or `delta_md`; they ignore the time zone and avoid DST complications. `subtract_datetime_absolute` gives seconds and nanoseconds.
- Adding months at month end uses an `end_of_month` algorithm: `wrap` (default for positive durations: 2010-08-31 + 1 month = 2010-10-01), `limit` (2010-01-30 + 1 month = 2010-02-28) or `preserve` (default for negative durations).

## Rules
- Store timestamps as UTC epoch seconds or ISO 8601 with `Z`; convert at the edges.
- Core `localtime`/`gmtime` in list context return `($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)`.
- Do not subtract 86400 to get "yesterday" across DST changes; use calendar arithmetic.

## Self-check
- [ ] `perl -MTime::Piece -e 'print Time::Piece->strptime("2026-01-31","%Y-%m-%d")->ymd'` prints `2026-01-31`.

## Checked
Confirmed on perldoc Time::Piece (accessors, strptime behaviour and version notes, arithmetic and DST, add_months, strftime caveats, 2038 note), metacpan DateTime (time zones, iso8601 stringification, delta_days, end_of_month algorithms, clone with add_duration) and perldoc POSIX (`strftime`, `floor` exist).
Removed: Time::Local, Time::HiRes, Time::Moment and Date::Calc advice, the DateTime::Format::Strptime example, and the Time::Piece "ignores %z in some versions" wording (replaced by the version note above).
Method: docs-only read of cited pages, 2026-11-08
