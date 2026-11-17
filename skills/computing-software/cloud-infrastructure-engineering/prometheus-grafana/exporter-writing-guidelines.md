---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.exporter-writing-guidelines
name: exporter-writing-guidelines
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, exporter-guidelines, exporter-labels-naming, writing-exporters, collect-on-scrape, const-metrics, default-port-allocation]
level: advanced
status: docs-checked
description: "Apply prometheus.io 'Writing exporters' rules: collect on scrape, const metrics, naming and labels, no timestamps, scrape failure reporting, default ports and target params."
sources: ["https://prometheus.io/docs/instrumenting/writing_exporters/", "https://github.com/prometheus/prometheus/wiki/Default-port-allocations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing-exporters guidelines

## Behaviour
- **Collect on scrape**: pull from the application only when Prometheus scrapes; exporters must not scrape on their own timers, so all scrapes are synchronous. In a collector, create new metrics on every scrape (Go: `MustNewConstMetric` in `Collect()`) instead of updating directly instrumented metrics. Reasons given: two scrapes can run at once and direct instrumentation uses effectively global variables (race conditions), and a label value that disappears would still be exported.
- **Caching**: acceptable only for a metric that is particularly expensive to retrieve (more than a minute); note it in the HELP string. Prometheus' default scrape timeout is 10 seconds, so call out in your docs if the exporter can exceed it.
- **Timestamps**: do not set them on exposed metrics; if you think you need them, you probably need the Pushgateway.
- **Failed scrapes**: two patterns. Return a 5xx (users find `up` works as usual, but you cannot tell an exporter that is down from an application that is down), or expose `<exporter>_up` (for example `haproxy_up`) as 0 or 1. The `_up` pattern is better when some useful metrics remain on failure, such as HAProxy exporter process stats.
- **Scrape metadata**: metrics about the scrape (duration, records processed) are gauges prefixed with the exporter name, for example `jmx_scrape_duration_seconds`. Avoid other scrape meta metrics such as a scrape counter or duration histogram: they duplicate Prometheus' own generated metrics and add storage cost. The `process_` and `scrape_` prefixes are reserved.
- **Machine and process metrics** that other tools already provide (CPU, memory, filesystem from the node exporter; JVM stats the Java client includes) should be dropped.
- **Deployment**: one exporter per application instance, preferably beside it, so that service discovery stays in Prometheus. Exceptions: targets you cannot run code beside (SNMP, blackbox, IPMI exporters; Prometheus still does discovery and passes on the target) and "any instance will do" cases such as querying a load-balanced set of replicas. With master election, monitor each instance and handle "masterness" in Prometheus.
- **Pushed sources** (StatsD, Graphite, collectd): decide when to expire metrics (use an expiry time if the source sends one), and rely on raw counters rather than deltas where possible.

## Naming and labels
- Names should let someone who knows Prometheus but not the system guess the meaning; prefix with the exporter or app name (for example `haproxy_up`); use base units and make the unit in the name match (`_seconds`, `_bytes`); expose ratios, not percentages (even better, a counter for each component).
- `snake_case`; only `[a-zA-Z0-9:_]` are valid; no colons (reserved for recording rules); avoid the `_sum`, `_count`, `_bucket` and `_total` suffixes unless producing those types; use `_total` for counters.
- Do not put label names in metric names (`by_type`). For success and failed requests, expose a total metric and a failed metric rather than one metric with a `success`/`failed` label (same for cache hits versus total).
- Labels: avoid `type`, and names that clash with target labels (`region`, `zone`, `cluster`, `env`, `service` and others listed on the page) unless that is what the application calls the thing; avoid `le` and `quantile`; keep read/write and send/receive as separate metrics. A metric should make sense when summed or averaged; never add a `total` label value or an unlabelled total series next to labelled ones.
- Labels every metric would share (software version, region, cluster) do not belong on exporter metrics: use an info-style metric or Prometheus target labels from scrape config.
- Types: match Prometheus types. A "counter" that can be decremented (Dropwizard) is not a counter; the page suggests UNTYPED there. Drop 1m/5m/15m rates, means, min, max and standard deviation from source systems.
- HELP strings: when transforming metrics, include the collector or exporter name, rule ID and original metric details; use one help string per metric name.
- Configuration: the exporter should work with no configuration beyond where the application is; YAML is the standard format.

## Packaging
- Port: pick a free one on the Default port allocations wiki (exporters start at 9100). The wiki asks you not to allocate a port without a public repository or intent to begin work immediately. For internal exporters the page recommends ports outside the allocated range.
- Landing page: a simple HTML page at `/` with the exporter name and a link to `/metrics`.

## Verify
- [ ] Stopping the upstream application yields the failure behaviour you chose (`<exporter>_up` 0, or 5xx).
- [ ] Concurrent scrapes do not share mutable metric state, and metrics for removed label values disappear.
- [ ] Scrape duration stays under the Prometheus scrape timeout (10s default) or is documented.

## Checked
Date: 2026-11-07. Read in full: the prometheus.io "Writing exporters" page. Read the head of the Default port allocations wiki page and searched it for free-port guidance; its port table was not read end to end. Corrections: the draft said to cache after "a few seconds", the page says more than a minute and to note it in HELP; the draft said to always return HTTP 200 on failure, but the page presents 5xx and `_up` as two patterns with trade-offs. Removed as not on the page: `<exporter>_scrape_collector_success` / per-collector duration (a node_exporter convention), the `/probe?target=` path, the `--web.listen-address` / `--web.telemetry-path` / `--web.config.file` flags and exporter-toolkit, the `promtool check metrics` verify, and "put the source field in HELP" as a rule for all exporters (the page says so for transformed metrics).
Method: documentation only; no commands were run.
