---
id: computing-software.cloud-infrastructure-engineering.cortex.overrides-exporter
name: overrides-exporter
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [overrides-exporter, metrics, tenant-limits, runtime-config]
level: practitioner
status: docs-checked
description: "Expose per-tenant limits as Prometheus metrics with the overrides-exporter module to see how close tenants are to their limits."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/overrides-exporter.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cortex applies per-tenant limits, which can be overridden in the `runtime_config` file reloaded periodically (set via the `runtime_config` section or `-runtime-config.file`). The `overrides-exporter` module turns those limits into Prometheus metrics so operators can compare them with actual usage.

It is not enabled by default. Run only one instance in the cluster because of the cardinality of the metrics it emits.

Example runtime file with a single tenant override:

```yaml
overrides:
  "user1":
    ingestion_burst_size: 350000
    ingestion_rate: 350000
    max_global_series_per_user: 300000
```

Start it with:

```
cortex -target overrides-exporter -runtime-config.file runtime.yaml -server.http-listen-port=8080
```

Then `curl -s http://localhost:8080/metrics | grep cortex_overrides` shows series per tenant and limit name.

The output is a gauge `cortex_overrides` labelled with `limit_name` and `user`, for example `cortex_overrides{limit_name="ingestion_rate",user="user1"} 350000`. With these metrics you can alert on tenants close to their limits before they exceed them. Before v1.20.0 the exporter exposed only a fixed hardcoded list of limits. From v1.20.0 it discovers every numerically representable field of `limits_config`: numbers convert directly to float64, booleans become 1.0 or 0.0, and durations become seconds (1h is 3600.0). Strings, slices, maps and nested structs such as `metric_relabel_configs` are ignored.

## Checked

2026-11-04. Claims were read against the Cortex docs page: Overrides Exporter guide (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
