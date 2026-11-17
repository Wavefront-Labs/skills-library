---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-correlations-editor
name: grafana-correlations-editor
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [correlations-editor, correlation-transformations, grafana-correlations, signal-correlation, data-links]
level: advanced
status: gated
description: "Configure Grafana Correlations: source and target data sources, target queries with variables, regex/logfmt transformations, and provisioning correlations as code."
sources: ["https://grafana.com/docs/grafana/latest/administration/correlations/", "https://grafana.com/docs/grafana/latest/administration/correlations/create-a-new-correlation/", "https://grafana.com/docs/grafana/latest/administration/correlations/use-variables-and-transformations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana Correlations

Correlations (Administration -> Plugins and data -> Correlations; UI path not clicked here) (gated: unconfirmed, source is paywalled or blocked) define links from fields in results of a
**source** data source to a query in a **target** data source. They show as links in Explore and
generalise data-source-specific features like derived fields.

## Create
1. Label and description.
2. Target: data source and query, using `${field}` variables from the source row, e.g. Loki target
   `{app="${app}"} |= "${traceId}"`, or Prometheus `rate(http_requests_total{pod="${pod}"}[5m])`.
3. Source: data source and **results field** the link attaches to (e.g. `pod`).
4. Optional transformations to extract variables from a field.

## Transformations
- `regex`: `{type: regex, field: message, expression: "orderId=(\\w+)", mapValue: orderId}` -> `${orderId}` (stored through provisioning with the expression kept as `pod=(\\S+)`).
- `logfmt`: parses `key=value` pairs from a field and exposes each key as a variable (not run here) (gated: unconfirmed, source is paywalled or blocked).
If any variable used in the target query is missing on a row, the link is not shown for that row.

## Provisioning (`provisioning/datasources/*.yaml`, inside the source data source)
Escape every `${...}` as `$${...}` in these files: Grafana substitutes environment variables when it reads the YAML, and an unescaped `${pod}` in the target query was stored as an empty string (`{pod=""}`) on Grafana 13.2.4.
```yaml
datasources:
  - name: Loki
    type: loki
    uid: loki
    correlations:
      - targetUID: prometheus
        label: Pod CPU
        description: CPU for this pod
        config:
          type: query
          field: pod
          target:
            expr: sum(rate(container_cpu_usage_seconds_total{pod="$${pod}"}[5m]))
          transformations:
            - {type: regex, field: message, expression: "pod=(\\S+)", mapValue: pod}
```
Correlations also have an HTTP API (`GET /api/datasources/uid/<uid>/correlations` returned the provisioned one with `provisioned: true`, `sourceUID`, `targetUID`, `config.field`, `config.target`, `config.transformations`) for Terraform-like automation
(`grafana_data_source_correlation` is not in all provider versions - check before relying on it; the Terraform provider was not run here) (gated: unconfirmed, source is paywalled or blocked).

## Correlations vs alternatives
- Derived fields (Loki) and trace-to-logs (Tempo) are simpler for the standard logs<->traces jump.
- Data links on panels work on dashboards; correlations target Explore.
- Use correlations for business IDs (order ID in logs -> orders DB query) and cross-source pivots.

## Verify
Run a source query in Explore; the field shows a link icon with your label; clicking it opens the target
pane with variables substituted (the Explore click-through was not run: no Loki here) (gated: unconfirmed, source is paywalled or blocked).

## Checked
Environment: Windows 11, Grafana OSS 13.2.4 local.
- Provisioned the skill's data source YAML with the correlation (the `\\S` escaping kept as in the skill), reloaded via `POST /api/admin/provisioning/datasources/reload`, read the stored correlation from the API: the unescaped `${pod}` came back as `pod=""`; with `$${pod}` it came back as `${pod}`.
- Explore behaviour and Terraform could not run: gated markers, so the skill is `gated`.
