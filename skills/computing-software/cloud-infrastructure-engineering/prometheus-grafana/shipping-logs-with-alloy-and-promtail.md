---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.shipping-logs-with-alloy-and-promtail
name: shipping-logs-with-alloy-and-promtail
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, loki, loki-ingest, grafana-alloy, alloy, promtail, log-shipping, kubernetes-logs, loki-source-kubernetes, loki-source-file, loki-process, pipeline-stages, multiline, json-stage, logfmt-stage, labels-stage, drop-stage, timestamp-stage, positions-file, loki-write, batching, backoff, otel-collector-loki, fluent-bit-loki, docker-driver, systemd-journal]
level: practitioner
status: gated
description: "Ship logs into Loki with Grafana Alloy (or Promtail): Kubernetes pod discovery and relabeling, processing stages (multiline, json, labels, drop, timestamp), loki.write batching, and debugging."
sources: ["https://grafana.com/docs/alloy/latest/reference/components/loki/loki.source.kubernetes/", "https://grafana.com/docs/alloy/latest/reference/components/loki/loki.process/", "https://grafana.com/docs/alloy/latest/reference/components/loki/loki.write/", "https://grafana.com/docs/loki/latest/send-data/promtail/", "https://grafana.com/docs/loki/latest/send-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shipping logs with Alloy and Promtail

**Goal:** every pod/host log line reaches Loki once, with the right few labels, correct
timestamps and multiline stack traces intact — and when it doesn't, you can see where it stopped.

## 1. Which shipper
- **Grafana Alloy** (current; Promtail reached EOL on 2 March 2026): one agent for logs,
  metrics, traces, profiles; components wired in an Alloy config (attributes in a block go on separate lines; comments are `//` or `/* */`, not `#`, and there is no `;`).
- **Promtail**: same pipeline model, YAML (`scrape_configs` + `pipeline_stages`); migrate
  with `alloy convert --source-format=promtail --output=config.alloy promtail.yaml`.
- Alternatives already in place: OpenTelemetry Collector (`filelog` receiver → `otlphttp`
  to Loki `/otlp`), Fluent Bit `loki` output, Docker Loki logging driver, Vector `loki` sink (gated: unconfirmed, source is paywalled or blocked): none of these were run.

## 2. Alloy on Kubernetes (DaemonSet via `grafana/alloy` or `k8s-monitoring` Helm chart (gated: unconfirmed, source is paywalled or blocked): no Kubernetes or Helm run)
```alloy
discovery.kubernetes "pods" {
  role = "pod"
}

discovery.relabel "pods" {
  targets = discovery.kubernetes.pods.targets

  // only this node's pods
  rule {
    source_labels = ["__meta_kubernetes_pod_node_name"]
    regex         = sys.env("HOSTNAME")
    action        = "keep"
  }
  rule {
    source_labels = ["__meta_kubernetes_namespace"]
    target_label  = "namespace"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_label_app_kubernetes_io_name"]
    target_label  = "app"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_container_name"]
    target_label  = "container"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_name"]
    target_label  = "pod"
  }
  rule {
    source_labels = ["__meta_kubernetes_namespace"]
    regex         = "kube-system"
    action        = "drop"
  }
}

// tails via the Kubernetes API (no hostPath needed)
loki.source.kubernetes "pods" {
  targets    = discovery.relabel.pods.output
  forward_to = [loki.process.pods.receiver]
}

loki.process "pods" {
  stage.cri {}

  stage.multiline {
    firstline     = "^\\d{4}-\\d{2}-\\d{2}[T ]\\d{2}:\\d{2}"
    max_wait_time = "3s"
    max_lines     = 500
  }

  stage.json {
    expressions = { level = "level", ts = "timestamp", trace_id = "trace_id" }
  }

  stage.template {
    source   = "level"
    template = "{{ ToLower .Value }}"
  }

  stage.labels {
    values = { level = "" }
  }

  stage.structured_metadata {
    values = { trace_id = "", pod = "" }
  }

  // pod stays queryable as structured metadata only (avoids stream churn)
  stage.label_drop {
    values = ["pod"]
  }

  stage.timestamp {
    source            = "ts"
    format            = "RFC3339Nano"
    action_on_failure = "fudge"
  }

  stage.drop {
    source              = "level"
    value               = "debug"
    drop_counter_reason = "debug"
  }

  stage.drop {
    longer_than         = "256KB"
    drop_counter_reason = "too_long"
  }

  stage.static_labels {
    values = { cluster = "prod-eu1" }
  }

  forward_to = [loki.write.default.receiver]
}

loki.write "default" {
  endpoint {
    url       = "https://loki-gateway/loki/api/v1/push"
    tenant_id = "team-payments"

    basic_auth {
      username      = "alloy"
      password_file = "/etc/alloy/secrets/loki"
    }

    batch_wait          = "1s"
    batch_size          = "1MiB"
    min_backoff_period  = "500ms"
    max_backoff_period  = "5m"
    max_backoff_retries = 10
  }

  external_labels = { cluster = "prod-eu1" }

  // experimental: needs `alloy run --stability.level=experimental`
  wal {
    enabled         = true
    max_segment_age = "1h"
  }
}
```
RBAC for `loki.source.kubernetes`: it tails through the Kubernetes API, which the docs say costs more kubelet network and CPU than `loki.source.file`; the exact ClusterRole rules are not in that page (gated: unconfirmed, source is paywalled or blocked).

## 3. Hosts and journals
```alloy
loki.source.journal "sys" {
  max_age       = "12h"
  labels        = { job = "systemd-journal" }
  relabel_rules = loki.relabel.journal.rules
  forward_to    = [loki.write.default.receiver]
}

loki.relabel "journal" {
  forward_to = []

  rule {
    source_labels = ["__journal__systemd_unit"]
    target_label  = "unit"
  }
}

local.file_match "nginx" {
  path_targets = [{ __path__ = "/var/log/nginx/*.log", job = "nginx", host = constants.hostname }]
}

loki.source.file "nginx" {
  targets       = local.file_match.nginx.targets
  forward_to    = [loki.write.default.receiver]
  tail_from_end = true
}

loki.write "default" {
  endpoint {
    url = "http://127.0.0.1:3199/loki/api/v1/push"
  }
}
```
Positions are persisted under the Alloy storage path (`--storage.path`; Promtail: `positions.filename`); with no stored position the file is read from the start unless `tail_from_end = true` (default false).

## 4. Promtail equivalent (EOL; for reading old configs)
```yaml
# placeholders marked [ ...same as above... ] must be filled in; the rest converts with `alloy convert`
clients: [{ url: https://loki/loki/api/v1/push, tenant_id: team-payments, batchwait: 1s, batchsize: 1048576, backoff_config: { max_retries: 10 } }]
positions: { filename: /run/promtail/positions.yaml }
scrape_configs:
  - job_name: pods
    kubernetes_sd_configs: [{ role: pod }]
    relabel_configs: [ ...same as above... , { source_labels: [__meta_kubernetes_pod_uid, __meta_kubernetes_pod_container_name], target_label: __path__, separator: /, replacement: /var/log/pods/*$1/*.log } ]
    pipeline_stages:
      - cri: {}
      - multiline: { firstline: '^\d{4}-\d{2}-\d{2}', max_wait_time: 3s }
      - json: { expressions: { level: level, trace_id: trace_id } }
      - labels: { level: "" }
      - structured_metadata: { trace_id: "" }
      - timestamp: { source: ts, format: RFC3339Nano }
```

## 5. Debugging a silent pipeline
1. Alloy UI (`127.0.0.1:12345` by default) → components → `discovery.relabel`/`loki.source.*` shows targets
   and their labels; the `loki.process` debug stream shows lines after each stage
   (top-level `livedebugging { enabled = true }`, accepted by `alloy validate` in v1.21.1).
2. Metrics: `loki_source_file_read_lines_total`, `loki_process_dropped_lines_total{reason}`,
   `loki_write_sent_entries_total`, `loki_write_dropped_entries_total`, `loki_write_request_duration_seconds`,
   `loki_write_batch_retries_total`. Zero `sent_entries` with rising `read_lines` → a stage
   drops everything (often a `stage.drop` or a failed `stage.json` feeding a filter).
3. Loki side: 429 → `per_stream_rate_limit`/`ingestion_rate_mb`; 400 `entry too far behind`
   → timestamps wrong (fix `stage.timestamp` or let Loki assign ingest time).
4. `alloy fmt config.alloy` formats and `alloy validate config.alloy` checks syntax and component references (there is no `alloy run --dry-run`).

## Gotchas
- `stage.json` after `stage.cri` parses the **message** only if `stage.cri` put it in the
  line; Docker `json-file` logs need `stage.docker {}` first.
- `stage.timestamp` on a parse failure follows `action_on_failure`: `fudge` (default) reuses the last known timestamp plus 1 ns, `skip` keeps the scrape time; compare entry time with the time inside the line to catch it.
- `stage.multiline` flushes a block after `max_wait_time` (default 3s) and holds at most `max_lines` (default 128) lines; the page's `max_lines = 500` raises that.
- `external_labels` on the writer apply to **all** streams; do not put per-app labels there.

## Verify
- [ ] Grafana Explore `{cluster="prod-eu1", app="api"}` shows lines within 5 s of `kubectl logs` output.
- [ ] A Java stack trace arrives as a single entry.
- [ ] `loki_write_dropped_entries_total` is 0 after 24 h; backoff retries recover after a 5-minute Loki outage with no gaps.
- [ ] Stream count per node is stable across pod restarts (no `pod` label unless intended).

## Checked
Ran Alloy v1.21.1 on Windows. The page's original blocks failed `alloy validate` (`;` separators, `#` comments, attributes on one line, deprecated `env()` which prints a deprecation warning; `sys.env()` is the replacement); the rewritten Kubernetes and host blocks validate, and the same `loki.process` pipeline (`stage.cri`, `stage.multiline`, `stage.json`, `stage.template` ToLower, `stage.labels`, `stage.structured_metadata`, `stage.label_drop`, `stage.timestamp`, two `stage.drop`, `stage.static_labels`) ran on a CRI-format file into Loki 3.7.9: level lower-cased, the debug line dropped, the stack trace joined into one entry, entry time taken from the JSON `timestamp`, `pod` kept as structured metadata only. `loki.write` `wal {}` is experimental: with the default stability level Alloy refuses to build the component (`enabling wal requires stability.level flag to be experimental`), noted in the page. The Promtail YAML shape converted with `alloy convert`. Metric names (`loki_source_file_read_lines_total`, `loki_process_dropped_lines_total`, `loki_write_*`), `drop_counter_reason`, `longer_than`, `max_wait_time`/`max_lines` defaults and `action_on_failure` were read in the Alloy v1.21.1 reference. Not run: Kubernetes discovery, RBAC, Helm and the alternative shippers (gated as marked).
