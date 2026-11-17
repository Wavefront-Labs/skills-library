---
id: computing-software.cloud-infrastructure-engineering.contour.contour-metrics-and-health-listeners
name: contour-metrics-and-health-listeners
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [metrics, prometheus, server-certificate-path, om-enforced-health-listener, overload-max-heap, bootstrap-flags, port-8000, port-8002]
level: advanced
status: docs-checked
description: "Contour metrics server parameters (ports, TLS, client CA), overload-manager enforced health listener, and contour bootstrap flags for Envoy xDS connection."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour metrics endpoints and bootstrap flags

`metrics` has `contour` and `envoy` sub-blocks:

```yaml
metrics:
  contour:
    address: 0.0.0.0
    port: 8000
    server-certificate-path: /path/to/server-cert.pem
    server-key-path: /path/to/server-private-key.pem
    ca-certificate-path: /path/to/root-ca-for-client-validation.pem
  envoy:
    port: 8002
```

Defaults: address `0.0.0.0`, port 8000 (Contour) and 8002 (Envoy). Metrics are served over HTTPS when certificate and key paths are both set; `ca-certificate-path` enables client-certificate verification. Metrics and health endpoints cannot share a port when HTTPS is on.

`omEnforcedHealthListener` (address, port; disabled by default) adds a health listener that enforces overload manager limits such as max global downstream connections, so readiness can fail (load-shedding) without failing liveness.

`contour bootstrap` (run by the Envoy daemonset initContainer) flags:
- `--xds-address` (127.0.0.1), `--xds-port` (8001), `--xds-resource-version` (v3 only).
- `--envoy-cafile`, `--envoy-cert-file`, `--envoy-key-file` for secure xDS.
- `--admin-address` (unix socket `/admin/admin.sock`), `--namespace` (projectcontour).
- `--dns-lookup-family` (auto), `--log-format`.
- `--overload-max-heap` (>0 enables overload manager, shrinks heap at 95%) and `--overload-downstream-max-conn` (global downstream connection cap).

## Checked

2026-11-04. Confirmed against the Contour Configuration Reference (configuration.md): the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
