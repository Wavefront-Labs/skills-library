---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-stream-aggregation
name: victoriametrics-stream-aggregation
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [stream-aggregation, downsampling, recording-rules, aggregation-outputs, dedup-interval, vmagent]
level: advanced
status: docs-checked
description: "Aggregate samples on ingestion with stream aggregation config, outputs, by and without labels, staleness and dedup."
sources: ["https://docs.victoriametrics.com/victoriametrics/stream-aggregation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics stream aggregation

Stream aggregation processes data before it is stored. Enable it with `-streamAggr.config=aggr.yaml` (all incoming data) or, on vmagent, `-remoteWrite.streamAggr.config` per `-remoteWrite.url`. Related flags: `-streamAggr.dedupInterval`, `-streamAggr.ignoreOldSamples`, `-streamAggr.ignoreFirstIntervals`, `-streamAggr.enableWindows`, `-streamAggr.dropInputLabels` (per-URL variants use the `-remoteWrite.streamAggr.` prefix).

Each rule has `match`, `interval`, `outputs`, and optionally `by` or `without` (label lists), `keep_metric_names` (works with a single output), `staleness_interval` (defaults to `interval`), `dedup_interval`, `ignore_old_samples`, `ignore_first_intervals`, `enable_windows`, `drop_input_labels`, `input_relabel_configs`, `output_relabel_configs`, `flush_on_shutdown` and `no_align_flush_to_interval`.

```yaml
- match: 'http_requests_total'
  interval: 30s
  without: [path, user]
  outputs: [total]
```

Outputs: `total`, `total_prometheus`, `increase`, `increase_prometheus`, `rate_sum`, `rate_avg`, `count_samples`, `count_series`, `sum_samples`, `unique_samples`, `avg`, `min`, `max`, `last`, `stddev`, `stdvar`, `quantiles(...)`, `histogram_bucket`.

Output names follow `<metric_name>:<interval>[_by_<by_labels>][_without_<without_labels>]_<output>`, so the example above yields `http_requests_total:30s_without_path_user_total`.

Use cases: a cheap alternative to recording rules (use an interval of at least twice the collection interval), downsampling to one sample per 5 minutes, and reducing stored series by dropping high-cardinality labels.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
