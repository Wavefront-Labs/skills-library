---
id: computing-software.cloud-infrastructure-engineering.thanos.querier-endpoint-service-discovery
name: querier-endpoint-service-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-query, endpoint-sd, file-sd, per-endpoint-tls]
level: practitioner
status: docs-checked
description: "Discover StoreAPI endpoints through file service discovery and override TLS per endpoint."
sources: ["https://thanos.io/tip/components/query.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Querier endpoint discovery and per-endpoint TLS

The flag `--store.sd-files` (marked deprecated in the flag list) points to a JSON or YAML file in Prometheus target format:

```yaml
- targets:
    - prometheus-0.thanos-sidecar:10901
    - thanos-store:10901
```

The newer `--endpoint.sd-config-file` (or inline `--endpoint.sd-config`) allows richer per-endpoint settings; `--endpoint.sd-config-reload-interval` defaults to 5m. Static `--endpoint`, `--endpoint-group`, `--endpoint-strict` and `--endpoint-group-strict` are marked deprecated. A `dns+` or `dnssrv+` scheme prefix triggers DNS discovery; `--endpoint-strict` addresses are always used even when health checks fail, which helps with a caching layer on top.

**Per-endpoint TLS.** In the SD file, `default_client_config` supplies defaults and each `endpoints[].client_config` overrides them:

```yaml
default_client_config:
  tls_config: { enabled: true, ca_file: "/path/to/ca.pem" }
endpoints:
  - address: "store-a:10901"
    client_config:
      tls_config: { enabled: false }
```

Per-endpoint settings win; there is no per-endpoint TLS override for endpoints from DNS discovery or static CLI options. Omit a key to inherit it, or set it to an empty string to unset the global value. `compression` accepts `none` or `snappy`. `--store.unhealthy-timeout` (default 5m) removes an unhealthy store from the UI.

## Checked

2026-11-03. Confirmed against the Thanos Query page (components/query.md): API parameters and defaults, deduplication algorithms (penalty default, chain), partial response strategies (abort default), endpoint flags and per-endpoint TLS, PromQL engine and distributed mode, tenancy flags, sub-path prefixing. Fixed: --store.sd-files is marked deprecated; per-endpoint TLS does not apply to DNS or static endpoints; partial-response default wording. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
