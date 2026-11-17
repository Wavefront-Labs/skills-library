---
id: computing-software.data-engineering.metabase.prometheus-monitoring
name: prometheus-monitoring
category: computing-software
field: data-engineering
product: metabase
tags: [prometheus, metrics-endpoint, mb-prometheus-server-port, scrape-config, jvm-metrics]
level: practitioner
status: docs-checked
description: "Expose Metabase metrics to Prometheus with MB_PROMETHEUS_SERVER_PORT: ports, scrape config, metric families and mismatched target gotchas."
sources:
  - https://www.metabase.com/docs/latest/installation-and-operation/observability-with-prometheus
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable: set `MB_PROMETHEUS_SERVER_PORT` to the port Prometheus will scrape; the docs use `9191`.
`MB_PROMETHEUS_SERVER_PORT=9191 java --add-opens java.base/java.nio=ALL-UNNAMED -jar metabase.jar`
Startup logs should show a collector and a web server starting on that port.

Ports: the Metabase app uses 3000 (change with `MB_JETTY_PORT`), the metrics endpoint uses the Prometheus server port setting, and Prometheus itself is on 9090.

Scrape config (`prometheus.yml`): the example sets global `scrape_interval: 15s`, a `prometheus` job at `5s` and target `localhost:9191`. Change the target to the host running Metabase. Start Prometheus with `./prometheus --config.file=prometheus.yml`.

Metric families:
- `jvm_*` (GC, memory, memory pools, threads such as `jvm_threads_current` and `jvm_threads_deadlocked`)
- `jetty_*`
- `c3p0_*` (connection pool)
- `process_*`
- `metabase_email_messages_total` and `metabase_email_message_errors_total`
- `metabase_security_center_last_sync_timestamp_seconds` and `metabase_security_center_vulnerable_advisories`

Gotchas:
- The scrape target port must match `MB_PROMETHEUS_SERVER_PORT`.
- When Prometheus and Metabase run on different machines, the target host must be the Metabase machine.
- The page shows a local example only, with no production hardening, and states no plan requirement.

## Checked
2026-11-03. Confirmed against the Metabase docs page Installation and operation, Observability with Prometheus: MB_PROMETHEUS_SERVER_PORT and the 9191 example, ports 3000/9191/9090 and MB_JETTY_PORT, startup log lines, prometheus.yml example (15s, 5s, localhost:9191), the prometheus run command, and the exported metric families listed. Nothing removed.
Method: documentation only; no commands were run.
