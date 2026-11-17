---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-troubleshooting-and-internal-telemetry
name: otel-collector-troubleshooting-and-internal-telemetry
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, opentelemetry, otel-collector, collector-troubleshooting, collector-internal-telemetry, otelcol-metrics, debug-exporter, zpages, pprof-extension, health-check, telemetrygen, otlp-debugging, data-loss, dropped-spans, refused-spans, enqueue-failed, send-failed, queue-size, memory-limiter, oom, backpressure, tls-errors, grpc-errors, resource-exhausted, 429, config-reload, log-level-debug, collector-dashboard]
level: advanced
status: docs-checked
description: "Find out where telemetry stops in a Collector: the otelcol_* internal metrics that locate loss (refused, enqueue_failed, send_failed), plus debug exporter and zpages."
sources: ["https://opentelemetry.io/docs/collector/troubleshooting/", "https://opentelemetry.io/docs/collector/internal-telemetry/", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/extension/zpagesextension/README.md", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/telemetrygen"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collector troubleshooting and internal telemetry

**Goal:** when "the traces are not showing up", point at the exact stage (app → receiver →
processor → queue → exporter → backend) within ten minutes, using the Collector's own
numbers rather than guesses.

## 1. Turn on the Collector's own telemetry (always, in prod)
```yaml
service:
  telemetry:
    metrics:
      level: detailed                 # basic | normal (default) | detailed
      readers: [{ pull: { exporter: { prometheus: { host: 0.0.0.0, port: 8888 } } } }]   # scrape it; older: address: 0.0.0.0:8888
    logs: { level: info, encoding: json }
extensions:
  zpages: { endpoint: 0.0.0.0:55679 }
  pprof: { endpoint: 0.0.0.0:1777 }
```
Internal metrics are served on port 8888 by default (`http://127.0.0.1:8888/metrics`); scrape them with Prometheus.

## 2. The loss ledger: metrics by stage
```promql
# receivers: what came in, what was pushed back
sum by (receiver) (rate(otelcol_receiver_accepted_spans[5m]))
sum by (receiver) (rate(otelcol_receiver_refused_spans[5m]))        # memory_limiter or downstream error → SDK retries
# processors: items in vs items out shows what a processor discarded
sum by (processor) (rate(otelcol_processor_incoming_items[5m]))
sum by (processor) (rate(otelcol_processor_outgoing_items[5m]))
rate(otelcol_processor_batch_batch_send_size_sum[5m]) / rate(otelcol_processor_batch_batch_send_size_count[5m])   # effective batch size
# exporters: the usual culprit
sum by (exporter) (rate(otelcol_exporter_sent_spans[5m]))
sum by (exporter) (rate(otelcol_exporter_send_failed_spans[5m]))    # backend rejected after retries → LOST
sum by (exporter) (rate(otelcol_exporter_enqueue_failed_spans[5m])) # queue full → LOST
otelcol_exporter_queue_size / otelcol_exporter_queue_capacity        # both in batches; near 1 = backend slow / down
# process
otelcol_process_memory_rss ; otelcol_process_runtime_total_sys_memory_bytes ; otelcol_process_cpu_seconds
```
(Same families with `_metric_points` and `_log_records`.) Compare accepted, refused, enqueue_failed, send_failed
and sent; whichever failure term is non-zero names the stage. Alert on `send_failed`, `enqueue_failed`, `refused`
and a high queue ratio. Sustained `refused` rates mean clients are getting errors, which may be client-side data loss.

## 3. See the actual data
- **debug exporter** temporarily added to the pipeline (`debug: { verbosity: detailed }`)
  prints resource attributes, span names, attributes. Use a canary replica, not the fleet.
- **zpages** (port 55679, default endpoint `localhost:55679`): `/debug/tracez` (spans bucketed by latency),
  `/debug/pipelinez` (receivers, processors and exporters per pipeline), `/debug/servicez`,
  `/debug/extensionz`. Great for "is this receiver even in a pipeline?".
- **Synthetic input**: `telemetrygen traces --otlp-insecure --traces 1`
  (`metrics` and `logs` subcommands too; `telemetrygen traces --help` lists the endpoint option). If synthetic data arrives at the backend, the fault is upstream in the app.
- **Log level**: set `service::telemetry::logs::level` to `debug` temporarily.

## 4. Decode common errors
| Log / symptom | Meaning | Fix |
|---|---|---|
| `Dropping data because sending_queue is full` | backend slower than ingest for too long | persistent queue, scale backend, shed |
| `refused` counters rising | receiver returning errors to clients, often memory pressure from a missing or misconfigured `memory_limiter` | fix memory limits and queue sizes |
| nothing at all, no errors | receiver bound to localhost, or wrong port/protocol (gRPC vs HTTP) | check the listening address and the client's protocol |
| exporter errors with TLS/auth wording | TLS mismatch (plaintext vs TLS, wrong CA) | check exporter `tls` settings and the port |

## 5. Memory and CPU
```bash
curl -s http://localhost:1777/debug/pprof/heap > heap.pb.gz && go tool pprof -top heap.pb.gz
```
The pprof extension listens on port 1777 and is an advanced tool. Memory pressure often comes from a missing or misconfigured `memory_limiter` processor.
CPU: the `debug` exporter left on at `detailed` verbosity.

## 6. Method
1. Backend empty? → is `exporter_sent_*` rising? If yes, backend/query problem (tenant header, time range).
2. `sent` flat → `enqueue_failed`/`send_failed`/`queue_size` → exporter/backend problem (see table).
3. Exporter fine but `accepted` flat → receiver/app problem: `telemetrygen` into the receiver; if it arrives, fix the app (`OTEL_*` env, agent order).
4. `refused` rising → memory_limiter → memory pressure, see §5.
5. Data arrives mangled → `debug` exporter at the receiver stage vs after processors; bisect the processor list.

## Gotchas
- Internal metric names change across versions (for example, `_total` suffixes are off by default for `otelcol_process_uptime`); check `:8888` for the exact names in your version.
- The `debug` exporter at `detailed` can itself be the bottleneck.
- The health_check extension reports process liveness, not whether exports succeed; use the exporter metrics.
- A pipeline with no exporters is a config error; a pipeline whose exporter is `debug` only looks fine and sends nothing to backends.

## Verify
- [ ] Collector dashboard shows accepted ≈ sent per signal with `send_failed`, `enqueue_failed`, `refused` at 0 in steady state.
- [ ] `telemetrygen` traces reach the backend end to end.
- [ ] Alerts exist for a high queue ratio, any `send_failed` rate > 0, and RSS near the memory limit.
- [ ] You can name the stage of the last three "data missing" incidents from the metrics alone.

## Checked
2026-10-31. Confirmed against the Collector internal-telemetry page (port 8888, levels basic/normal/detailed with normal default, `readers` pull/prometheus form, json log encoding, the `otelcol_exporter_*`, `otelcol_receiver_*`, `otelcol_process_*` and `otelcol_processor_incoming_items|outgoing_items` and batch `batch_send_size` metric names, queue size in batches, `Dropping data because sending_queue is full`), the Collector troubleshooting page (pprof port 1777, zPages port 55679, `/debug/tracez`, memory_limiter pressure), the zpagesextension README (`/debug/pipelinez|servicez|extensionz`) and the telemetrygen README (`--otlp-insecure`, `--traces`). Removed: the processor dropped/filter/tail-sampling metric names, the dashboard id, self-tracing config, the error-message table rows (gRPC/HTTP codes, retry-after, k8sattributes), the 0.8/85%/10 s thresholds and the load-balancer remark (not in the fetched pages).
Method: documentation only; no commands were run.
