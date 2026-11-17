---
id: computing-software.cloud-infrastructure-engineering.kubernetes.loki-log-aggregation-in-kubernetes
name: loki-log-aggregation-in-kubernetes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, loki, promtail, grafana-alloy, logql, log-aggregation, label-cardinality, chunks, index, grafana, streams]
level: advanced
status: docs-checked
description: "Deploying Loki for Kubernetes log aggregation: the label-as-index model, Promtail/Alloy discovery, LogQL basics, and the cardinality mistakes that make Loki slow or expensive."
sources: ["https://grafana.com/docs/loki/latest/get-started/labels/", "https://grafana.com/docs/loki/latest/operations/storage/retention/", "https://grafana.com/docs/loki/latest/get-started/deployment-modes/", "https://grafana.com/docs/loki/latest/operations/troubleshooting/troubleshoot-ingest/", "https://grafana.com/docs/loki/latest/send-data/promtail/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki in Kubernetes: index by label, grep the rest

**Goal:** deploy and query Loki correctly by internalizing its core design choice — it
indexes **labels only**, not log content — which is both why it's cheap at scale and the
source of almost every "Loki is slow" complaint when someone treats labels like
Elasticsearch fields.

## 1. The model: streams, chunks, and the label index
Loki groups logs into **streams** — one stream per unique combination of label values. Each
stream's log lines are compressed into **chunks** in object storage (S3/GCS/filesystem); the
**index only maps label sets to chunk locations**, not log content. Querying filters by
label first (cheap, index lookup), then **greps the matching chunks' content** (the expensive
part, proportional to log volume in the matched streams over the time range).

Consequence: **every unique label value creates a new stream**, and Loki performance and
cost scale with stream count, not just total log volume. This inverts the Prometheus
intuition — in Prometheus more labels are usually fine until genuinely high-cardinality; in
Loki, a label with unbounded cardinality (a request ID, a user ID, a timestamp put in a
label instead of content) **must never be a label** — it creates one stream per log line and
can take down ingesters (`too many streams` / `per-stream rate limit exceeded` errors) or
balloon storage/index size.

## 2. Kubernetes-specific label conventions
Via Promtail or **Grafana Alloy** (Promtail's successor, different config language; Loki's docs say Promtail reached end of life on
2 March 2026 with no further updates, so use Alloy for new and migrating deployments):
discovery mirrors Prometheus's `kubernetes_sd_configs` — same relabeling mental model, which
is why teams running both find Loki's config half-familiar and half-surprising. Standard
labels to keep: `namespace`, `pod` (bounded-ish per deployment, but churns across rollouts —
accept the churn, it's still far lower cardinality than a trace/request ID),
`container`, `app`/`job`. **Do not** promote arbitrary pod annotations to labels the way
kube-state-metrics does for `kube_pod_annotations`
(`computing-software.cloud-infrastructure-engineering.kubernetes.kube-state-metrics-object-state-and-cardinality`)
— that pattern is fine for a low-cardinality Prometheus gauge, catastrophic as a Loki label.

Loki's labels docs say to keep labels low-cardinality and to use structured metadata for
high-cardinality values you search often (for example a trace ID); otherwise keep fields inside
the log line and extract them at query time with LogQL's `| json` / `| logfmt` parsers. The docs
also note that `k8s.pod.name` and `service.instance.id` are no longer recommended as default
labels for OpenTelemetry ingestion because of their cardinality.

## 3. LogQL essentials
```logql
{namespace="checkout", container="api"} |= "error"                    # label select + line filter (cheap then expensive)
{namespace="checkout"} | json | status_code >= 500                    # parse JSON, filter on extracted field
sum(rate({namespace="checkout"} |= "error" [5m])) by (pod)             # log-derived metric query
{namespace="checkout"} | logfmt | line_format "{{.msg}}"               # reformat output
```
- Line filters (`|=`, `!=`, regex `|~`) run **after** the label match narrows the stream set —
  put the most selective label filter first; a query with only a broad label match and a
  wide time range scans every chunk in that range.
- `rate()`/`count_over_time()` turn logs into Prometheus-style time series — this is how
  "error rate from logs" panels get built without a separate metrics pipeline, and is often
  the fastest way to alert on an error signature that was never instrumented as a metric.

## 4. Operational gotchas
- **Out-of-order writes**: Loki accepts out-of-order entries within a stream; the docs tie how far
  back they may be to `max_chunk_age` (default 2h), and the troubleshooting guide lists
  `entry too far behind` errors for older entries. There is also `reject_old_samples` (default
  true) with `reject_old_samples_max_age` (default 1 week) in `limits_config`.
- **Retention is applied by the compactor**: `compactor.retention_enabled` defaults to `false`, so logs
  live forever by default. Enable it, set `limits_config.retention_period` (it only applies when
  retention is enabled; 0 disables) and run the compactor as a singleton. Per-tenant and per-stream
  retention are also supported.
- **Deployment mode**: Loki's docs describe monolithic (`-target=all`, suited to roughly up to 20GB/day),
  HA monolithic and microservices modes. HA monolithic replaces the Simple Scalable Deployment, which
  is deprecated and will be removed in Loki 4.0. Know which mode runs before chasing a failure to a
  component (`distributor` for ingest limits, `ingester`, `querier`/`query-frontend` for reads).
- Ingest limits are reported with `loki_discarded_samples_total` and `loki_discarded_bytes_total`
  (label `reason`). Typical errors: `Per stream rate limit exceeded` (`per_stream_rate_limit`, default 3MB) and
  `maximum active stream limit exceeded` (`max_global_streams_per_user`, default 5000). The docs warn
  not to raise stream limits to accommodate high-cardinality labels.

## Gotchas
- A dashboard built on `count_over_time` of a line filter instead of a real metric is a
  cheap win early on, but doesn't replace proper instrumentation — line-filter counting
  breaks silently if a log message's wording changes in a future release.
- Promtail/Alloy itself needs the same offset-tracking and rotation awareness as any
  node-level tailer (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.node-level-logging-with-fluent-bit-and-fluentd`)
  — Loki's ingest side doesn't fix tailer-side log loss.

## Verify
- [ ] No label in the pipeline config has unbounded or near-unbounded cardinality (audit `{namespace=~".+"} | label_values` style checks periodically).
- [ ] `compactor.retention_enabled` is true, a retention period is set and the compactor is confirmed running.
- [ ] `loki_discarded_samples_total` by `reason` is scraped and alerted on.

## Checked

2026-10-26, against Loki docs in grafana/loki (docs/sources, latest commit 2026-10-24), including the configuration reference, labels, retention, deployment-modes and troubleshoot-ingest pages. Confirmed: label-indexed streams and cardinality guidance, structured metadata for high-cardinality data, Promtail EOL date, retention flags and defaults, `max_chunk_age`, `reject_old_samples`, stream and rate limit defaults and error text, deployment modes and the SSD deprecation. Wrong: Promtail described as LTS-only (it is EOL), `unordered_writes` (not in the current configuration reference), retention advice that omitted `compactor.retention_enabled`, and error strings `too many streams`/`entry out of order`. Removed the unconfirmed Grafana Explore line-cap claim and the dashboard timing check. Alloy's own configuration was not checked.

Method: documentation only; no commands were run.
