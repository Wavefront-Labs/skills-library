---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.deploying-beyla-daemonset-or-sidecar
name: deploying-beyla-daemonset-or-sidecar
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [beyla-daemonset, beyla-helm, beyla, ebpf, auto-instrumentation]
level: practitioner
status: docs-checked
description: "Deploy Grafana Beyla eBPF auto-instrumentation on Kubernetes: Helm DaemonSet, sidecar with shared PID namespace, required capabilities, and Alloy beyla.ebpf."
sources: ["https://grafana.com/docs/beyla/latest/setup/kubernetes-helm/", "https://grafana.com/docs/beyla/latest/setup/kubernetes/", "https://grafana.com/docs/beyla/latest/security/", "https://grafana.com/docs/beyla/latest/", "https://grafana.com/docs/alloy/latest/reference/components/beyla/beyla.ebpf/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying Beyla as DaemonSet or sidecar

Beyla uses eBPF to instrument HTTP/S and gRPC services without code changes, exporting OpenTelemetry data and native
Prometheus metrics. It needs Linux kernel 5.8 or higher with BTF enabled (RHEL-based 8 distributions ship a 4.18
kernel with backported eBPF patches and are supported). HTTP-header trace context propagation needs kernel 5.17 or higher.

## DaemonSet via Helm (one Beyla per node)
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm install beyla -n beyla --create-namespace grafana/beyla
```
Defaults: Prometheus metrics on Pod port 9090, path `/metrics`; tries to instrument all applications in the cluster;
application-level metrics only (network metrics are off); metrics are decorated with Kubernetes metadata labels.

Override with a values file; `config.data` holds the Beyla configuration file:
```yaml
config:
  data:
    discovery:
      instrument:
        - k8s_namespace: shop
service:
  enabled: true
serviceMonitor:
  enabled: true
```
```bash
helm upgrade beyla grafana/beyla -f helm-beyla.yml
```
Set `honor_labels: true` on the Prometheus scrape config to keep the per-process `instance` labels Beyla sets. Pass
Grafana Cloud OTLP credentials through `envValueFrom` with a Kubernetes Secret (`OTEL_EXPORTER_OTLP_HEADERS`), not inline.

DaemonSet mode needs `hostPID: true` so Beyla sees all host processes, plus the capabilities below.

## Sidecar (when you cannot run node-wide pods)
```yaml
spec:
  shareProcessNamespace: true
  containers:
    - name: app
      image: shop/checkout
    - name: beyla
      image: grafana/beyla:<VERSION>
      securityContext:
        runAsUser: 0
        capabilities: {add: [BPF, PERFMON, NET_RAW, SYS_PTRACE, CHECKPOINT_RESTORE, DAC_READ_SEARCH]}
      env:
        - {name: BEYLA_OPEN_PORT, value: "8080"}
        - {name: OTEL_EXPORTER_OTLP_ENDPOINT, value: "<OTLP_ENDPOINT>"}
```
The process namespace must be shared between all containers of the Pod. `BEYLA_OPEN_PORT` selects the process by open
port (comma-separated ports and ranges). Capability roles per the Beyla security page: `BPF` general BPF and socket
filters, `NET_RAW` raw sockets for socket filters, `PERFMON` loading probes, `DAC_READ_SEARCH` and `CHECKPOINT_RESTORE`
reading `/proc`, `SYS_PTRACE` reading executables; `NET_ADMIN` is needed for the TC programs used by network flow capture
and trace context propagation. If `kernel.perf_event_paranoid` is above 2 (Debian-based distributions use 3), use
`SYS_ADMIN` instead of `PERFMON` or lower the setting. `privileged: true` also works but is broader than needed.

## Alloy
`beyla.ebpf "default" { ... }` runs Beyla inside Alloy; its `targets` export feeds `prometheus.scrape`. In Kubernetes,
set `hostPID: true`. The Alloy docs recommend running as root with `privileged: false` and only the required
capabilities (this keeps seccomp and AppArmor active); `privileged: true` is documented as not recommended for production.

## Gotchas
- Context propagation across services is off by default (`context_propagation` defaults to "disabled"); enable it in the
  `ebpf` block, or rely on the applications' own trace headers.
- Pin an image version.

## Checked
Date: 2026-10-28. Confirmed against the Beyla overview, Kubernetes setup, Helm, security and configuration options pages and the Alloy `beyla.ebpf` reference: kernel and BTF requirements, RHEL 4.18, Helm install command and defaults, `config.data`, `serviceMonitor`, `honor_labels`, `envValueFrom`, `hostPID`, `shareProcessNamespace`, capability list and roles, `BEYLA_OPEN_PORT`, `context_propagation` default, Alloy privilege guidance. Fixed: the skill said Alloy must be privileged; the docs recommend unprivileged root with specific capabilities. Removed unconfirmed claims: OBI donation date, Kafka/SQL/Redis coverage, Helm chart setting `hostPID` itself, `prometheus_export` and `otel_traces_export` keys, metric names, the log grep, and the Autopilot/Fargate and `latest` statements.
Method: documentation only; no commands were run.
