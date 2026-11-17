---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.beyla-configuration-discovery-and-network-metrics
name: beyla-configuration-discovery-and-network-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [beyla-configuration, beyla-discovery, beyla-network-metrics, beyla, ebpf]
level: advanced
status: docs-checked
description: "Configure Beyla: service discovery selectors, route decoration and cardinality, metric and trace exporters, Kubernetes attributes, and network flow metrics."
sources: ["https://grafana.com/docs/beyla/latest/configure/", "https://grafana.com/docs/beyla/latest/configure/service-discovery/", "https://grafana.com/docs/beyla/latest/network/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Beyla configuration

Config via YAML (`-config` / `BEYLA_CONFIG_PATH`) or `BEYLA_*`/`OTEL_*` env vars; env overrides file.

## Discovery
```yaml
discovery:
  instrument:                         # older versions: `services`
    - k8s_namespace: shop
      k8s_deployment_name: "checkout*"      # glob, not a regex
    - open_ports: 80,443,8000-8999
    - exe_path: "*java*"                  # glob against the full executable path
  exclude_instrument:
    - k8s_namespace: kube-system
  exclude_otel_instrumented_services: true    # skip apps already sending OTel
```
Selectors in one entry must all match; a process matching any entry is instrumented. `open_ports` takes a
comma-separated list of ports and ranges. Single process shortcut: `BEYLA_OPEN_PORT=8080` or `BEYLA_AUTO_TARGET_EXE`.
Without the (deprecated) `name:` selector property, the service name is the Deployment name, then the
ReplicaSet/DaemonSet/StatefulSet name, then the Pod name on Kubernetes, else the executable name. By default Beyla
excludes itself, Alloy and the OpenTelemetry Collector (`default_exclude_instrument`).

## Routes (cardinality control)
```yaml
routes:
  patterns: ["/api/orders/{id}", "/api/users/{id}/cart"]
  ignored_patterns: [/healthz, /metrics]
  unmatched: heuristic        # heuristic (default) | path | wildcard | unset
```
`patterns` use `:name` or `{name}` matchers. For paths matching no pattern, `unmatched: heuristic` (the default)
replaces numeric and non-word path components with `*`; `path` copies the raw path to `http.route` and can cause a
cardinality explosion; `wildcard` sets it to `/**`; `unset` leaves it unset. `ignore_mode` (`all`, `metrics`,
`traces`) controls what `ignored_patterns` discards.

## Exporters
```yaml
otel_metrics_export: {endpoint: http://alloy:4318, features: [application, application_span, application_service_graph]}
otel_traces_export:  {endpoint: http://alloy:4318, sampler: {name: parentbased_traceidratio, arg: "0.1"}}
prometheus_export:   {port: 9400, features: [application, network]}
attributes:
  kubernetes: {enable: true}
  select:
    http_server_request_duration_seconds:
      include: ["*"]
      exclude: ["server.address"]
```
The `application_span` and `application_service_graph` features produce span metrics and service graph metrics.
An exported signal needs its exporter configured, otherwise Beyla ignores it.

## Network metrics
```yaml
network:
  enable: true
  source: socket_filter        # default; or tc
  cidrs: [10.0.0.0/8]          # sets src.cidr / dst.cidr; narrowest match wins
attributes:
  select:
    beyla_network_flow_bytes:
      include: [k8s.src.owner.name, k8s.src.namespace, k8s.dst.owner.name, k8s.dst.namespace]
```
Produces `beyla_network_flow_bytes` (`beyla_network_flow_bytes_total` when exported through a Prometheus endpoint).
Use `socket_filter` when Cilium or another eBPF program uses Traffic Control filters (`tc` assumes none does).
Network metrics also need an exporter (`otel_metrics_export` or `prometheus_export`).

## Verify
Run with `BEYLA_LOG_LEVEL=debug` and check which processes Beyla selects and which exporters are active.

## Checked
Date: 2026-10-28. Confirmed against the Beyla configuration options, service discovery, export data, metrics/traces/attributes and network configuration pages and the Alloy `beyla.ebpf` reference: `-config` / `BEYLA_CONFIG_PATH` and env priority, selector properties and AND semantics, `k8s_deployment_name` and `exe_path` being globs, `open_ports` syntax, default service naming, default exclusions, `exclude_otel_instrumented_services`, `routes` fields and `unmatched` values, `network.source` default and Cilium note, `cidrs`, `attributes.select` for `beyla_network_flow_bytes`, `BEYLA_LOG_LEVEL`. Fixed: `k8s_deployment_name` is a glob (the skill used a regex), `allowed_attributes` does not exist (use `attributes.select`), `unmatched` default is `heuristic` and `unset` is a value, network `source` default is `socket_filter`. Removed unconfirmed internal-metrics names and the pods-x-pods series claim.
Method: documentation only; no commands were run.
