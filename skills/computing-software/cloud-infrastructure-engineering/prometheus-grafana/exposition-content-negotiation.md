---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.exposition-content-negotiation
name: exposition-content-negotiation
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [exposition-content-negotiation, accept-header-negotiation, scrape-protocols, openmetrics, protobuf-exposition, exposition-format]
level: advanced
status: verified
description: "How Prometheus negotiates exposition formats with Accept headers (OpenMetrics, text 0.0.4/1.0.0, protobuf), testing with curl and fixing bad Content-Type."
sources: ["https://prometheus.io/docs/instrumenting/content_negotiation/", "https://prometheus.io/docs/instrumenting/exposition_formats/", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exposition content negotiation

Prometheus builds an `Accept` header from the job's `scrape_protocols` list (in preference order) and the target answers with one format and a `Content-Type`.

## Formats and media types
| scrape_protocols value | Content-Type |
|---|---|
| `PrometheusProto` | `application/vnd.google.protobuf;proto=io.prometheus.client.MetricFamily;encoding=delimited` |
| `OpenMetricsText1.0.0` | `application/openmetrics-text;version=1.0.0` |
| `OpenMetricsText0.0.1` | `application/openmetrics-text;version=0.0.1` |
| `PrometheusText1.0.0` | `text/plain;version=1.0.0` (UTF-8 names) |
| `PrometheusText0.0.4` | `text/plain;version=0.0.4` |
Protobuf is first in the default list when `scrape_native_histograms` is true (needed to receive native histograms); with it false the default order starts with `OpenMetricsText1.0.0`.

## Testing a target
```bash
curl -s -D- -o /dev/null -H 'Accept: application/openmetrics-text;version=1.0.0' http://target:8080/metrics | grep -i content-type
curl -s -H 'Accept: application/openmetrics-text;version=1.0.0' http://target:8080/metrics | tail -1   # must be "# EOF"
```
Prometheus 3.15.1 sent, with default settings: `application/openmetrics-text;version=1.0.0;escaping=allow-utf-8;q=0.7,application/openmetrics-text;version=0.0.1;q=0.6,text/plain;version=1.0.0;escaping=allow-utf-8;q=0.5,text/plain;version=0.0.4;q=0.4,*/*;q=0.3`; with `scrape_native_histograms: true` the protobuf entry is first (`q=0.7`); with `scrape_protocols: [PrometheusText0.0.4]` it sent `text/plain;version=0.0.4;q=0.7,*/*;q=0.6`.

## Fixing bad targets
- A missing or unsupported `Content-Type` fails the scrape in Prometheus 3: the target error was `non-compliant scrape target sending blank Content-Type and no fallback_scrape_protocol specified for target` for a blank header and `received unsupported Content-Type "application/octet-stream" and no fallback_scrape_protocol specified for target` for the other. Fix the exporter, or set per job:
```yaml
fallback_scrape_protocol: PrometheusText0.0.4
```
- Force a protocol for a job: `scrape_protocols: [PrometheusText0.0.4]`.

## Gotchas
- OpenMetrics requires `# EOF` and `_total` counter naming; a hand-written exporter claiming OpenMetrics but missing EOF fails the scrape with `data does not end with # EOF`.
- Proxies and API gateways that rewrite `Content-Type` (e.g. to `application/octet-stream`) break scrapes.
- Exemplars are only transmitted in OpenMetrics/protobuf, not classic text. `_created` is part of OpenMetrics; the Python client also writes it into classic text as a separate gauge series.

## Verify
- [ ] Targets page shows no content-type errors; `scrape_body_size_bytes` is present if `extra_scrape_metrics: true` is set (the `extra-scrape-metrics` feature flag is deprecated in 3.15).
- [ ] `promtool check metrics` passes on the target's output.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), prometheus_client 0.26.0 on Python 3.14, client_golang 1.25.0 on Go 1.26.
- Accept headers and failure messages: Prometheus 3.15.1 scraping a small Python HTTP server that logged the request header and returned blank, octet-stream and OpenMetrics-without-EOF responses; `fallback_scrape_protocol: PrometheusText0.0.4` made the blank and octet-stream targets `up`.
- Table of protocols and MIME types, escaping parameter and the 'highest q wins / fallback / PrometheusText0.0.4 last resort' rule: prometheus.io content-negotiation spec (source in prometheus/docs).
- Go client_golang 1.25.0 answered the protobuf Accept with `application/vnd.google.protobuf; proto=io.prometheus.client.MetricFamily; encoding=delimited; escaping=underscores`.
- prometheus_client 0.26.0: OpenMetrics output ends with `# EOF`; classic text output includes `*_created` gauges and no exemplars.
- `extra_scrape_metrics` and the deprecation note: 3.15 configuration and feature-flag pages; `scrape_body_size_bytes`/`scrape_sample_limit`/`scrape_timeout_seconds` series appeared with the option on.
