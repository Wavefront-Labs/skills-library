---
id: computing-software.cloud-infrastructure-engineering.cert-manager.prometheus-metrics
name: prometheus-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [prometheus, metrics, podmonitor, metrics-tls, port-9402, venafi-metrics, mixin]
level: practitioner
status: docs-checked
description: "Scrape cert-manager metrics: port 9402, Helm PodMonitor values, TLS on the metrics endpoint (static or dynamic), troubleshooting and the Venafi metrics."
sources:
  - https://cert-manager.io/docs/devops-tips/prometheus-metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The controller, webhook and cainjector each serve `/metrics` on Pod port `9402` (port name `http-metrics`). The page documents a PodMonitor (Prometheus Operator), not a ServiceMonitor.

Helm: `prometheus.enabled: true`, `prometheus.podmonitor.enabled: true`; extra endpoint settings (for example `scheme: https`, `tlsConfig`) go in `prometheus.podmonitor.endpointAdditionalProperties`. A manual PodMonitor in `cert-manager` uses `jobLabel: app.kubernetes.io/name` and selects the name, instance and component labels of the three components.

TLS on metrics:
- Static: flags `--metrics-tls-cert-file` and `--metrics-tls-private-key-file`, or config `metricsTLSConfig.filesystem.certFile`/`keyFile` (Helm `config`, `webhook.config`, `cainjector.config`). Mount the files into the Pod; changes are reloaded without downtime.
- Dynamic: flags `--metrics-dynamic-serving-ca-secret-namespace`, `--metrics-dynamic-serving-ca-secret-name`, `--metrics-dynamic-serving-dns-names`, or config `metricsTLSConfig.dynamic.secretNamespace`, `secretName`, `dnsNames`. It creates Secret `cert-manager/cert-manager-metrics-ca`, which the PodMonitor reads via `tlsConfig.ca.secret` key `tls.crt`. All Pods share one DNS name, which must also be the PodMonitor `serverName`. Rotation is automatic.

Troubleshooting: `kubectl -n cert-manager logs -l app.kubernetes.io/instance=cert-manager --prefix`; port-forward the webhook on 9402 and `curl --insecure https://localhost:9402/metrics`; check target health in Prometheus.

Venafi metrics from the controller: `certmanager_venafi_oauth_token_requests_total` (counter, label `status` of `success` or `failure`) and `certmanager_venafi_oauth_token_request_duration_seconds` (histogram).

Alerts and dashboards: the Jsonnet `cert-manager-mixin`.

## Checked

2026-11-03: Confirmed against the Prometheus Metrics page: port 9402 on controller, webhook and cainjector, PodMonitor with `http-metrics`, Helm `prometheus.enabled` and `prometheus.podmonitor.enabled`, `endpointAdditionalProperties` example, static TLS flags and `metricsTLSConfig.filesystem` keys with reload on change, dynamic TLS flags and config keys, the `cert-manager/cert-manager-metrics-ca` Secret and shared DNS name, the troubleshooting commands, the two Venafi metrics with labels, and the monitoring mixin. Nothing removed.

Method: documentation only; no commands were run.
