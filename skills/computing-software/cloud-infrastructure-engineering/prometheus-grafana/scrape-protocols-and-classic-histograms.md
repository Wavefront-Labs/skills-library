---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.scrape-protocols-and-classic-histograms
name: scrape-protocols-and-classic-histograms
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, scrape-config, scrape-protocols-negotiation, scrape-classic-histograms, scrape-protocols, content-negotiation, accept-header, prometheus-proto, openmetrics-1-0, native-histograms, always-scrape-classic-histograms, fallback-scrape-protocol, exposition-format, pca]
level: advanced
status: docs-checked
description: "Control which exposition format Prometheus negotiates (scrape_protocols order), enable native-histogram scraping, and keep classic histograms alongside during migration."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://prometheus.io/docs/prometheus/latest/feature_flags/#native-histograms", "https://prometheus.io/docs/specs/native_histograms/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scrape_protocols and classic histograms

**Goal:** make Prometheus ask targets for the format you want — protobuf when you need
native histograms, OpenMetrics when you need exemplars/`_created`, plain text otherwise —
and avoid losing classic histograms when switching.

## 1. How negotiation works
`scrape_protocols` lists the protocols to negotiate during a scrape, in order of preference. When it is unset
(globally and per job), the order depends on `scrape_native_histograms` (default false):
```yaml
# scrape_native_histograms: false ->
#   [OpenMetricsText1.0.0, OpenMetricsText0.0.1, PrometheusText1.0.0, PrometheusText0.0.4]
# scrape_native_histograms: true  ->
#   [PrometheusProto, OpenMetricsText1.0.0, OpenMetricsText0.0.1, PrometheusText1.0.0, PrometheusText0.0.4]
```
Per-job override:
```yaml
scrape_configs:
  - job_name: app-native-hist
    scrape_protocols: [PrometheusProto, OpenMetricsText1.0.0, PrometheusText0.0.4]
```
Valid values: `PrometheusProto`, `OpenMetricsText0.0.1`, `OpenMetricsText1.0.0`,
`PrometheusText0.0.4`, `PrometheusText1.0.0` (case sensitive). Native histograms need the protobuf exposition
format, so `PrometheusProto` has to be in the list. The native histogram spec notes that text scraping is generally
much less resource demanding than protobuf scraping.

## 2. Native histograms
Two things are needed:
1. `scrape_native_histograms: true` (default false), globally or per scrape config. If false, any native parts of
   a histogram are ignored and only the classic parts are recognized. Setting it to true also puts
   `PrometheusProto` first in the default `scrape_protocols`; if you set `scrape_protocols` yourself, list
   `PrometheusProto` first;
2. the client library configured to expose native histograms.

`histogram_count()` and `histogram_quantile()` work on native histograms (without the special `le` label).

## 3. Keeping classic histograms during migration
When a client exposes **both** representations, `always_scrape_classic_histograms` (default false) makes
Prometheus ingest the classic parts as well as the native histogram. Classic series are suffixed (`_sum`,
`_count`, `_bucket` with `le`), the native histogram is a single series with the unmodified name, so they do not
collide. Keep both while dashboards and rules are migrated:
```yaml
scrape_configs:
  - job_name: app
    always_scrape_classic_histograms: true
```
Then run old (`histogram_quantile(0.9, sum by (le) (rate(x_bucket[5m])))`) and new
(`histogram_quantile(0.9, sum(rate(x[5m])))`) queries side by side, switch, and drop the setting.
`convert_classic_histograms_to_nhcb` (default false) converts scraped classic histograms into native histograms
with custom buckets.

## 4. Fallback for broken targets
`fallback_scrape_protocol` is the protocol to use if a scrape returns a blank, unparsable or otherwise invalid
`Content-Type`. Fix the target, or set it per scrape config:
```yaml
    fallback_scrape_protocol: PrometheusText0.0.4
```

## Gotchas
- Protobuf scraping costs more than text scraping, so list `PrometheusProto` only for jobs that need native histograms.
- Native histograms have no `le` label; `histogram_quantile` handles them without it.
- Exemplars are an OpenMetrics feature; a job pinned to `PrometheusText0.0.4` cannot expose them.

## Checked
2026-10-28. Confirmed on the Prometheus configuration page (`scrape_protocols` values and dynamic defaults,
`scrape_native_histograms`, `convert_classic_histograms_to_nhcb`, `always_scrape_classic_histograms`, `fallback_scrape_protocol`)
and the native histograms specification (protobuf requirement, resource cost note, migration with classic series, `histogram_quantile`
without `le`). Fixed: the documented default protocol lists and the native histogram prerequisite (the current docs enable native
histogram scraping with the configuration option, not a feature flag). Removed: the `q=` weights claim, a curl Accept header,
`/targets` Content-Type claim, `scrape_classic_histograms`, series-halving claim, quoted error texts, global fallback claim,
client_golang option.
Method: documentation only; no commands were run.

## Verify
- [ ] `histogram_count(<native metric>)` returns data for the migrated job.
- [ ] After migration, dropping `always_scrape_classic_histograms` stops ingestion of the classic `_bucket` series.
