---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.openmetrics-features
name: openmetrics-features
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, openmetrics, openmetrics-exemplars, openmetrics-created, stateset-info, info-metric, exposition-format, content-negotiation]
level: advanced
status: verified
description: "Use OpenMetrics-only exposition features: exemplars, _created samples, info and stateset types, units and # EOF; plus how Prometheus negotiates the format."
sources: ["https://github.com/prometheus/OpenMetrics/blob/main/specification/OpenMetrics.md", "https://prometheus.io/docs/instrumenting/exposition_formats/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenMetrics-only features

Served with `Content-Type: application/openmetrics-text; version=1.0.0`. Prometheus requests it via
`Accept` (see `scrape_protocols`); client libraries switch format based on that header.

```
# TYPE http_requests counter
# HELP http_requests Requests.
http_requests_total{code="200"} 1027 # {trace_id="4bf92f3577b34da6"} 1 1697440000.123
http_requests_created{code="200"} 1697400000.0
# TYPE build info
build_info{version="1.4.2",revision="abc123"} 1
# TYPE feature_flags stateset
feature_flags{feature_flags="new_checkout"} 1
feature_flags{feature_flags="dark_mode"} 0
# TYPE queue_age_seconds gaugehistogram
# UNIT queue_age_seconds seconds
queue_age_seconds_bucket{le="10.0"} 3
queue_age_seconds_bucket{le="+Inf"} 4
queue_age_seconds_gcount 4
queue_age_seconds_gsum 55.0
# EOF
```

## Features
- **# UNIT**: optional metadata line; the unit must be the suffix of the family name (`queue_age_seconds` / `seconds`).
  `# UNIT http_requests_seconds s` under family `http_requests` is rejected by the reference parser.
- **Exemplars**: `# {labels} value [timestamp]` after a counter or bucket sample; label set <= 128 UTF-8
  chars. Prometheus stores them only with `--enable-feature=exemplar-storage`.
- **_created**: creation time of counters/histograms/summaries; lets the backend know when counting
  started (used by created-timestamp zero ingestion).
- **info** type: `_info` suffix, value always 1, carries metadata labels for joins (`group_left`).
- **stateset** type: one series per state, value 1 for the active state(s); good for enums.
- **gaugehistogram** type for distributions that can go down (queue item ages); samples are `_bucket`, `_gcount`, `_gsum`.
- **counter** samples must end in `_total`; family name in `# TYPE` omits it.
- **# EOF** terminator is mandatory; truncated responses are detected.

## Prometheus specifics
- `info` and `stateset` series are ingested as ordinary series with value 1/0; the type is kept for the metadata API (`/api/v1/metadata` reported `stateset` and `info`, with the family name `build` for `build_info`).
- The classic text format has no exemplars and no `_created`; if your library emits exemplars but the scrape
  uses `text/plain`, they are silently lost.

## Verify
- [ ] `curl -H 'Accept: application/openmetrics-text' http://app:8080/metrics | tail -1` prints `# EOF`.
- [ ] Exemplars visible via `/api/v1/query_exemplars?query=http_requests_total` (empty unless started with `--enable-feature=exemplar-storage`).

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), prometheus_client 0.26.0 on Python 3.14, client_golang 1.25.0 on Go 1.26.
- Reference parser: prometheus_client's OpenMetrics parser accepted the corrected sample block (counter with exemplar and `_created`, info, stateset, gaugehistogram with unit) and rejected a unit that did not match the family name (`Unit does not match metric name`) and a body without `# EOF` (`Missing # EOF at end`).
- Exemplar limit of 128 UTF-8 code points, `_gcount`/`_gsum`, 'unit must be a suffix of the family name': OpenMetrics specification (prometheus/OpenMetrics, specification/OpenMetrics.md).
- Prometheus 3.15.1 scraping a prometheus_client target: `/api/v1/metadata` returned type `stateset` for `feature_flags` and `info` for `build`; `build_info{version="1.4.2"}` stored as value 1; `query_exemplars` returned exemplars with `--enable-feature=exemplar-storage` and none without it.
- `Accept` header from Prometheus and `# EOF` check: see `exposition-content-negotiation`.
