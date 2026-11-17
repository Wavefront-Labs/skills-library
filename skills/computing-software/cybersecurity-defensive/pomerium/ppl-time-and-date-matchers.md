---
id: computing-software.cybersecurity-defensive.pomerium.ppl-time-and-date-matchers
name: ppl-time-and-date-matchers
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [time-of-day, day-of-week, date-matcher, timezone, schedule-policy]
level: practitioner
status: docs-checked
description: "Restrict Pomerium access by date, day of week and time of day using the PPL matchers, with timezone and format rules."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/ppl.mdx
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/native-ssh-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `date`, `day_of_week` and `time_of_day` criteria are available in Zero or Enterprise.

**Day of week matcher**: a string. `*` matches all days, commas list days, dashes give ranges. Full names or three-letter abbreviations work, e.g. `tue-fri`.

**Date matcher**: keys `after` and `before` with ISO-8601 values.

**Time of day matcher**: keys `timezone` (required), `after` and `before`.
- Prefer city names like `America/Phoenix` over abbreviations.
- Accepted time formats: "3:04 PM", "3:04PM", "3 PM", "3PM", "15:04:05.999999999", "15:04:05", "15:04".

These criteria also work on SSH routes in Enterprise.

Deny takes precedence over allow, so put exclusions in a `deny` rule.

## Checked

2026-11-04. Read the Pomerium Policy Language page and the Native SSH Access page: tier availability, day of week syntax, date operators, time of day timezone rule and formats, and SSH support all confirmed. Removed an unsupported suggestion of typical use patterns.

Method: documentation only; no commands were run.
