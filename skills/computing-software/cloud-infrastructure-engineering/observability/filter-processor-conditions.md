---
id: computing-software.cloud-infrastructure-engineering.observability.filter-processor-conditions
name: filter-processor-conditions
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [filter-processor-conditions, drop-spans-ottl, drop-metrics-ottl, transforming-telemetry, otel-collector]
level: practitioner
status: docs-checked
description: "Drop unwanted telemetry with filter processor OTTL conditions: spans, span events, metrics, datapoints and log records, error_mode, orphan risks and verification."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/filterprocessor", "https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filter processor conditions

Each listed OTTL condition is evaluated per item; if **any** is true, the item is **dropped**.

```yaml
processors:
  filter/noise:
    error_mode: ignore
    trace_conditions:
      - span.attributes["http.route"] == "/healthz" or span.attributes["http.route"] == "/readyz"
      - IsMatch(span.name, "^(GET|HEAD) /metrics$")
      - resource.attributes["k8s.namespace.name"] == "kube-system"
      - spanevent.name == "message" and spanevent.attributes["message.type"] == "RECEIVED"
    metric_conditions:
      - metric.name == "go_gc_duration_seconds" or IsMatch(metric.name, "^process_.*")
      - metric.type == METRIC_DATA_TYPE_SUMMARY
      - metric.name == "http.server.request.duration" and datapoint.attributes["http.route"] == "/healthz"
      - HasAttrKeyOnDatapoint("debug.id")
    log_conditions:
      - log.severity_number < SEVERITY_NUMBER_INFO
      - IsMatch(log.body, ".*GET /healthz.*")
```
Contexts per signal: traces `resource`, `scope`, `span`, `spanevent`; metrics `resource`, `scope`, `metric`, `datapoint`;
logs `resource`, `scope`, `log`. The older nested layout (`traces.span`, `metrics.datapoint`, `logs.log_record`) is
deprecated in the README and will be removed; use the `*_conditions` form above. Stability: alpha for traces, metrics and logs.

## Semantics
- Dropping a span does not drop its children: the README warns of orphaned spans if a dropped span is a parent, and of
  orphaned logs that reference a dropped span. Filter every span of an unwanted flow, or sample at trace level instead.
- If all datapoints of a metric are dropped, the metric is dropped. If all span events of a span are dropped, the span is left intact.
- A higher-level match wins: when a span is dropped its span event conditions are not checked. A condition mixing paths
  from several contexts is evaluated at the lowest context it uses.
- `error_mode` values: `ignore` (default, recommended: logs the error and moves to the next condition), `silent` (same
  without logging), `propagate` (returns the error up the pipeline, so the payload is dropped from the collector).

## Useful helpers
`IsMatch` (OTTL), plus the filter processor's `HasAttrKeyOnDatapoint(key)` and `HasAttrOnDatapoint(key, value)`, which
must be used in the `metric` context (string values only for the latter). Conditions combine with `and`, `or` and parentheses.

## Verify
Compare `otelcol_processor_incoming_items` with `otelcol_processor_outgoing_items` (attributes `otel.signal` and
`processor`); the difference is what the filter dropped. Enable debug logging to see OTTL condition evaluation.

## Checked

2026-10-24. OpenTelemetry Collector contrib filter processor README (main branch). Confirmed: OR semantics of conditions, `trace_conditions`/`metric_conditions`/`log_conditions` as the current form with the legacy nested form deprecated, contexts per signal, `error_mode` values and default, datapoint and span event dropping rules, the orphaned telemetry warning, `HasAttrKeyOnDatapoint` and `HasAttrOnDatapoint`, and the incoming/outgoing item metrics.

Method: documentation only; no commands were run.
