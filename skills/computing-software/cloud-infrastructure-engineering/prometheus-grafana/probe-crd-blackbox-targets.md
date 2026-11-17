---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.probe-crd-blackbox-targets
name: probe-crd-blackbox-targets
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-operator, probe-crd, blackbox-probe-crd, blackbox-exporter, uptime-checks, ingress-probing]
level: practitioner
status: docs-checked
description: "Probe URLs and ingresses through blackbox_exporter with the Probe CRD: prober spec, static and ingress targets, module choice, and alerting on probe_success."
sources: ["https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.Probe", "https://github.com/prometheus/blackbox_exporter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Probe CRD for blackbox targets

Prerequisite: a blackbox_exporter Service whose config defines the modules you reference (for example `http_2xx`).

```yaml
apiVersion: monitoring.coreos.com/v1
kind: Probe
metadata:
  name: public-endpoints
  namespace: monitoring
  labels: {release: kube-prometheus-stack}          # must match the Prometheus probeSelector
spec:
  jobName: blackbox-http
  interval: 30s
  scrapeTimeout: 10s
  module: http_2xx
  prober:
    url: blackbox-exporter.monitoring.svc:9115      # address:port, no scheme
    path: /probe                                    # default
  targets:
    staticConfig:
      static: [https://shop.example.com/healthz, https://api.example.com/healthz]
      labels: {env: prod}
    # or discover from Ingress objects:
    # ingress:
    #   selector: {matchLabels: {probe: "true"}}
    #   namespaceSelector: {any: true}
```
- `prober.url` is required and must be `address:port` without a scheme (a separate `scheme` field carries it).
- `interval` defaults to the Prometheus global scrape interval; `scrapeTimeout` defaults to the global scrape timeout
  and must not exceed the interval or the operator rejects the resource.
- If both `staticConfig` and `ingress` are set, `staticConfig` takes precedence.

## Alerts
```yaml
- alert: EndpointDown
  expr: probe_success{job="blackbox-http"} == 0
  for: 3m
```
Useful series: `probe_success`, `probe_duration_seconds`. For certificate expiry alerts, see the certificate-expiry skill.

## Gotchas
- Probing from inside the cluster tests cluster networking, not the user path; add external synthetic checks.

## Verify
- [ ] `/targets` lists the probe job with `instance` set to each target URL.
- [ ] `probe_success` is 1; stopping a test endpoint fires EndpointDown after the `for` period.

## Checked
2026-10-31. Confirmed against the prometheus-operator v1 Probe API reference (`jobName`, `module`, `prober.url`
address:port form and `prober.path` default `/probe`, `interval`, `scrapeTimeout` rule, `targets.staticConfig` and
`targets.ingress` precedence) and the blackbox_exporter README (module config, `probe_success`). Removed: the generated
job-name path, relabeling internals, ingress-host behaviour, extra `probe_http_*` series names and the TLS expiry rule
(not on the cited pages), and the chart-name and timeout-overlap claims.
Method: documentation only; no commands were run.
