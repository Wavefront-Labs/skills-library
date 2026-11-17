---
id: computing-software.cloud-infrastructure-engineering.kubernetes.blackbox-exporter-probe-crd
name: blackbox-exporter-probe-crd
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, prometheus-operator, blackbox-exporter, probe-crd, synthetic-monitoring, tls-expiry]
level: practitioner
status: docs-checked
description: "Probe HTTP, TCP and TLS endpoints with blackbox exporter through the Prometheus Operator Probe CRD, and alert on failures, latency and certificate expiry."
sources: ["https://github.com/prometheus/blackbox_exporter", "https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.Probe", "https://raw.githubusercontent.com/prometheus/blackbox_exporter/master/CONFIGURATION.md", "https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/prometheus-blackbox-exporter/values.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Probe CRD with blackbox exporter

## Install the exporter
```bash
helm install blackbox prometheus-community/prometheus-blackbox-exporter -n monitoring \
  --set config.modules.http_2xx.prober=http \
  --set config.modules.http_2xx.http.preferred_ip_protocol=ip4
```
Modules define how to probe; each has a prober (`http`, `tcp`, `dns`, `icmp`, `grpc`, ...), and the exporter's
`example.yml` names modules such as `http_2xx` and `tcp_connect`.

## Probe resource
```yaml
apiVersion: monitoring.coreos.com/v1
kind: Probe
metadata:
  name: public-endpoints
  namespace: monitoring
  labels: {release: kube-prometheus-stack}
spec:
  interval: 30s
  module: http_2xx
  prober:
    url: blackbox-prometheus-blackbox-exporter.monitoring.svc:9115   # Service name and port: check `kubectl get svc -n monitoring`
  targets:
    staticConfig:
      static:
      - https://shop.example.com/healthz
      - https://api.example.com/ready
      labels: {team: web}
```
`targets.ingress` configures a target for each host/path of the Ingress objects it selects, instead of a
static list. `prober.url` is required. The Prometheus resource needs a matching `probeSelector`.

## Alerts
```promql
probe_success == 0                                              # for: 2m
probe_duration_seconds > 2
(probe_ssl_earliest_cert_expiry - time()) / 86400 < 14
probe_http_status_code >= 500
```

## Notes
- Probing from inside the cluster tests in-cluster DNS and routing, not what users see; add an
  external probe (another region or a SaaS) for user-facing SLOs.
- For internal CAs use a separate module with `tls_config` (for example a CA file). `fail_if_ssl` makes a
  probe fail when SSL *is* present; it is not a verification switch.

## Verify
In Prometheus, `probe_success{instance="https://shop.example.com/healthz"}` returns 1.

## Checked
2026-10-28. Confirmed: Probe fields (`prober.url`, `module`, `targets.staticConfig.static`/`labels`,
`targets.ingress`) and `probeSelector` against the Prometheus Operator API reference; the chart's
`config.modules.http_2xx` values, `preferred_ip_protocol` and Service port 9115 against the chart
`values.yaml`; prober types, `fail_if_ssl` semantics and `tls_config` against `CONFIGURATION.md`; module names
against `example.yml`; `probe_success`, `probe_duration_seconds`, `probe_http_status_code` and
`probe_ssl_earliest_cert_expiry` against the exporter README and source. Removed: the earlier `fail_if_ssl:
false` advice (it does not select internal CAs) and the ingress "discover hosts" wording.
Method: documentation only; no commands were run.
