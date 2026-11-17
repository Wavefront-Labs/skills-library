---
id: computing-software.data-engineering.kestra.flow-concurrency-limits
name: flow-concurrency-limits
category: computing-software
field: data-engineering
product: kestra
tags: [concurrency, queue, cancel, fail, allowconcurrent, deadlock]
level: advanced
status: docs-checked
description: "Cap simultaneous Kestra executions with concurrency limit and QUEUE, CANCEL or FAIL behaviour, trigger locking, and the subflow deadlock trap."
sources:
  - https://kestra.io/docs/workflow-components/concurrency
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flow-level limit (open source):

```yaml
concurrency:
  limit: 2
```

Namespace and tenant limits are Enterprise Edition. Evaluation order: flow, then namespaces up to the root, then tenant; the first limit reached decides.

`behavior` (default `QUEUE`):

- `QUEUE`: hold until a slot opens.
- `CANCEL`: mark `CANCELLED` immediately.
- `FAIL`: mark `FAILED` immediately; a trigger with `stopAfter: [FAILED]` is disabled by the first rejection.

Behaviours:

- Executions keep their slot until terminal, including `PAUSED` ones.
- Restarts and replays count.
- Queued time counts toward an SLA `MAX_DURATION`.
- Changing a limit affects new executions only. Removing and re-adding `concurrency` resets the running count to 0.

Triggers: `allowConcurrent` defaults to `false`; the trigger stays locked while an execution runs.

Stuck slots: use Kill, not delete. To reset the count, use the Concurrency Limits page or `PUT /api/v1/{tenant}/concurrency-limit/{namespace}/{flowId}`.

Deadlock: with namespace or tenant limits, `QUEUE` and subflows, a parent with `wait: true` holds its slot while its subflow queues. Prevent by raising the limit, using `FAIL` or `CANCEL`, or setting `wait: false`.

## Checked

2026-11-04. Confirmed against the Kestra concurrency page: concurrency.limit, QUEUE default with CANCEL and FAIL, Enterprise namespace and tenant limits, evaluation order, PAUSED executions keep slots, restarts and replays count, queued time counts toward SLA MAX_DURATION, limit changes and re-adding reset, allowConcurrent default false, Kill rather than delete, PUT concurrency-limit API, subflow deadlock and its fixes. The open-source scope of the flow-level limit is implied by the page marking only namespace and tenant limits as Enterprise.

Method: documentation only; no commands were run.
