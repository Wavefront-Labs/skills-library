---
id: computing-software.data-engineering.kestra.triggers-overview
name: triggers-overview
category: computing-software
field: data-engineering
product: kestra
tags: [triggers, when, allowconcurrent, stopafter, failontriggererror, trigger-variables]
level: practitioner
status: docs-checked
description: "Kestra trigger types and shared properties: disabled, allowConcurrent, when guards, stopAfter, failOnTriggerError, and the trigger context variables."
sources:
  - https://kestra.io/docs/workflow-components/triggers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Core triggers: Schedule, Flow, Webhook, Polling, Realtime, MCP Tool. Plugins add more (S3, SQS, Kafka).

Common properties: `id`, `type`, `description`, `disabled`, `allowConcurrent`, `when` (Pebble that must be true), `workerSelector` (Enterprise).

```yaml
triggers:
  - id: schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 * * *"
    when: "{{ not isWeekend(trigger.date) }}"
```

The `conditions` list is removed in Kestra 2.0 and flows still using it fail to parse. Use `when` (all triggers) or `dependsOn` (Flow trigger).

- Each trigger allows one active execution by default; manual executions are exempt.
- `stopAfter` lists states that disable the trigger; re-enable it manually.
- A failed trigger creates no execution by default; `failOnTriggerError: true` produces a `FAILED` one.
- `{{ trigger._context.id }}` and `{{ trigger._context.type }}` identify the trigger on any type.

Caveats:

- Variables like `trigger.date` error on manual runs.
- Unlocking a trigger may create duplicate executions.
- Deleting a trigger removes its stored state (lock, next evaluation date, backfill).
- Flow and Webhook triggers do not appear in the Triggers tab.

## Checked

2026-11-04. Confirmed against "Start Flows Automatically with Scheduled, Event, and Webhook Triggers" (workflow-components/triggers): six core trigger types, common properties table, when and dependsOn, conditions removal in Kestra 2.0, trigger._context variables, concurrency default and manual-run exemption, stopAfter behaviour, failOnTriggerError, unlock and delete trigger behaviour, Triggers tab visibility. No claims removed.
Method: documentation only; no commands were run.
