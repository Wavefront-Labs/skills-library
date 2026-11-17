---
id: computing-software.data-engineering.prefect.automations-actions
name: automations-actions
category: computing-software
field: data-engineering
product: prefect
tags: [automations, actions, jinja, triggers, notifications]
level: practitioner
status: docs-checked
description: "Prefect automations: trigger kinds, action type strings, selected versus inferred targets, Jinja notification variables and event tracing."
sources:
  - https://docs.prefect.io/v3/concepts/automations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: wire a trigger to an action.

Triggers: flow run state change (flow run tags evaluated with OR only), work pool status, work queue status, deployment status, metric thresholds (average duration, lateness, completion percentage), custom event triggers, absence of an expected event (proactive), and webhooks on Prefect Cloud.

Action type strings: `cancel-flow-run`, `delete-flow-run`, `change-flow-run-state`, `suspend-flow-run`, `resume-flow-run`, `run-deployment`, `pause-deployment`, `resume-deployment`, `pause-work-pool`, `resume-work-pool`, `pause-work-queue`, `resume-work-queue`, `pause-automation`, `resume-automation`, `send-notification`, `call-webhook`. Cloud only: `send-email-notification`, `declare-incident`.

Targets: Selected (you pick the object) or Inferred (deduced from the trigger, such as the flow run that fired it; not always possible).

Notifications use any block that can send messages (Slack, Microsoft Teams, email). Jinja variables: `flow_run`, `flow`, `deployment`, `work_queue`, `work_pool` (each with `id`, `created`, `updated`), `flow_run|ui_url`, `automation`, `event`, and `flow_run_log_summary` (Cloud only).

```
Flow run {{ flow_run.name }} entered state {{ flow_run.state.name }}.
{{ flow_run | tojson(indent=2) }}
```

Tracing events: `prefect.automation.triggered`, `prefect.automation.resolved`, `prefect.automation.action.triggered`, `prefect.automation.action.executed`, `prefect.automation.action.failed`.

## Checked

2026-11-09. Confirmed: Automations page (docs.prefect.io/v3/concepts/automations): trigger list, action type table with Cloud-only actions, selected and inferred targets, tracing event names, flow_run_log_summary as Cloud-only. Nothing removed.

Method: documentation only; no commands were run.
