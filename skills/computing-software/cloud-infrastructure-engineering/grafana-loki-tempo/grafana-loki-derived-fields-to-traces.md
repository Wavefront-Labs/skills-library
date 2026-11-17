---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.grafana-loki-derived-fields-to-traces
name: grafana-loki-derived-fields-to-traces
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [derived-fields, grafana, loki-datasource, trace-id-regex, internal-link, logs-to-traces]
level: practitioner
status: docs-checked
description: "Configure Loki derived fields so trace IDs in log lines become links into Tempo, with regex or label types, internal links and provisioning."
sources: ["https://grafana.com/docs/grafana/latest/datasources/loki/configure/", "https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/configure-trace-to-logs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: from a log line open the trace.

UI path: Loki data source > Additional settings > Derived fields. Options per field: **Name**, **Type** (**Regex in log line** or **Label**), **Regex** (include a capture group; the first captured group is the value), **Label** (regex matched against label keys, such as `trace[_]?id`, matching indexed, parsed or structured metadata labels), **URL/query** (use `${__value.raw}`), **URL Label** (optional), **Internal link** (pick the target data source), **Open in new tab**, and **Show example log message** to test the regex.

Provisioning (escape `$` as `$$` in YAML):
```yaml
jsonData:
  maxLines: 1000
  derivedFields:
    - datasourceUid: my_tempo_uid        # internal link; must equal the Tempo data source uid
      matcherRegex: "traceID=(\\w+)"
      name: TraceID
      url: '$${__value.raw}'             # interpreted as a query for the data source
      urlDisplayLabel: 'View Trace'
    - matcherRegex: "traceID=(\\w+)"     # external link
      name: TraceID
      url: 'http://localhost:16686/trace/$${__value.raw}'
```
For Tempo the Tempo trace-to-logs page uses Type Regex in log line, an example regex of `trace_id=(\w+)`, Internal link on, and Query `${__value.raw}`. The target data source's `uid` must match `datasourceUid`.

Gotchas
- One value per log line: you cannot combine multiple labels or capture groups into one link.
- The link opens the target data source even if the trace was never ingested (for example, sampled out), and then shows no trace.
- Complex regexes can hurt browser performance on large log volumes.
- Different trace ID field names need separate derived fields; consider OpenTelemetry structured metadata so one Label rule works.
- A provisioned data source is read-only in the UI.

## Verify
In Explore with Loki, expand a log line containing a trace ID; log details show the derived field with a link, and clicking it opens the trace in Tempo.

## Checked
2026-11-03. Confirmed against the Grafana Loki data source configuration page (derived fields table, provisioning and Terraform examples) and the trace-to-logs page. Removed: the YAML `matcherType: label` key (only the UI Type is documented), the draft's regex `trace_?[iI][dD]=(\w+)`, the claim that line_format changes matching, and the per-line performance remark beyond the documented regex warning.
Method: documentation only; no commands were run.
