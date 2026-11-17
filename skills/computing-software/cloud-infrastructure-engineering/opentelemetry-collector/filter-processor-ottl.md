---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.filter-processor-ottl
name: filter-processor-ottl
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, processors, filter, ottl, drop, conditions]
level: practitioner
status: docs-checked
description: "Drop unwanted spans, metrics and logs with the filter processor using OTTL conditions."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/filterprocessor/README.md
  - https://opentelemetry.io/docs/collector/transforming-telemetry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The filter processor drops telemetry when any OTTL condition matches; conditions in a list are ORed. Configuration is split by signal with `trace_conditions`, `metric_conditions`, `log_conditions` and `profile_conditions`.

```yaml
processors:
  filter/ottl:
    error_mode: ignore
    trace_conditions:
      - resource.attributes["host.name"] == "localhost"
    log_conditions:
      - IsMatch(log.body, ".*password.*")
      - log.severity_number < SEVERITY_NUMBER_WARN
```

To keep only some services, write the inverse: drop spans where the service name differs from app1, app2 and app3, joined with `and`. The transforming-telemetry page shows this with an older `traces: span:` layout; use the `trace_conditions` form from the README.

Details from the README:

- Trace conditions may use the `resource`, `scope`, `span` and `spanevent` contexts; metrics use `resource`, `scope`, `metric` and `datapoint`; logs use `resource`, `scope` and `log`.
- Evaluation runs from higher to lower levels. A dropped span is never checked for span event conditions, and a condition mixing `resource` and `spanevent` paths is evaluated at the span event level.
- Dropping every datapoint of a metric drops the metric, but dropping every span event leaves the span.
- `error_mode` is `ignore` (log and continue, recommended and the default), `silent`, or `propagate`, which drops the payload.
- Advanced form groups conditions per `context` with their own `error_mode`.

## Checked

Method: docs-checked 2026-11-09 against the filter processor README (read in full) and the transforming-telemetry page (filter section).
