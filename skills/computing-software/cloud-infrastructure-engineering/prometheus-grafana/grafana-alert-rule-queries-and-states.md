---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-alert-rule-queries-and-states
name: grafana-alert-rule-queries-and-states
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-alerting, math-expression-usage, resample-expression, reduce-expression, no-data-handling, error-state-handling, multi-dimensional-alerts, alert-instances, grafana-alert-annotations, values-templating]
level: practitioner
status: verified
description: "Build Grafana-managed alert rules: query + Reduce/Math/Resample/Threshold expressions, multi-dimensional instances, No data and Error states, and annotation templates with $values."
sources: ["https://grafana.com/docs/grafana/latest/alerting/fundamentals/alert-rules/queries-conditions/", "https://grafana.com/docs/grafana/latest/alerting/fundamentals/alert-rule-evaluation/state-and-health/", "https://grafana.com/docs/grafana/latest/alerting/alerting-rules/templates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana alert rule queries, expressions and states

## Pipeline
```
A: query  sum by (service) (rate(http_requests_total{code=~"5.."}[5m]))       (range or instant)
B: query  sum by (service) (rate(http_requests_total[5m]))
C: Reduce  A -> Last (mode: Drop non-numeric)        # only needed for range queries
D: Reduce  B -> Last
E: Math    $C / $D                                   # per-series join on identical labels
F: Threshold  E > 0.05                               # the condition
```
- **Reduce**: `Last` and `Max` over a range were run here (other reducers are listed in the Grafana expressions docs); in alert rules the mode must be `dropNN` (Drop non-numeric) or `replaceNN` (Replace non-numeric): `strict` was rejected with `reducer mode 'strict' is not supported. Supported only: [dropNN,replaceNN]`.
- **Math**: `$C / $D` joins series with identical label sets (ran: one result per `service`); `abs($S) > 0.05 && $S < 1000` evaluated and fired.
- **Resample**: align a series to a new interval (`window`, `downsampler`, `upsampler`) before Math between
  sources with different timestamps (e.g. Prometheus vs SQL). When creating the rule through the API give the Resample node its own `relativeTimeRange` (for example `{"from":600,"to":0}`); without it the rule errored with `the series cannot be sampled further; the time range is shorter than the interval`.
- **Threshold**: `gt` and `within_range` ran (`within_range` with params `[5,20]` fired); an optional recovery threshold (`unloadEvaluator`, hysteresis) is accepted only on the expression that is the alert condition (otherwise `recovery threshold 'T' is only allowed to be the alert condition`).
- Prometheus/Loki data sources can do it all in one PromQL query with an instant query + Threshold; prefer that
  (fewer moving parts) unless combining data sources.

## Multi-dimensional rules
Every series reaching the condition is a separate **alert instance** with its own labels and state
(`service="checkout"` firing, `service="search"` normal). One rule covers all services; cap cardinality with
`by (...)` in the query.

## States
Normal -> Pending (for the pending period) -> Alerting -> Recovering (keep firing for) -> Normal. Observed on 13.2.4: with `keep_firing_for: 5m` a condition that went false showed `Recovering` and went back to `Alerting` when the condition returned. Editing the rule resets its state, so a keep-firing test must change the data, not the rule.
Configure per rule:
- **No data** (query returned nothing): API values `NoData` (fires a `DatasourceNoData` alert with a `rulename` label), `Alerting`, `OK` (shown as `Normal (NoData)`), `KeepLast` (`Normal (NoData, KeepLast)`). For ratio rules where no errors means no series, set `OK`.
- **Error / timeout**: `Error` (fires `DatasourceError`, state `Error`), `Alerting`, `OK`, `KeepLast`.
  Keep Last State avoids pages on a transient data source blip. All four values were run for both cases (an unknown data source uid produced the error case).

## Annotations
```
Summary: {{ $labels.service }} 5xx ratio {{ humanizePercentage $values.E.Value }}
Description: errors {{ $values.C.Value | printf "%.1f" }}/s of {{ $values.D }} req/s
```
Both `{{ humanizePercentage $values.E.Value }}` and `{{ $values.E.Value | humanizePercentage }}` rendered (`9.091%`); `$values.D` printed the number. `$value` is a string of all values, e.g. `[ var='C' labels={service=checkout} type='reduce' value=1 ], [ var='D' ... ]`.

## Verify
- [ ] Rule "Preview" shows one row per expected instance with correct state.
- [ ] No-data and error states set deliberately; test by pointing at a stopped source.

## Checked
Environment: Windows 11, Grafana OSS 13.2.4, Prometheus 3.15.1 scraping a local exporter with `http_requests_total` per service.
- Ran the A..F pipeline exactly (range queries, Reduce last with dropNN, Math `$C / $D`, Threshold `gt 0.05`): `checkout` alerting at 9.091%, `search` normal at 0.9901%; annotation templates rendered as quoted.
- Ran Resample, Math with `&&`, `within_range` with a recovery threshold, all four no-data and error handling values, `DatasourceNoData` and `DatasourceError` alerts reaching a webhook, and the Recovering state.
- Everything left in the skill was run or read from the API responses.
