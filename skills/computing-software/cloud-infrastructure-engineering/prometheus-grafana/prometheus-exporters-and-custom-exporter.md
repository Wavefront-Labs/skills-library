---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-exporters-and-custom-exporter
name: prometheus-exporters-and-custom-exporter
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, exporters, exporter, node-exporter, blackbox-exporter, custom-exporter, writing-exporters, exporter-development, textfile-collector, mysqld-exporter, postgres-exporter, redis-exporter, snmp-exporter, json-exporter, windows-exporter, statsd-exporter, graphite-exporter, exporter-ports, collect-on-scrape, multi-target-pattern, probe-endpoint]
level: advanced
status: docs-checked
description: "Choose, deploy and write exporters: node/blackbox/textfile patterns, the multi-target /probe convention, and the rules for a custom exporter (collect on scrape)."
sources: ["https://prometheus.io/docs/instrumenting/exporters/", "https://prometheus.io/docs/instrumenting/writing_exporters/", "https://github.com/prometheus/node_exporter", "https://github.com/prometheus/blackbox_exporter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exporters and writing your own

**Goal:** get metrics out of things you cannot instrument directly, and when nothing
exists, write an exporter that behaves like the official ones.

## 1. Pick an exporter
The Prometheus exporters page marks some exporters "official" (maintained in the Prometheus GitHub organisation); the
rest are community-maintained and not vetted for best practices. Marked official: node/system, blackbox, MySQL server,
Consul, Memcached, HAProxy, AWS CloudWatch, Collectd, Graphite, InfluxDB, JMX, SNMP, StatsD. PostgreSQL, Redis,
Windows, SQL and many more are listed as third-party.
Each exporter has a unique default port; the registry is the "Default port allocations" wiki page. node_exporter
listens on 9100 and blackbox_exporter on 9115 by default. For exporters of internal applications, use ports outside the
default allocations.
Run one exporter per application instance, next to it (same machine or sidecar), with service discovery done in
Prometheus. Exceptions: SNMP, blackbox and IPMI exporters, where nothing can run beside the target, and a stat-puller
that talks to any one replica through a load balancer. Do not do this for systems with master election; monitor each
instance.

## 2. node_exporter
- Collectors are enabled with `--collector.<name>` and default ones disabled with `--no-collector.<name>`;
  `--collector.disable-defaults` enables only those you list. `systemd` and `processes` are off by default.
- Filter with include/exclude flags, e.g.
  `--collector.filesystem.mount-points-exclude=^/(dev|proc|sys|var/lib/docker/.+|var/lib/kubelet/.+)($|/)`.
  Include and exclude flags are mutually exclusive on a collector.
- `node_scrape_collector_success` and `node_scrape_collector_duration_seconds` report collector health.
- In a container, share the host namespaces (Docker: `--net=host --pid=host`) and bind-mount the host root, e.g.
  `-v /:/host:ro,rslave`, then pass `--path.rootfs=/host`. Non-root mount points must be bind-mounted too.
- **Textfile collector**: set `--collector.textfile.directory`; it parses every `*.prom` file there in the text
  format, and timestamps are not supported. Write atomically: `echo ... > x.prom.$$` then `mv x.prom.$$ x.prom`.
  Use it for machine-tied metrics (for example a cron job's completion time); service-level metrics belong in the
  Pushgateway.
- `--web.config.file` enables TLS or basic auth (exporter-toolkit web configuration).

## 3. blackbox_exporter and the multi-target pattern
```yaml
# blackbox.yml (load with --config.file)
modules:
  http_2xx:
    prober: http
# prometheus.yml
scrape_configs:
  - job_name: blackbox
    metrics_path: /probe
    params: { module: [http_2xx] }
    static_configs: [{ targets: ["https://shop.example.com/health", "https://api.example.com/ready"] }]
    relabel_configs:
      - { source_labels: [__address__], target_label: __param_target }
      - { source_labels: [__param_target], target_label: instance }
      - { target_label: __address__, replacement: blackbox-exporter:9115 }
```
- Probers: HTTP/HTTPS (the `http` prober), DNS, TCP, ICMP and gRPC. Probe timeout comes from the Prometheus
  `scrape_timeout` (slightly reduced), further limited by the module `timeout`; default 120 s if neither is set.
- The three relabel rules are the **multi-target pattern**: the target becomes the `target` URL parameter, `instance`
  is set to it, and the scrape goes to the exporter. SNMP and IPMI exporters work the same way.
- `/probe?target=...&module=http_2xx` returns probe metrics, `probe_success` among them; add `debug=true` for
  debug output. Exporter-own metrics are at `/metrics`, which should be scraped as a separate job.

## 4. Writing a custom exporter
Rules from the official "Writing exporters" guide:
1. **Scrape-time collection.** Pull from the application only when Prometheus scrapes; no timers of your own, and no
   timestamps on metrics (needing timestamps suggests the Pushgateway). Caching is acceptable only for a metric that
   takes over a minute to fetch, noted in HELP. Prometheus's default scrape timeout is 10 s; document it if you can
   exceed it.
2. **Create new metrics on every scrape**, never update direct-instrumentation metrics: concurrent scrapes race, and
   vanished label values would still be exported. In Go use `MustNewConstMetric` in `Collect()`.
3. **Naming**: snake_case, prefixed with the exporter name (`haproxy_up`), base units matching the name, `_total` on
   counters, ratios not percentages, no colons (reserved for recording rules), no metric names that embed label names.
   Avoid `process_` and `scrape_` prefixes unless semantics match, and avoid the `_sum`, `_count`, `_bucket` suffixes
   unless you produce those types.
4. **Labels**: avoid `type`, and names that clash with target labels (`region`, `zone`, `cluster`, `env`, `service`,
   ...). Do not use `le` or `quantile` except for histograms and summaries. A metric should make sense when summed
   or averaged; never emit a `total` label value or an unlabelled total beside labelled series. Put infrastructure
   labels in Prometheus scrape config, not in the exporter.
5. **Types**: match counters and gauges; use UNTYPED when unsure; a counter that can decrease is a gauge.
6. **Scrape meta metrics**: gauges prefixed with the exporter name, e.g. `jmx_scrape_duration_seconds`. Avoid scrape
   counters and duration histograms (Prometheus already records them).
7. **Failed scrapes**: either return a 5xx, or expose `<exporter>_up` as 0 or 1. The `_up` form is better when some
   metrics are still available; the 5xx form works with the usual `up` but cannot tell exporter-down from
   application-down.
8. **Drop** other systems' machine and process metrics (use node_exporter) and 1m/5m/15m rates, means, min/max and
   standard deviations.
9. Work out of the box with config limited to where the application is; use YAML for configuration. Serve a simple
   landing page at `/` linking to `/metrics`.
10. Help strings should name the original metric and any transformation rule applied.

Python: see the client_python custom collectors documentation; Java: generate `MetricFamilySamples` in `collect`.

## 5. Shortcuts before writing code
- Dotted-name legacy sources (Graphite, StatsD): the Graphite and StatsD exporters share a small configuration language
  for extracting labels.
- Push-based sources (StatsD, Graphite, collectd): decide when to expire metrics; prefer raw counters over deltas.
- Batch jobs: push to the Pushgateway for service-level metrics; textfile collector for machine-level ones.
- Search the exporters page first; JMX exporter covers many JVM applications (for example Kafka and Cassandra).

## Verify
- [ ] The `/metrics` output passes a Prometheus metrics lint and includes `<exporter>_up` and a scrape duration gauge.
- [ ] Stopping the target makes `<exporter>_up` 0 (or the scrape 5xx) as designed.
- [ ] Scrape duration is well under the job's scrape timeout.
- [ ] Series count per scrape is bounded (no per-request or per-timestamp labels).

## Checked
Checked 2026-11-08 against prometheus.io "Exporters and integrations" and "Writing exporters" (read in full) and the
node_exporter and blackbox_exporter READMEs. Removed as not on those pages: the port numbers other than 9100 and 9115,
node_exporter key-metric names, the Kubernetes DaemonSet hostPID/hostNetwork detail, blackbox module option examples
(`valid_status_codes`, `fail_if_not_ssl`, dns/tcp module fields), probe metric names other than `probe_success`, the
Go and Python skeleton code, the `*_timestamp_seconds` staleness advice and specific exporter-name shortcuts
(json, script, sql, grok, mtail). Sample hostnames are placeholders.
Method: documentation only; no commands were run.
