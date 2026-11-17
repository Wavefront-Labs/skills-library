---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-runtime-configuration
name: grafana-mimir-runtime-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [runtime-config, overrides, per-tenant-limits, reload, ingester-limits]
level: practitioner
status: docs-checked
description: "Explains Mimir runtime configuration files: enabling, reload period, merging, per-tenant limit overrides and dynamic instance limits for ingesters and distributors."
sources: ["https://grafana.com/docs/mimir/latest/configure/about-runtime-configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Runtime configuration

A runtime configuration file is reloaded periodically while Mimir runs, so a subset of settings can change without restarting a component. Runtime values take precedence over command-line options.

## Enable

Set `-runtime-config.file=<filepath>,<filepath>` or the `runtime_config` YAML block. Files are reloaded every 10 seconds by default (`-runtime-config.reload-period`) and merged left to right. A `.gz` extension means the file is decompressed before YAML parsing. On Kubernetes store the files in a ConfigMap mounted into each container.

View current values at `/runtime_config`; add `?mode=diff` to show only non-default values.

## Per-tenant limits

The `limits` block sets defaults for all tenants; `overrides` changes them per tenant.

```yaml
overrides:
  tenant1:
    ingestion_rate: 50000
  tenant2:
    ingestion_rate: 75000
```

Any limit in the `limits` block can be overridden, each tenant can override different limits, and unlisted limits are inherited.

## Instance limits

Everything under the ingester and distributor `instance_limits` blocks can be changed dynamically:

```yaml
ingester_limits:
  max_ingestion_rate: 20000
  max_series: 1500000
  max_tenants: 1000
  max_inflight_push_requests: 30000
distributor_limits:
  max_ingestion_rate: 75000
  max_inflight_push_requests: 1500
  max_inflight_push_requests_bytes: 314572800
```

These protect individual instances regardless of per-tenant limits.

## Checked

Confirmed precedence over command-line options, the enable flag and YAML block, the 10 second default reload, left-to-right merging, the .gz rule, the ConfigMap advice, the /runtime_config endpoint, the per-tenant override behaviour and both instance limit examples. Nothing removed.

Method: docs-checked 2026-11-09 against the raw grafana/mimir docs page about-runtime-configuration.md, read in full.
