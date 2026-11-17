---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-remote-write-and-agent-mode
name: prometheus-remote-write-and-agent-mode
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, remote-write, remote-write-tuning, remote-write-queue, remote-read, agent-mode, prometheus-agent, queue-config, shards, max-samples-per-send, write-relabel-configs, remote-write-2, prometheus-remote-write-protocol, backpressure, wal-truncation, mimir, thanos-receive, cortex, victoriametrics, grafana-alloy, pca]
level: advanced
status: docs-checked
description: "Ship samples to Mimir/Thanos reliably: queue_config tuning, write_relabel_configs, remote write 2.0, agent mode for edge collectors, and the lag/failure metrics to alert on."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write", "https://prometheus.io/docs/practices/remote_write/", "https://prometheus.io/docs/prometheus/latest/feature_flags/#prometheus-agent", "https://prometheus.io/docs/specs/prw/remote_write_spec_2_0/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote write and agent mode

**Goal:** every sample scraped reaches the long-term store with bounded lag and no silent
drops, using as little memory as possible on the sending side.

## 1. Minimal, correct config
```yaml
remote_write:
  - url: https://mimir.internal/api/v1/push
    name: mimir
    protobuf_message: io.prometheus.write.v2.Request   # remote write 2.0; default is prometheus.WriteRequest (1.0); check receiver support first
    headers: { X-Scope-OrgID: team-payments }           # Mimir/Cortex tenant
    basic_auth: { username: prom, password_file: /etc/prometheus/secrets/rw }
    send_exemplars: true
    send_native_histograms: true
    write_relabel_configs:
      - { action: drop, source_labels: [__name__], regex: "go_.*|process_.*" }
    queue_config:
      capacity: 10000            # per shard buffer (samples)
      max_shards: 50
      min_shards: 1
      max_samples_per_send: 2000
      batch_send_deadline: 5s
      min_backoff: 30ms
      max_backoff: 5s
      retry_on_http_429: true    # default false (experimental)
    metadata_config: { send: true, send_interval: 1m }
```
- Remote write reads from the **WAL**, so it survives restarts and the receiver being
  down (until the WAL is truncated, ~2h of data by default; longer outages lose data).
- Prometheus auto-scales shards between `min_shards` and `max_shards` from observed
  ingestion vs send rate. Start with defaults; tune only with evidence.
- `external_labels` are added to every series sent to external systems such as remote storage.

## 2. Tuning rules of thumb
- Unless the endpoint is very slow, `max_shards` rarely needs to go above the default (50). `max_samples_per_send`
  suits the backend: some take bigger batches well, others fail on large requests.
- Shard memory is proportional to shards * (capacity + max_samples_per_send); the defaults (capacity 10000,
  max_samples_per_send 2000) stay under 2 MB per shard. Each remote has its own queue.
- Backpressure: when a shard fills its queue, Prometheus **blocks reading from the WAL**, so lag grows;
  failures are retried without loss unless the endpoint is down for more than 2 hours.
- Per the remote write 2.0 spec, senders must not retry 4xx other than 429, must retry 5xx and use backoff.
  A rejected request is therefore lost, so scrub invalid labels with `write_relabel_configs`.

## 3. Watch it
```promql
# lag in seconds between newest enqueued sample and newest sent
prometheus_remote_storage_queue_highest_timestamp_seconds
  - prometheus_remote_storage_queue_highest_sent_timestamp_seconds
rate(prometheus_remote_storage_samples_failed_total[5m])     # unrecoverable drops
rate(prometheus_remote_storage_samples_retried_total[5m])
prometheus_remote_storage_shards / prometheus_remote_storage_shards_max   # pegged at 1 = at the shard cap
rate(prometheus_remote_storage_samples_dropped_total[5m])    # write_relabel drops (expected) 
```
Alert on sustained lag and on any `samples_failed_total` increase.

## 4. Agent mode
```bash
prometheus --agent --config.file=prometheus.yml --storage.agent.path=/data \
  --storage.agent.retention.max-time=2h
```
- Keeps scraping, service discovery and their configuration; **disables** querying, alerting and local
  storage, replacing the TSDB with a customized WAL (blog announcing agent mode).
- Use at the edge (per cluster, per site, behind NAT) sending to a central Mimir/Thanos
  Receive; keep one full Prometheus (or Mimir ruler) centrally for rules.

## 5. remote_read
```yaml
remote_read:
  - url: https://mimir.internal/prometheus/api/v1/read
    read_recent: false          # only query remote for ranges older than local data
    required_matchers: { cluster: prod }
```
Rarely worth it; querying Mimir/Thanos directly from Grafana is faster. Useful during
migrations so old data is reachable from the local server.

## Gotchas
- A receiver that is slow but up causes shards to scale to max and memory to climb; cap
  `max_shards` to protect the sender, and accept lag.
- Running remote_write to two remotes doubles WAL read load and memory; fine on small servers.
- `name:` labels the queue in metrics and logs and must be unique among remote_write configs.
- Native histograms need receiver support; `send_native_histograms` is a no-op (always true) with the 2.0 message.
- A receiver without remote write 2.0 support may answer 415; the spec lets senders retry with another
  content type. Test the receiver before setting `protobuf_message`.

## Checked
2026-10-28. Confirmed: configuration page (`protobuf_message` default and values, `send_exemplars`,
`send_native_histograms`, `name`, `headers`, `write_relabel_configs`, `queue_config` defaults, `retry_on_http_429` default
false, `read_recent`, `required_matchers`, external_labels scope), Remote write tuning page (2 hour limit, memory formula,
blocking), remote write 2.0 spec (4xx/429/5xx and 415 rules), command-line page (`--agent`, `--storage.agent.*`), agent
mode blog, and Prometheus source for metric names. Removed: throughput and memory-per-shard formulas not in the docs,
5000-10000 batch advice, lag thresholds, Mimir/Thanos version gates, HA-dedupe label claim, collector interchangeability,
rename behaviour.
Method: documentation only; no commands were run.

## Verify
- [ ] Lag stays near zero in steady state and recovers after a short receiver outage without `samples_failed_total` increments.
- [ ] A test series scraped locally appears in the remote within one scrape interval + lag.
- [ ] Agent-mode pods use noticeably less memory than the full server they replaced.
