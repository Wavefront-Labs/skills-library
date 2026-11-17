---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.scrapeconfig-crd
name: scrapeconfig-crd
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-operator, scrapeconfig-crd, static-configs, external-targets, file-sd, http-sd, additional-scrape-configs]
level: practitioner
status: docs-checked
description: "Scrape targets outside Kubernetes with the ScrapeConfig CRD (static, file, HTTP, DNS, Consul, EC2 SD), replacing additionalScrapeConfigs Secrets."
sources: ["https://prometheus-operator.dev/docs/developer/scrapeconfig/", "https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1alpha1.ScrapeConfig"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ScrapeConfig CRD

ScrapeConfig (prometheus-operator v0.65.x and later; the CRD must be installed and the operator restarted after it
is created or updated) scrapes targets external to the Kubernetes cluster, or builds scrape configurations the
higher-level ServiceMonitor/PodMonitor/Probe resources cannot express. It is a typed, per-team object.

```yaml
apiVersion: monitoring.coreos.com/v1alpha1
kind: ScrapeConfig
metadata:
  name: legacy-vms
  namespace: monitoring
  labels: {release: kube-prometheus-stack}     # must match the Prometheus scrapeConfigSelector
spec:
  scrapeInterval: 30s
  staticConfigs:
    - targets: ["vm1.example.net:9100", "vm2.example.net:9100"]
      labels: {env: prod, role: db}
---
apiVersion: monitoring.coreos.com/v1alpha1
kind: ScrapeConfig
metadata: {name: cmdb-targets, namespace: monitoring, labels: {release: kube-prometheus-stack}}
spec:
  httpSDConfigs:
    - url: http://cmdb-exporter.example.net/targets
      refreshInterval: 2m
  metricsPath: /metrics
  basicAuth:
    username: {name: scrape-creds, key: user}
    password: {name: scrape-creds, key: password}
```
Service discovery blocks: tier 1 (fully supported) are `kubernetesSDConfigs`, `fileSDConfigs`, `staticConfigs`,
`dnsSDConfigs` and `httpSDConfigs`. Tier 2 (maintainers review issues and PRs but do not actively maintain) covers
cloud providers such as `azureSDConfigs`, `ec2SDConfigs` and `gceSDConfigs`; `consulSDConfigs` also exists (see the
API reference for the full list). `fileSDConfigs` files must be mounted into the Prometheus pods (for example a ConfigMap listed
in the Prometheus `spec.configMaps`, then `/etc/prometheus/configmaps/<name>/<file>`).

`kubernetesSDConfigs` needs only a `role` (`Node`, `Pod`, `Service`, `Endpoints`, `EndpointSlice` or `Ingress`,
capitalised); prefer ServiceMonitor, PodMonitor or Probe where they cover the case. The Prometheus service account
needs get, list and watch on the discovered resources.

## Enable selection
Prometheus and PrometheusAgent both have `spec.scrapeConfigSelector` (for example `matchLabels`).
Without `scrapeConfigNamespaceSelector` only ScrapeConfigs in the Prometheus's own namespace are selected; set it to
`{}` for all namespaces, or `matchLabels` to pick namespaces by label. kube-prometheus-stack exposes the selector as
`prometheus.prometheusSpec.scrapeConfigSelector`.

## Gotchas
- Dashboards that filter on a particular `job` value need a `jobName` or relabeling to produce it; check `/targets`
  for the job name the operator generated.
- The API is `v1alpha1`; check field names against your operator release.

## Verify
- [ ] `/targets` shows the ScrapeConfig targets up.
- [ ] Operator logs show no rejection of the ScrapeConfig.

## Checked
2026-10-31. Confirmed against the prometheus-operator ScrapeConfig developer guide (minimum operator version, selector
and namespace selector behaviour, tier-1 and tier-2 service discovery lists, `kubernetesSDConfigs` roles, file_sd
mounting path, http_sd `refreshInterval`) and the v1alpha1 API reference (`staticConfigs`, `fileSDConfigs`,
`httpSDConfigs`, `kubernetesSDConfigs`, `consulSDConfigs`, `dnsSDConfigs`, `ec2SDConfigs`, `azureSDConfigs`,
`gceSDConfigs`, `metricsPath`, `jobName`, `basicAuth`). Removed: the generated job-name format, the "nil selector
selects nothing" claim, the operator log message text, the claim that ScrapeConfigs replaced shared Secrets without
validation, and the placeholder IP addresses.
Method: documentation only; no commands were run.
