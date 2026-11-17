---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-migrate-from-agent-static
name: grafana-alloy-migrate-from-agent-static
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [migrate-agent-static, integrations-next, configexpand-env, agent-management, extra-args]
level: practitioner
status: docs-checked
description: "Convert a Grafana Agent Static config to Alloy, with integrations-next and expand-env extra-args, and the limits around agent management and the gRPC server."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/set-up/migrate/from-static.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating from Grafana Agent Static

```shell
alloy convert --source-format=static --output=/path/to/config.alloy /path/to/agent.yaml
```
Then stop Grafana Agent Static and run Alloy with the new file. Use `--report` and `--bypass-errors` as with other sources. The expected warning is: review your agent command-line flags and set them where needed in Alloy. Alternatively run directly with `alloy run --config.format=static`.

## Components produced
Metrics become `prometheus.scrape` and `prometheus.remote_write`; logs become `local.file_match`, `loki.source.file`, `loki.process`, `loki.write`; traces become `otelcol.receiver.otlp`, `otelcol.processor.batch`, `otelcol.exporter.otlp`.

## Extra args
- Integrations next: `--extra-args="-enable-features=integrations-next"` for `convert`, or `--config.extra-args=...` for `run`.
- Environment variables: `--extra-args="-config.expand-env"`.
- Combine them in one quoted string separated by a space: `--extra-args="-enable-features=integrations-next -config.expand-env"`.

## Limitations
- Agent Management options cannot be converted.
- Alloy has no gRPC server; any non-default gRPC server setting is reported as unsupported.
- Check agent CLI flags such as `-server.http.address` and any environment variables used.
- The metrics and logs sections inherit the Prometheus and Promtail limitations.

## Checked

2026-11-04. Confirmed against the Migrate from Grafana Agent Static page (set-up/migrate/from-static.md): convert and run --config.format=static commands, produced components, extra-args, limitations list. Removed the parenthetical on renamed meta-metrics, which the page does not state for this source.

Method: documentation only; no commands were run.
