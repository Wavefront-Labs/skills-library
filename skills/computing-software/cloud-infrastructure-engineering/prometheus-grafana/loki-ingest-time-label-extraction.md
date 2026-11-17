---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-ingest-time-label-extraction
name: loki-ingest-time-label-extraction
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [ingest-time-label-extraction, pipeline-label-extraction, loki-labels, loki-process, structured-metadata]
level: practitioner
status: verified
description: "Promote log fields to Loki labels or structured metadata at ingest: Alloy loki.process json/regex/labels stages, Promtail, OTLP resource attribute mapping, and cardinality checks."
sources: ["https://grafana.com/docs/alloy/latest/reference/components/loki/loki.process/", "https://grafana.com/docs/loki/latest/send-data/otel/", "https://grafana.com/docs/loki/latest/get-started/labels/bp-labels/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ingest-time label extraction

Labels define streams and the index; extract only **low-cardinality** fields you select by (level, app, namespace,
cluster). Everything else stays in the line or goes to **structured metadata** (stored per entry, filterable, not indexed).

## Alloy loki.process
```alloy
loki.process "app" {
  stage.json {
    expressions = { level = "level", trace_id = "trace_id", route = "http.route" }
  }
  stage.labels             { values = { level = "" } }              // indexed label
  stage.structured_metadata { values = { trace_id = "" } }          // high cardinality, not indexed
  stage.label_drop         { values = ["filename"] }
  stage.static_labels      { values = { cluster = "prod-eu1" } }
  forward_to = [loki.write.default.receiver]
}
```
Other extractors: `stage.regex { expression = "level=(?P<level>\\w+)" }`, `stage.logfmt`, `stage.cri`, `stage.template`
(normalise values, e.g. lowercase level) and `stage.match { selector = "{app=\"api\"}" ... }` to scope stages.
Promtail uses the same names under `pipeline_stages` (`json`, `labels`, `structured_metadata`).

## OTLP ingestion
Loki 3 maps a default set of **resource attributes** to labels (`service.name` -> `service_name`,
`k8s.namespace.name`, `deployment.environment`, cloud and k8s IDs); everything else becomes structured metadata.
Change per tenant:
```yaml
limits_config:
  otlp_config:
    resource_attributes:
      attributes_config:
        - action: index_label
          attributes: [team]
        - action: drop
          regex: process\..*
    log_attributes:
      - {action: structured_metadata, attributes: [trace_id]}
  discover_log_levels: true      # sets detected_level structured metadata
  discover_service_name: [service, app, application, container]
```

## Cardinality check
- `logcli series '{app="api"}' --analyze-labels` shows label value counts.
- `loki_ingester_memory_streams` per tenant and the `max_global_streams_per_user` limit (default 5000 in Loki 3.7.9).
- Never promote `trace_id`, `user_id`, `pod` IP or `path` to labels.

## Verify
`logcli labels` lists the new label, `logcli labels level` shows a small value set, and structured metadata fields are queryable as `| trace_id="..."` without a parser.

## Checked
Ran Alloy v1.21.1 (`alloy validate` on the block, then `alloy run` tailing a CRI-format file into Loki 3.7.9): `stage.json`, `stage.labels`, `stage.structured_metadata`, `stage.label_drop`, `stage.static_labels`, `stage.template` (ToLower) and `stage.multiline` all behaved as described; `stage.regex`, `stage.logfmt` and `stage.match` validated. `alloy convert --source-format=promtail` converted a `structured_metadata` pipeline stage. The `otlp_config` and `discover_*` YAML loaded with Loki's `-verify-config` and the OTLP mapping was confirmed by a real OTLP push. Docs read: Alloy v1.21.1 loki.process reference (stage list), Loki otel docs.
