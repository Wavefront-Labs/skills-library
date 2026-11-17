---
id: computing-software.devops-ci-cd.flagger.flagger-prometheus-metric-provider
name: flagger-prometheus-metric-provider
category: computing-software
field: devops-ci-cd
product: flagger
tags: [prometheus, metrictemplate, promql, authentication]
level: practitioner
status: docs-checked
description: "Query Prometheus from a Flagger MetricTemplate with PromQL, and authenticate with basic auth or a bearer token Secret."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/metrics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `provider.type: prometheus` and write the query in PromQL. Example: percentage of requests that are not 404s, failing the canary when 404s reach 5 percent:

```yaml
spec:
  provider:
    type: prometheus
    address: http://prometheus.istio-system:9090
  query: |
    100 - sum(rate(istio_requests_total{reporter="destination",
      destination_workload_namespace="{{ namespace }}",
      destination_workload="{{ target }}", response_code!="404"}[{{ interval }}]))
    / sum(rate(istio_requests_total{reporter="destination",
      destination_workload_namespace="{{ namespace }}",
      destination_workload="{{ target }}"}[{{ interval }}])) * 100
```

with `thresholdRange: {max: 5}` in the canary metric.

Authentication: create a Secret in the same namespace as the MetricTemplate, either with `username` and `password` (basic auth) or with `token` (bearer, for example a service account token), and point at it with `provider.secretRef.name`.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/metrics.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
