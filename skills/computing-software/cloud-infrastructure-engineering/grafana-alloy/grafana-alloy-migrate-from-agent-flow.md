---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-migrate-from-agent-flow
name: grafana-alloy-migrate-from-agent-flow
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [migrate-agent-flow, storagepath, data-alloy, modulefile, import-blocks, live-migration]
level: advanced
status: docs-checked
description: "Live migration from Grafana Agent Flow v0.40 or later to Alloy: renamed defaults, removed module.* components, data directory copy and cutover order."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/set-up/migrate/from-flow.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating from Grafana Agent Flow

Required only for live migrations; for a fresh start just uninstall Flow and install Alloy. You need Flow v0.40 or later, and autoscaling disabled until the migration finishes.

## Differences
- `--storage.path` default changed from `data-agent/` to `data-alloy/`.
- `--server.http.memory-addr` default changed from `agent.internal:12345` to `alloy.internal:12345`.
- Debug metrics are prefixed `alloy_` instead of `agent_`.
- Classic modules `module.file`, `module.git`, `module.http` and `module.string` are replaced by `import.*` blocks.
- `prometheus.exporter.vsphere` is replaced by `otelcol.receiver.vcenter` (experimental, so run with `--stability.level=experimental`).

## Steps
1. Deploy Alloy with the same topology and flags as Flow. On Kubernetes rename the `agent` key to `alloy` in `values.yaml`. For clusters match the instance count and keep autoscaling off.
2. Copy the contents of the Flow data directory into the Alloy one (on Linux from `/var/lib/grafana-agent-flow` to `/var/lib/alloy/data`; for Kubernetes use `kubectl cp` and mind `agent.storagePath` versus `alloy.storagePath`).
3. Move pipelines that receive network data first (for example `otelcol.receiver.otlp`, `prometheus.receive_http`) and repoint applications to Alloy.
4. Disable the remaining pipelines in Flow, then configure them in Alloy. Configuring them in Alloy first removes downtime but sends duplicate data during the overlap.
5. Uninstall Flow and re-enable autoscaling.

## Checked

2026-11-04. Confirmed against the Migrate from Grafana Agent Flow page (set-up/migrate/from-flow.md): version and autoscaling prerequisites, changed defaults, import.* replacements, vcenter stability level, data directory paths, step order. No claims changed.

Method: documentation only; no commands were run.
