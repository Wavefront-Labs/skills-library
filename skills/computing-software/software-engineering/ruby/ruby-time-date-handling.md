---
id: computing-software.software-engineering.ruby.ruby-time-date-handling
name: ruby-time-date-handling
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, time-date-handling, time]
level: practitioner
status: docs-checked
description: "Parse, format and compare Time and Date in Ruby with explicit offsets, strftime, iso8601 and monotonic clocks."
sources: ["https://docs.ruby-lang.org/en/master/Time.html", "https://docs.ruby-lang.org/en/master/Date.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time, Date and time zones

```ruby
require "time"; require "date"
t = Time.now.utc                       # explicit UTC
Time.iso8601("2026-11-03T09:00:00+10:00")
t.iso8601(3)                           # "2026-11-02T23:00:00.123Z"
t.strftime("%Y-%m-%d %H:%M:%S %z")
Time.at(1_700_000_000, in: "+05:30")   # time in a fixed offset
Date.parse("2026-11-03") + 30          # Date arithmetic is in days
Date.today.next_month; Date.valid_date?(2026, 2, 30) # false
(Date.new(2026,12,25) - Date.today).to_i
```
Measure durations with the monotonic clock, not wall time:
```ruby
t0 = Process.clock_gettime(Process::CLOCK_MONOTONIC)
work
elapsed = Process.clock_gettime(Process::CLOCK_MONOTONIC) - t0
```

## Gotchas
- `Time.parse` uses a heuristic (`Date._parse`) to detect the format, and a zone abbreviation it does not recognise is ignored so the time is taken as local. It raises `ArgumentError` when nothing can be extracted. Prefer a fixed format: `Time.iso8601`, `Time.strptime(str, fmt)` or `Date.strptime(str, "%d/%m/%Y")`.
- When the string has no zone, `Time.parse` regards it as local time (or uses its `zone:` argument), so store and exchange UTC or an explicit offset.
- `Time.at(..., in:)` takes offsets such as `"+12:00"`. A named zone (`America/New_York`) needs a timezone object such as one from the TZInfo gem; see the Ruby timezones doc.
- `Time#+` is seconds, `Date#+` is days. The Ruby docs say the `DateTime` class is considered deprecated and to use `Time`.

Verify: print `Time.parse("2026-11-03 10:00").zone` and `Time.parse("2026-11-03 10:00 +10:00").utc_offset`; the first reports the local zone and the second 36000.

## Checked
2026-11-03. Confirmed against ruby/ruby `timev.rb` (`Time.at` `in:` with offsets), `lib/time.rb` (`Time.parse` heuristic, ArgumentError, unrecognised zone treated as local, `iso8601` alias of `xmlschema`), `doc/_timezones.rdoc` (zone objects, TZInfo), `ext/date/date_core.c` (`valid_date?`, `next_month`, "DateTime class is considered deprecated") and `process.c` (`CLOCK_MONOTONIC`). Removed: the "10/11/12" junk claim, the ActiveSupport mention, the TZ environment claim, the DST 86400 claim and the Ruby 3.1 tag.
Method: documentation only; no commands were run.
