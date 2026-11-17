---
id: computing-software.data-engineering.prefect.event-trigger-fields
name: event-trigger-fields
category: computing-software
field: data-engineering
product: prefect
tags: [triggers, posture, for-each, metric, compound]
level: advanced
status: docs-checked
description: "Prefect event, metric, compound and sequence trigger fields: posture, after, expect, for_each, threshold, within, and matching rules."
sources:
  - https://docs.prefect.io/v3/concepts/event-triggers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write an exact trigger definition.

`type`: `event`, `metric` (Cloud only), `compound`, `sequence`.

Event fields: `match` and `match_related` (object or array; wildcards and negation), `posture` (`Reactive` counts events, `Proactive` watches for absence), `after` and `expect` (string arrays; empty `expect` counts any matched event), `for_each` (labels, evaluated separately per value; supports `related:<role>:<label>`), `threshold` (integer), `within` (seconds; Reactive may be 0, Proactive minimum 10).

```yaml
type: event
posture: Proactive
match:
  prefect.resource.id: prefect.flow-run.*
after: [prefect.flow-run.Running]
expect: [prefect.flow-run.Completed]
for_each: [prefect.resource.id]
threshold: 1
within: 60
```

Metric: `metric.name` (`successes`, `duration`, `lateness`), `operator` (`<`, `<=`, `>`, `>=`), `threshold`, `range` (seconds), `firing_for` (seconds).

Composite: `compound` has `require` (`any`, `all` or a number), `within`, `triggers`; `sequence` needs all children in order. `within: null` means no limit but the key is required.

Rules:
- Labels in one filter are ANDed; values in one label are ORed.
- A `!` pattern cannot share a list with a positive pattern.
- `threshold` above 1 requires `within`.
- Reactive ignores `expect` events arriving before any `after` event.
- Exclusions are reliable only for roles with one related resource.

## Checked

2026-11-09. Read the whole event-triggers page. Confirmed the event, metric, compound and sequence fields, posture and within limits, matching and negation rules, after ordering and the Cloud-only note for metric triggers. Removed nothing.

Method: documentation only; no commands were run.
