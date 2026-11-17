---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-derived-fields-to-traces
name: loki-derived-fields-to-traces
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [loki-derived-fields, derived-field-regex, signal-correlation, data-links, trace-to-logs]
level: practitioner
status: gated
description: "Configure Loki data source derived fields to turn trace IDs in log lines or structured metadata into links to Tempo or external URLs, with regex tests and provisioning."
sources: ["https://grafana.com/docs/grafana/latest/datasources/loki/configure-loki-data-source/", "https://grafana.com/docs/grafana/latest/datasources/loki/#derived-fields"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki derived fields and data links to traces

Derived fields extract a value from each log line (regex) or from a label/structured metadata field and render
it as a link - internal (opens a query in another data source, e.g. Tempo) or external URL.

## Provisioning
```yaml
datasources:
  - name: Loki
    type: loki
    uid: loki
    url: http://loki-gateway
    jsonData:
      derivedFields:
        - name: TraceID
          matcherType: regex                       # regex on the line
          matcherRegex: '"trace_id":"(\w+)"'
          datasourceUid: tempo                      # internal link
          url: '$${__value.raw}'                    # query sent to Tempo ($$ escapes $ in provisioning)
          urlDisplayLabel: View trace
        - name: TraceIDMeta
          matcherType: label                        # from a label or structured metadata
          matcherRegex: trace_id
          datasourceUid: tempo
          url: '$${__value.raw}'
        - name: Ticket
          matcherRegex: 'ticket=(JIRA-\d+)'
          url: 'https://jira.example.com/browse/$${__value.raw}'
```
- Include a capture group in the regex: Grafana uses the first captured group as the value, available as `${__value.raw}` (Grafana Loki data-source docs).
- `matcherType: label` is the right choice when the OTLP endpoint stores `trace_id` as structured
  metadata - no regex over the line needed (provisioning accepted it in Grafana 13.2.4; the UI type is called **Label**).
- In the UI the **Show example log message** box (data-source settings) lets you paste a line and see what each derived field extracts; the docs describe it, it was not driven here (gated: unconfirmed, source is paywalled or blocked).

## Common regexes
- logfmt: `traceID=(\w+)` / `trace_id=(\w+)`
- JSON: `"traceId":"([0-9a-f]{32})"`
- Spring/Logback MDC: `\[\w+,(\w+),\w+\]`

## Gotchas
- `$` must be doubled in provisioning YAML (`$$`) or env-var interpolation eats it.
- Escaping: in YAML single quotes, `\w` is literal; in double quotes it must be `\\w`.
- Where the link renders (Explore, logs panel detail, not a table panel) (gated: unconfirmed, source is paywalled or blocked): no browser session was run.
- If trace IDs are 16 hex chars (Jaeger 64-bit), adjust the regex length.

## Verify
`GET /api/datasources/uid/loki` returns the three `derivedFields` with `url` as `${__value.raw}`; then Explore -> Loki -> expand a log line -> "Fields" shows TraceID with a "View trace" button that opens
the trace in a split pane (gated: unconfirmed, source is paywalled or blocked): the UI step was not run.

## Checked
Ran Grafana 13.2.4 (windows-amd64, own data, log and provisioning directories on localhost port 3300) with the page's provisioning files and read the results back through the HTTP API. Provisioned the page's Loki data source (regex, label and external-URL derived fields) next to a Tempo data source with uid `tempo`: `GET /api/datasources/uid/loki` returned all three fields, `matcherType: label` was accepted, and `$${__value.raw}` was stored as `${__value.raw}` (so the `$$` escape works), while the single-quoted `\w` and `\d` regexes were stored intact. Docs read: Grafana v13.2.4 docs source, datasources/loki/configure (derived-field options, first capture group, **Show example log message**) and administration/provisioning (`$$` escaping). The UI behaviours are gated as marked.
