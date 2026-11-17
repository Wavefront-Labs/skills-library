---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.transform-processor-ottl
name: transform-processor-ottl
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, processors, transform, ottl, set, replace-pattern]
level: advanced
status: docs-checked
description: "Modify telemetry with OTTL statements in the transform processor, including conditions and error modes."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md
  - https://opentelemetry.io/docs/collector/transforming-telemetry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The transform processor modifies telemetry with OTTL statements that run in the order written. Each statement can carry a `where` condition. Settings are per signal: `trace_statements`, `metric_statements`, `log_statements`.

```yaml
transform:
  error_mode: ignore
  trace_statements:
    - set(span.status.code, STATUS_CODE_OK) where span.attributes["http.request.status_code"] == 400
    - replace_pattern(span.attributes["process.command_line"], "password\=[^\s]*(\s?)", "password=***")
    - limit(span.attributes, 100, [])
    - truncate_all(span.attributes, 4096)
  log_statements:
    - set(log.severity_text, "FAIL") where log.body == "request failed"
```

Details from the README:

- Path prefixes depend on the signal: traces allow `resource`, `scope`, `span` and `spanevent`; metrics add `datapoint` and `exemplar`; logs allow `log`. You cannot use `span.attributes` under `log_statements`.
- `error_mode` defaults to `ignore`, which logs the error and continues; `silent` skips the log; `propagate` returns the error and drops the payload.
- Advanced config groups statements with an explicit `context`, `conditions`, a per-group `error_mode` and `shared_cache`.
- Metric helpers include `convert_sum_to_gauge()` and `convert_gauge_to_sum("cumulative", false)`.
- The page warns that advanced transformations may noticeably affect Collector performance.
- The page also shows span names derived from attributes.

## Checked

2026-11-03. Claims were read against these official pages:

- https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/transformprocessor/README.md
- https://opentelemetry.io/docs/collector/transforming-telemetry/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
