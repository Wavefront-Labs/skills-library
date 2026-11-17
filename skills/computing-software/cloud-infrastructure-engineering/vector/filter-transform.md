---
id: computing-software.cloud-infrastructure-engineering.vector.filter-transform
name: filter-transform
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [filter, transform, conditions, vrl, datadog-search, drop-events, vector]
level: intro
status: docs-checked
description: "Drop events that fail a condition using the filter transform and its condition syntaxes."
sources:
  - https://vector.dev/docs/reference/configuration/transforms/filter/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `filter` transform forwards an event if its condition matches and drops it otherwise. It is stable, stateless and accepts logs, metrics and traces.

```yaml
transforms:
  drop_noise:
    type: filter
    inputs: [logs]
    condition: '.status_code != 200 && !includes(["info", "debug"], .severity)'
```

The `condition` is required and can be written in several syntaxes via `type`:

- `vrl`: a VRL boolean expression (the default; a bare string is shorthand, `condition: ".status == 500"`).
- `datadog_search`: a Datadog Search query string such as `*stack`.
- `is_log`, `is_metric`, `is_trace`: match by event type.

Long form:

```yaml
condition:
  type: vrl
  source: ".status == 500"
```

Behaviour notes:

- Dropping is intentional, so with end-to-end acknowledgements a filtered event still counts as delivered and the source is not told to retry.
- A VRL condition must evaluate to a boolean, and fallible functions must be handled just as in `remap`. Prefer `exists(.field) &&` guards before comparing a field that may be missing.
- The `measure_cpu_usage` option (default false) adds CPU metrics for the transform.

To keep rather than discard the rejected events, use `route` so each branch has an output.

Verify with a `vector test` that uses `no_outputs_from` for an event that should be dropped.

## Checked

2026-11-03. Read transforms/filter and architecture/end-to-end-acknowledgements. Confirmed: stable, stateless, logs, metrics and traces; the condition syntaxes (`vrl` shorthand, `datadog_search`, `is_log`, `is_metric`, `is_trace`); `measure_cpu_usage` default false; and that a filtered event counts as delivered. Nothing removed.

Method: documentation only; no commands were run.
