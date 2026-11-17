---
id: computing-software.devops-ci-cd.renovate.schedule-and-timezone
name: schedule-and-timezone
category: computing-software
field: devops-ci-cd
product: renovate
tags: [schedule, timezone, cron, renovate]
level: practitioner
status: docs-checked
description: "Limit when Renovate may create branches with cron schedules, a timezone, and schedule presets, with the 3-4 hour window rule."
sources:
  - https://docs.renovatebot.com/configuration-options/#schedule
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`schedule` defines when Renovate is allowed to create branches. It does not make Renovate run; it is like a sign saying deliveries are only accepted between 9 and 11. If Renovate rarely runs inside your window, updates get skipped. Allow a window of at least 3-4 hours unless Renovate runs more often than that.

Use Cron syntax. Later syntax is deprecated and no longer supported for config help. The default is "at any time", equal to `* * * * *`.

```json
{
  "timezone": "Europe/London",
  "schedule": ["* 21-23 * * 0"]
}
```

- Prefer a `schedule:` preset when one fits, for example `schedule:automergeDaily`; the docs have a Schedule presets list.
- `timezone` must be an IANA zone name; the default is `null`. Set it only if you use `schedule` and want evaluation in your own zone.
- A schedule can sit on a single `packageRules` entry, so a noisy package gets its own cadence.
- For Cron you must use `*` for the minutes, because minute granularity is not supported, and the schedule must have five parts. Several entries in the array are combined with OR.
- If both day of week and day of month are restricted, both must match: `* * 1-7 * 4` means only the first Thursday of the month.
- Set `updateNotScheduled=false` to stop updates to existing branches outside the schedule, and use `automergeSchedule` to limit when automerge happens.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`schedule`, `timezone`, `updateNotScheduled`, `automergeSchedule`) and the Dependency Dashboard page (`schedule:automergeDaily`). Removed: `schedule:weekly` and `schedule:daily` (presets not on fetched pages), the monthly eslint example, the claim about a separate global schedule, and the default UTC claim (the docs list the default as `null`). The `Europe/London` zone is a placeholder.

Method: documentation only; no commands were run.
