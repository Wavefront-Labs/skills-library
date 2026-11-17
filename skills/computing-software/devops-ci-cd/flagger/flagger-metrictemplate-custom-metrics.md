---
id: computing-software.devops-ci-cd.flagger.flagger-metrictemplate-custom-metrics
name: flagger-metrictemplate-custom-metrics
category: computing-software
field: devops-ci-cd
product: flagger
tags: [metrics, metrictemplate, custom-metrics, templatevariables]
level: practitioner
status: docs-checked
description: "Write a Flagger MetricTemplate with a provider and query, reference it with templateRef and pass templateVariables."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/metrics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `MetricTemplate` connects Flagger to a metric provider and runs a query that returns a `float64`, which is validated against the threshold range.

```yaml
apiVersion: flagger.app/v1beta1
kind: MetricTemplate
metadata:
  name: my-metric
spec:
  provider:
    type: prometheus      # prometheus, datadog, etc
    address: http://prometheus.linkerd-viz:9090
    insecureSkipVerify: false
    secretRef:
      name: api-credentials
  query: |
    histogram_quantile(0.99, sum(rate(response_latency_ms_bucket{
      namespace="{{ namespace }}", deployment=~"{{ target }}",
      direction="{{ variables.direction }}"}[{{ interval }}])) by (le))
```

Query variables: `name`, `namespace`, `target` (targetRef.name), `service`, `ingress`, `interval` (the metric interval) and `variables` (the metric `templateVariables`).

Reference it from the analysis:

```yaml
metrics:
  - name: "my metric"
    templateRef:
      name: my-metric
      namespace: flagger     # optional, defaults to the canary namespace
    thresholdRange:
      min: 10
      max: 1000
    interval: 1m
    templateVariables:
      direction: inbound
```

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/metrics.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
