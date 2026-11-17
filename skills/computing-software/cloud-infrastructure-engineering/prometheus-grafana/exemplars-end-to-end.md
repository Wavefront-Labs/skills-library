---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.exemplars-end-to-end
name: exemplars-end-to-end
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-exemplars, exemplar-storage, exemplar-config, signal-correlation, trace-to-metrics]
level: advanced
status: docs-checked
description: "Exemplars from client to Grafana: OTel exemplar filter, client_golang ExemplarObserver, OpenMetrics handler, Prometheus exemplar-storage flag and buffer, Grafana exemplar view."
sources: ["https://prometheus.io/docs/prometheus/latest/feature_flags/#exemplars-storage", "https://grafana.com/docs/grafana/latest/fundamentals/exemplars/", "https://pkg.go.dev/github.com/prometheus/client_golang/prometheus/promhttp", "https://pkg.go.dev/github.com/prometheus/client_golang/prometheus", "https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exemplars end to end

Grafana's definition: an exemplar is a specific trace representative of a measurement taken in a given time interval; exemplars link metrics (aggregated view) to traces (one request). Every hop below has to carry them.

## 1. Emit (client)
- Go client_golang: a histogram observer implements `prometheus.ExemplarObserver` (`ObserveWithExemplar(value float64, exemplar Labels)`). Counters implement `ExemplarAdder` (`AddWithExemplar`). Put the trace ID in the exemplar labels (conventionally `trace_id`); the label set is limited to 128 runes in total.
- In HTTP middleware, `promhttp.WithExemplarFromContext(fn)` adds exemplars to counters and histograms; if `fn` returns nil labels no exemplar is added and the metric still counts.
- OpenTelemetry metrics SDK: sampling is controlled by an ExemplarFilter (`AlwaysOn`, `AlwaysOff`, `TraceBased`); the spec says the default SHOULD be `TraceBased`, which makes eligible only measurements recorded in the context of a sampled parent span. A sampled-only filter keeps exemplars pointing at traces that were actually kept. The spec also says exemplar sampling SHOULD be on by default and that exemplars carry the trace and span ID of the active span for synchronous instruments.

## 2. Expose (OpenMetrics)
Exemplars are only transmitted via OpenMetrics, so in Go set `EnableOpenMetrics: true` in `promhttp.HandlerOpts` (the scraper must also negotiate an OpenMetrics format).

## 3. Store (Prometheus)
- `--enable-feature=exemplar-storage` enables storing exemplars scraped by Prometheus. The feature-flags page lists it among features that are disabled by default and may change.
- Storage is a fixed-size circular buffer held in memory for all series; the `storage/exemplars` config block sets its size as a number of exemplars. An exemplar with only a `trace_id` takes roughly 100 bytes. With the feature on, exemplars are also appended to the WAL for local persistence (for the WAL duration).

## 4. Show (Grafana)
Exemplars are supported for the Prometheus data source only. After you enable the functionality, exemplar data is available by default (see the Exemplars section in Grafana's Prometheus configuration options). Grafana shows each exemplar as a highlighted star in Explore and in dashboards; hover to see the trace ID, then click the button next to the `traceID` property (for example "Query with Tempo") to open the trace. Exemplars can also be reached from Loki log details by extracting the trace ID with a derived field.

## Debug order
- Is the client emitting? Fetch the endpoint with an OpenMetrics `Accept` header and look for exemplars on histogram or counter lines.
- Is Prometheus storing? Confirm the `exemplar-storage` flag is set.
- Is Grafana's Prometheus data source configured for exemplars and the trace data source?

## Checked
Date: 2026-11-07. Read in full: the Grafana "Introduction to exemplars" page and the Prometheus feature-flags page (Exemplars storage section; other flags skimmed). Read from the OTel metrics SDK spec: the Exemplar, ExemplarFilter, ExemplarReservoir and defaults sections. Read from pkg.go.dev: the promhttp page (`HandlerOpts.EnableOpenMetrics`, `WithExemplarFromContext`) and, by search only (the page is very large), the `ExemplarObserver` entry on the prometheus package page; the 128-rune limit is from the earlier read of that package page for the client-golang skill. Thin skill: removed the Java and Python snippets, the `max_exemplars` key name, the claim that exemplars are not compacted into blocks, `prometheus_tsdb_exemplar_exemplars_appended_total`, `scrape_protocols` defaults, the `send_exemplars` remote-write option and Mimir `max_global_exemplars_per_user`, the `/api/v1/query_exemplars` endpoint, the Grafana `exemplarTraceIdDestinations` provisioning key and Exemplars panel toggle, the OpenMetrics sample line and the "Prometheus 2.x" claim, none of which the fetched pages state. Replaced the client_golang examples_test.go source (it only demonstrates const-histogram exemplars) with the pkg.go.dev pages.
Method: documentation only; no commands were run.
