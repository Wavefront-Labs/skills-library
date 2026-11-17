---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.metric-and-label-name-rules
name: metric-and-label-name-rules
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, label-naming-rules, metric-name-regex, reserved-labels, utf8-metric-names, name-validation-scheme, otlp-translation]
level: practitioner
status: verified
description: "Apply Prometheus metric and label name rules: legacy regexes, reserved __ labels, UTF-8 names in Prometheus 3 (quoting, escaping schemes) and OTel name translation."
sources: ["https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels", "https://prometheus.io/docs/guides/utf8/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#otlp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metric and label name rules

## Legacy rules (still the safe default for compatibility)
- Metric names: `[a-zA-Z_:][a-zA-Z0-9_:]*`. Colons are reserved for recording rules (`level:metric:ops`);
  never use them in instrumentation.
- Label names: `[a-zA-Z_][a-zA-Z0-9_]*`.
- Labels starting with `__` are reserved for internal use (`__name__`, `__address__`, `__meta_*`,
  `__tmp_*` is the convention for your own temporary relabel labels). They are stripped after relabeling.
- Label values: any UTF-8. An empty label value equals the label not existing.

## UTF-8 names (Prometheus 3.x)
Prometheus 3 accepts any UTF-8 metric and label names (`metric_name_validation_scheme: utf8`, the default).
Querying them needs quoting:
```promql
{"http.server.request.duration", "http.route"="/api/v1/orders"}
sum by ("k8s.pod.name") (rate({"http.server.request.duration_count"}[5m]))
```
Content negotiation decides what a scraper receives through the `escaping=` parameter: `allow-utf-8` (names as is),
`underscores` (every non-legacy character becomes `_`, the default when none is sent), `dots` (`.` becomes `_dot_`,
existing `_` becomes `__`) and `values` (`U__` prefix, other characters as hex code points). Older consumers may not
handle UTF-8 names, so check each consumer before relying on them.

## OTLP translation
```yaml
otlp:
  translation_strategy: UnderscoreEscapingWithSuffixes   # default: http.server.request.duration -> http_server_request_duration_seconds
  # NoUTF8EscapingWithSuffixes keeps dots but adds unit/_total suffixes; UnderscoreEscapingWithoutSuffixes escapes but adds no
  # suffixes; NoTranslation (experimental) keeps names as-is
  promote_resource_attributes: [service.name, k8s.namespace.name]
```

## Choosing
- Mixed estate with older Grafana/remote storage: keep legacy names (`underscores` escaping).
- Pure OTel shop on Prometheus 3 + recent Grafana: UTF-8 names avoid double naming, but dashboards and
  alert rules must quote names.

## Verify
- [ ] `promtool check metrics < metrics.txt` reports no naming violations for instrumented services (it flags a missing `_total`
  on counters, camelCase, abbreviated units and a `_total` suffix on non-counters).
- [ ] Dashboards query one consistent naming form per metric.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), prometheus_client 0.26.0 on Python 3.14, client_golang 1.25.0 on Go 1.26.
- UTF-8 names: samples named `http.server.request.duration_count` with label `http.route` and `k8s.pod.name` were accepted by a 3.15.1 receiver; the quoted selector `{"http.server.request.duration_count", "http.route"="/api/v1/orders"}` returned them and the unquoted form failed with a parse error. `metric_name_validation_scheme` default `utf8` and the `otlp` keys come from the 3.15 configuration page.
- Escaping schemes: prometheus.io escaping-schemes spec (source in prometheus/docs).
- OTLP strategies: all four values sent through the 3.15.1 OTLP receiver produced the names described (see `otel-to-prometheus-metric-name-translation`).
- `promtool check metrics` on a file with `badCounter`, a gauge named `http_requests_total` and `lat_ms`: it printed the four violations listed above (exit 3).
- Legacy regexes, reserved `__` labels and the empty-label rule are stated on the Prometheus data-model page; relabeling drops `__tmp_*` labels (seen on live targets in the hashmod test).
