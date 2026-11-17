---
id: computing-software.data-engineering.kestra.execution-context-variables
name: execution-context-variables
category: computing-software
field: data-engineering
product: kestra
tags: [context, execution, taskrun, trigger-variables, envs, globals, item]
level: practitioner
status: docs-checked
description: "The variables available in Kestra expressions: flow, execution, task, taskrun, trigger, loop item, envs and globals, plus fetchContext() to inspect them."
sources:
  - https://kestra.io/docs/expressions/context
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Inspect the live context with `{{ fetchContext() }}` in Executions, Logs, Debug Expression.

Defaults:

- `flow`: `id`, `namespace`, `revision`, and `tenantId` (Enterprise).
- `execution`: `id`, `startDate`, `state`, `originalId` (kept across replays).
- `task`: `id`, `type`.
- `taskrun`: `id`, `startDate`, `attemptsCount`, `parentId`.
- `parent.outputs`, `parents`, `labels` (by key), `trace.parent` (only when OpenTelemetry tracing is on).

Triggers: Schedule gives `trigger.date`, `trigger.next`, `trigger.previous`. Flow trigger gives `trigger.executionId`, `trigger.namespace`, `trigger.flowId`, `trigger.flowRevision`.

Loop `item`: `item.index` (zero-based), `item.value`, `item.key` (maps), `item.parent.index`/`value`, `item.parents[n].value`.

Environment: `ENV_FOO` is read as `{{ envs.foo }}` (default prefix `ENV_`); `{{ kestra.environment }}`, `{{ kestra.url }}`, `{{ globals.foo }}`.

Also `vars.x`, `inputs.x`, `secret('NAME')`, and Enterprise-only `credential('name')` and `namespace.*` (wrap Pebble-bearing values in `render()`).

Use bracket notation for hyphens: `{{ outputs['second-task'].value }}`.

## Checked

2026-11-04. Confirmed against the Kestra execution context page: default flow, execution, task and taskrun variables, trace.parent, schedule and flow trigger variables, loop item variables, ENV_ prefix with envs, kestra.environment, kestra.url, globals, vars, inputs, secret(), Enterprise credential() and namespace.* with render(), bracket notation for hyphens, fetchContext() in Debug Expression. Nothing removed.

Method: documentation only; no commands were run.
