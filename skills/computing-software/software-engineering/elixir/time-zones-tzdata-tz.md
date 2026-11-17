---
id: computing-software.software-engineering.elixir.time-zones-tzdata-tz
name: time-zones-tzdata-tz
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, time-zone, tzdata, tz, timezone-database, shift-zone, dst, time-zone-database, time-zones]
level: advanced
status: docs-checked
description: "Configure a time zone database (tzdata or tz) so shift_zone and DateTime.new with named zones work, and handle DST gaps and ambiguity."
sources: ["https://hexdocs.pm/elixir/DateTime.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time zones with a time zone database

**Goal:** convert instants to local wall-clock time reliably.

```elixir
# add the chosen library to mix.exs deps first (time_zone_info, tz, tzdata or zoneinfo), then either:
# config/config.exs
config :elixir, :time_zone_database, Tz.TimeZoneDatabase     # name comes from the library's install docs
# or at runtime
Calendar.put_time_zone_database(Tz.TimeZoneDatabase)

new_york = DateTime.from_naive!(~N[2023-06-26T09:30:00], "America/New_York")
utc = DateTime.shift_zone!(new_york, "Etc/UTC")      # ~U[2023-06-26 13:30:00Z]
DateTime.shift_zone!(utc, "Europe/Paris")            # 15:30:00+02:00 CEST

case DateTime.from_naive(naive, "America/New_York") do
  {:ok, dt} -> dt
  {:gap, just_before, just_after} -> just_after          # wall-clock time does not exist
  {:ambiguous, first_dt, second_dt} -> first_dt          # wall-clock time happens twice
  {:error, reason} -> {:error, reason}
end
```

## Rules
- The default database is `Calendar.UTCOnlyTimeZoneDatabase`: it handles only "Etc/UTC" and returns `{:error, :utc_only_time_zone_database}` for any other zone. Add a database library and configure it (the DateTime docs list time_zone_info, tz, tzdata and zoneinfo, the last recommended for embedded devices). Use the module name given in that library's installation instructions.
- A time zone database records UTC offsets used in the past, present and expected future. Because those plans change, it needs periodic updates.
- A future DateTime is only a snapshot of current zone rules: rules may change before the event happens. Past datetimes are unaffected. For future events, store the naive local time and the zone name and recompute, rather than only a derived UTC instant.
- With daylight saving time there is an hour that does not exist (clocks forward) and an hour that happens twice (clocks back); `DateTime.new/4` and `from_naive/3` return `{:gap, ...}` and `{:ambiguous, ...}` for those, and applications must handle both and tell users.
- `DateTime.add/4` with a day unit may land in a gap or overlap; to surface conflicts, add to a `NaiveDateTime` and then call `DateTime.from_naive/2`.
- Avoid building the `DateTime` struct directly.

## Self-check
Convert the same UTC instant to "Asia/Tokyo" and "Europe/London" with `shift_zone!/2` and compare offsets.

## Checked

Checked 2026-11-09 against the DateTime module page on hexdocs.pm (Elixir v1.20.5 pages): "Time zone database", "Datetimes as snapshots", "Converting between timezones", `from_naive/3` return types, `add/4`.
Confirmed: the default UTC-only database and its error, the list of database libraries, both configuration forms, snapshot semantics, gap/ambiguous returns, the add-then-`from_naive` approach, and the shift examples.
Removed as unconfirmed: the tzdata and tz library pages (not read), tzdata runtime autoupdate and release storage notes, library version pins, and the specific New York gap/overlap dates.

Method: documentation only; no commands were run.
