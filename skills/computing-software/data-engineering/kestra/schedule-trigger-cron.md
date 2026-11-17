---
id: computing-software.data-engineering.kestra.schedule-trigger-cron
name: schedule-trigger-cron
category: computing-software
field: data-engineering
product: kestra
tags: [schedule, cron, timezone, when, allowconcurrent, trigger-date]
level: practitioner
status: docs-checked
description: "Configure the Kestra Schedule trigger: cron expressions and shortcuts, timezone, when conditions, no-overlap default, and handling manual runs."
sources:
  - https://kestra.io/docs/workflow-components/triggers/schedule-trigger
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Type `io.kestra.plugin.core.trigger.Schedule`, driven by a `cron` expression.

```yaml
triggers:
  - id: daily
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "@daily"
    timezone: America/New_York
```

Examples: `"*/15 * * * *"` (every 15 minutes), `"0 12 L * *"` (`L` in the day-of-month field is the last day of the month; runs at 12:00 including shorter months). Shortcuts: `@yearly`/`@annually`, `@monthly`, `@weekly`, `@daily`/`@midnight`, `@hourly`.

Refine with a `when` expression:

```yaml
cron: "@hourly"
when: "{{ dayOfWeek(trigger.date) == 'THURSDAY' }}"
```

`{{ trigger.date }}` is the current schedule date. A flow that depends on it cannot be run manually, since it is only available for scheduled runs. This fallback uses the current date when there is no schedule date:

```
{{ trigger.date ?? execution.startDate | date("yyyy-MM-dd") }}
```

Other properties: `inputs` (flow inputs for scheduled runs), `stopAfter` (for example `FAILED`, `KILLED`), `disabled: true`.

Schedules do not overlap by default: `allowConcurrent` is `false` and the trigger stays locked while an execution runs. Set it to `true` to allow overlap.

Keep server and database timezones aligned; otherwise account for Daylight Saving Time.

## Checked

2026-11-04. Confirmed against "Run Flows on a Cron Schedule with Backfills and Conditions" (triggers/schedule-trigger): type, cron shortcuts, timezone example, L day-of-month example, when example, trigger.date and fallback expression, inputs, stopAfter, disabled, allowConcurrent default and lock behaviour, timezone alignment advice. Removed: the "five-field" statement (page does not say it) and the "0 11 * * 1" example without its required when clause.
Method: documentation only; no commands were run.
