---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-configuration-and-custom-builds
name: otel-collector-configuration-and-custom-builds
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, opentelemetry, otel-collector, otelcol, collector-config, collector-pipelines, otelcol-config, receivers, processors, exporters, connectors, extensions, service-pipelines, otlp-receiver, batch-processor, memory-limiter, resource-processor, otlphttp-exporter, prometheusremotewrite-exporter, spanmetrics-connector, health-check, file-storage, sending-queue, retry-on-failure, config-validate, env-substitution, ocb, collector-builder, custom-collector, collector-distributions, otelcol-contrib]
level: advanced
status: docs-checked
description: "Write a correct OpenTelemetry Collector config: components wired into service pipelines, the memory_limiter+batch pair, queues and retries, and custom builds with ocb."
sources: ["https://opentelemetry.io/docs/collector/configuration/", "https://opentelemetry.io/docs/collector/distributions/", "https://opentelemetry.io/docs/collector/extend/ocb/", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/memorylimiterprocessor/README.md", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/exporterhelper/README.md", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/receiver/otlpreceiver/README.md", "https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/prometheusremotewriteexporter/README.md"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OTel Collector configuration and custom builds

**Goal:** a Collector config that is valid before deploy, does not OOM, does not lose
data on backend hiccups, and contains only the components you actually use.

## 1. Structure
```yaml
receivers:      # how data gets in (otlp, prometheus, filelog, kafka, jaeger, hostmetrics, k8s_cluster...)
processors:     # what happens in between, in order (memory_limiter, batch, resource, attributes, filter, transform, tail_sampling, k8sattributes)
exporters:      # where it goes (otlp, otlphttp, prometheusremotewrite, prometheus, debug, kafka, loki via otlphttp, vendor exporters)
connectors:     # exporter of one pipeline + receiver of another (spanmetrics, servicegraph, forward, count, routing)
extensions:     # not in the data path (health_check, pprof, zpages, file_storage, basicauth, oauth2client, bearertokenauth)
service:
  extensions: [health_check, file_storage]
  pipelines:
    traces:  { receivers: [otlp], processors: [memory_limiter, k8sattributes, resource, batch], exporters: [otlp/tempo, spanmetrics] }
    metrics: { receivers: [otlp, prometheus, spanmetrics], processors: [memory_limiter, resource, batch], exporters: [prometheusremotewrite] }
    logs:    { receivers: [otlp, filelog], processors: [memory_limiter, k8sattributes, resource, batch], exporters: [otlphttp/loki] }
  telemetry:
    metrics: { level: detailed, readers: [{ pull: { exporter: { prometheus: { host: 0.0.0.0, port: 8888 } } } }] }
    logs: { level: info }
```
Defining a component does nothing until it is referenced in a pipeline. Names are
`type` or `type/name` (`otlp/tempo`). Pipelines are per signal type; a component can be in
several pipelines (receivers/exporters shared; processors instantiated per pipeline).

## 2. The non-negotiable processors
```yaml
processors:
  memory_limiter:            # best practice: first processor in the pipeline
    check_interval: 1s
    limit_percentage: 80      # of the container limit (or limit_mib)
    spike_limit_percentage: 20
  batch:                     # conventionally last before exporters
    send_batch_size: 8192
    send_batch_max_size: 16384
    timeout: 5s
```
`memory_limiter` refuses data (receivers return retryable errors) above the soft limit and
forces GC above the hard one; without it the Collector OOMs under backpressure. `batch`
turns thousands of tiny requests into few large ones; exporters' compression and backends'
rate limits assume it. The memory_limiter README also recommends setting `GOMEMLIMIT` to 80% of the collector's hard memory limit.

## 3. Receivers and exporters that matter
```yaml
receivers:
  otlp:
    protocols:
      grpc: { endpoint: 0.0.0.0:4317 }
      http: { endpoint: 0.0.0.0:4318, cors: { allowed_origins: ["https://shop.example.com"] } }   # browsers (Faro/OTel JS)
  prometheus:
    config: { scrape_configs: [{ job_name: self, scrape_interval: 30s, static_configs: [{ targets: ["localhost:8888"] }] }] }
  hostmetrics: { collection_interval: 30s, scrapers: { cpu: {}, memory: {}, disk: {}, filesystem: {}, network: {}, load: {} } }
exporters:
  otlp/tempo:
    endpoint: tempo-distributor:4317
    tls: { insecure: false, ca_file: /etc/otel/ca.pem }
    headers: { X-Scope-OrgID: team-payments }
    compression: gzip
    sending_queue: { enabled: true, num_consumers: 10, queue_size: 5000, storage: file_storage }   # persistent queue survives restarts
    retry_on_failure: { enabled: true, initial_interval: 5s, max_interval: 30s, max_elapsed_time: 300s }
    timeout: 10s
  prometheusremotewrite:
    endpoint: http://mimir/api/v1/push
    headers: { X-Scope-OrgID: team-payments }
    resource_to_telemetry_conversion: { enabled: false }   # true = ALL resource attrs become labels (cardinality!)
    target_info: { enabled: true }
    remote_write_queue: { num_consumers: 5, queue_size: 10000 }
    tls: { insecure_skip_verify: false }
  otlphttp/loki: { endpoint: http://loki-gateway/otlp, headers: { X-Scope-OrgID: team-payments } }
  debug: { verbosity: basic }        # detailed only while debugging; it is slow
extensions:
  health_check: { endpoint: 0.0.0.0:13133 }   # default is localhost:13133
  file_storage: { directory: /var/lib/otelcol/storage, timeout: 1s }
  pprof: { endpoint: localhost:1777 }
  zpages: { endpoint: localhost:55679 }
```
`sending_queue` + `retry_on_failure` are what make a backend outage survivable; the queue
is in memory unless `storage` points at `file_storage` (give the pod a volume). Queue full
⇒ data dropped and `otelcol_exporter_enqueue_failed_*` increments.

## 4. Connectors
```yaml
connectors:
  spanmetrics: { histogram: { explicit: { buckets: [5ms, 25ms, 100ms, 250ms, 1s, 5s] } }, dimensions: [{ name: http.route }, { name: http.response.status_code }], exemplars: { enabled: true } }
  servicegraph: { latency_histogram_buckets: [10ms, 100ms, 1s], dimensions: [], store: { ttl: 2s, max_items: 1000 } }
  routing: { default_pipelines: [traces/default], table: [{ statement: 'route() where resource.attributes["tenant"] == "a"', pipelines: [traces/a] }] }
  forward: {}
  count: {}                 # count spans/logs → metrics
```
List a connector as an **exporter** in the source pipeline and as a **receiver** in the target.

## 5. Config hygiene
- Env substitution `${env:TENANT}` and `${env:VAR:-default}`; several `--config` sources are merged
  (`--config=file:base.yaml --config=file:overrides.yaml`). `--set` merges one key/value after all
  `--config` sources, with `::` as the nested-key separator (`--set service::telemetry::logs::level=debug`).
- Validate before deploy: `otelcol-contrib validate --config=config.yaml` (the `validate` command; it does not
  test backend reachability). `otelcol print-config` shows the resolved config with secrets redacted.
- Keep secrets out of the YAML: `${env:VAR}` substitution, or an auth extension (`bearertokenauth`, `basicauth`,
  `oauth2client`) that reads credentials from a file or environment.
- One pipeline per signal per tenant/destination; avoid sharing a `batch` across wildly
  different volumes (it is per pipeline anyway).
- Keep `debug` exporter out of production pipelines (CPU + log spam).

## 6. Distributions and custom builds (OCB)
| Distribution | Contents | Use |
|---|---|---|
| `otelcol` (core) | smallest official set (see its `manifest.yaml`) | minimal gateways |
| `otelcol-contrib` | the broadest set of community components | default pick; largest binary |
| `otelcol-k8s`, `otelcol-otlp`, `otelcol-ebpf-profiler` | curated subsets | matching use cases |
| third-party distros (AWS ADOT, Splunk, Grafana Alloy, others on the Distributions page) | vendor extras + support | when on that vendor |
Build your own when you need: a small attack surface, a private component, or a
contrib-less image:
```yaml
# builder-config.yaml
dist: { name: otelcol-payments, output_path: ./dist, version: 0.1.0 }
receivers:
  - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.115.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/filelogreceiver v0.115.0
processors:
  - gomod: go.opentelemetry.io/collector/processor/memorylimiterprocessor v0.115.0
  - gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.115.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/k8sattributesprocessor v0.115.0
exporters:
  - gomod: go.opentelemetry.io/collector/exporter/otlpexporter v0.115.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/prometheusremotewriteexporter v0.115.0
extensions:
  - gomod: go.opentelemetry.io/collector/extension/healthcheckextension v0.115.0
```
```bash
# ocb: download the binary from the collector releases (cmd/builder tags) and needs Go installed
./ocb --config builder-config.yaml            # produces ./dist/otelcol-payments
./dist/otelcol-payments validate --config config.yaml
```
Replace `v0.115.0` in every `gomod` line with one real release and use a builder of the same version.
Keep the config outside the image.

## Gotchas
- Pipelines silently accept a processor order that is wrong (`batch` before `memory_limiter`) — fix order by review.
- `otlp` receiver without `endpoint` defaults to `localhost:4317` / `localhost:4318`, not `0.0.0.0`: pods can't reach it.
- `prometheusremotewrite` drops non-cumulative monotonic, histogram and summary metrics; convert delta metrics to cumulative before it.
- Changing `service.pipelines` names resets persistent queue files (keyed by pipeline/exporter).
- Contrib components get deprecated/renamed (`loki` exporter → `otlphttp`; `logging` → `debug`); read the changelog on every bump.

## Verify
- [ ] `otelcol-contrib validate --config` passes in CI; the running pod answers on the health_check endpoint (13133 as configured above).
- [ ] Stopping the backend for longer than a typical outage then restarting it yields no gap (persistent queue drains; `enqueue_failed` stays 0).
- [ ] `otelcol_processor_refused_spans` (memory_limiter) is 0 at normal load and memory stays under the container limit under a load spike.
- [ ] The custom OCB binary starts with the production config and the image is smaller than the contrib image.

## Checked

2026-10-31. Confirmed against the Collector configuration, Distributions and OCB pages (`--config` merging, `--set`, `${env:VAR:-default}`, `validate`, five official distributions, `dist`/`gomod` manifest), the memory_limiter README (first processor, `GOMEMLIMIT` at 80%, percentage options), the OTLP receiver README (localhost defaults), the Prometheus remote write exporter README (non-cumulative metrics dropped) and the health_check README.
Removed: `max_recv_msg_size_mib`, the `go install` builder command and the pinned version in it, the "Server available" response body, image-size and component-count figures, the 90% GOMEMLIMIT figure, test durations, the `$__file` mount remark and the dist `description`.
Method: documentation only; no commands were run.
