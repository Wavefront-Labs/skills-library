---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-feature-flags
name: prometheus-feature-flags
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [enable-feature-flags, prometheus-feature-flags, prometheus, command-line-flags, exemplar-storage, native-histograms]
level: practitioner
status: verified
description: "Use Prometheus --enable-feature flags (exemplar storage, memory snapshot, extra scrape metrics, experimental PromQL) with their costs and verification."
sources: ["https://prometheus.io/docs/prometheus/latest/feature_flags/", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/", "https://prometheus.io/docs/prometheus/latest/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus feature flags

Syntax: `--enable-feature=flag1,flag2` (or repeat the flag). Unknown flags only log `Unknown option for --enable-feature` (the server still starts); flags that graduated become logged no-ops (`native-histograms` logged "This option ... is a no-op") and are removed later, so audit them on upgrade. 3.15.1 `--help` lists: concurrent-rule-eval, created-timestamp-zero-ingestion, delayed-compaction, exemplar-storage, extra-scrape-metrics, histograms-st-encoding, memory-snapshot-on-shutdown, metadata-wal-records, old-ui, openmetrics2, otlp-deltatocumulative, otlp-native-delta-ingestion, promql-binop-fill-modifiers, promql-delayed-name-removal, promql-experimental-functions, promql-extended-range-selectors, promql-per-step-stats, search-api, st-storage, st-synthesis, type-and-unit-labels, use-start-timestamps, use-uncached-io, xor2-encoding, zstd-scrape. Check the feature flags page for your exact version.

## Commonly used flags (3.x)
| Flag | What it does | Cost / caveat |
|---|---|---|
| `exemplar-storage` | keeps exemplars in a fixed-size in-memory circular buffer; size set by `storage.exemplars.max_exemplars` in config | memory grows with the buffer size (a per-exemplar byte figure is not in the docs, so none is given) |
| `memory-snapshot-on-shutdown` | stores a snapshot of in-memory chunks and series on shutdown so startup replays only the WAL not covered by the snapshot (docs) | disk snapshot written at shutdown |
| `extra-scrape-metrics` | adds `scrape_timeout_seconds`, `scrape_sample_limit`, `scrape_body_size_bytes` per target (run: values 3, 5000, 85820) | deprecated: startup warns it is being phased out; use `extra_scrape_metrics` in `global` or per scrape config. More series per target |
| `promql-experimental-functions` | enables experimental functions; without it `limitk(1,up)` fails with `limitk() is experimental and must be enabled with --enable-feature=promql-experimental-functions` (run); `limitk` and `sort_by_label` worked with it | may change or be removed |
| `promql-per-step-stats` | `stats=all` on a range query returns `totalQueryableSamplesPerStep` and `samplesReadPerStep` (run) | debugging only |
| `created-timestamp-zero-ingestion` | injects start (created) timestamps as 0-valued samples; the docs recommend `PrometheusProto`, and the flag changes the default `scrape_protocols` to negotiate it first | the application must expose start timestamps; OpenMetrics 1.0 shares them as extra `_created` series, which the docs call error-prone and expensive |
| `concurrent-rule-eval` | rules without a detectable dependency on other rules in the group are evaluated concurrently (docs); `--rules.max-concurrent-evals` defaults to 4 (run: shown in `/api/v1/status/flags`) | more concurrent query load (docs) |
| `delayed-compaction` | adds a random offset of up to 10% of the chunk range to the head compaction start, so instances do not compact at the same moment (docs) | none listed in the docs |
| `otlp-deltatocumulative` | converts OTLP delta metrics to cumulative instead of dropping them (docs) | in-memory per-series state, lost on restart (a counter reset in the cumulative series), mutex-guarded so it can hurt performance (docs) |

Separate flags (not feature flags): `--web.enable-otlp-receiver`, `--web.enable-remote-write-receiver`, `--web.enable-admin-api`, `--agent`.

## Usage
```bash
prometheus --config.file=prometheus.yml --enable-feature=exemplar-storage,memory-snapshot-on-shutdown
```

## Verify
- [ ] Startup log has one line per feature, e.g. "Experimental in-memory exemplar storage enabled", "Experimental per-step statistics reporting", "Experimental PromQL functions enabled." (seen in the 3.15.1 log).
- [ ] `prometheus_build_info` version matches the docs page you used for flag names.

## Checked
Prometheus 3.15.1 (windows-amd64) run with `--enable-feature=exemplar-storage,promql-per-step-stats,promql-experimental-functions` and separately `extra-scrape-metrics`, `native-histograms,bogus-flag`. Checked: startup log lines, the full valid-option list from `--help`, per-step `stats=all` output, `limitk`/`sort_by_label` with and without the flag, the three extra scrape series values, and the warning for a phased-out flag. Docs read: feature_flags.md at tag v3.15.1 (concurrent-rule-eval, delayed-compaction, created-timestamp-zero-ingestion and otlp-deltatocumulative descriptions in the table are taken from it).
