---
id: computing-software.cloud-infrastructure-engineering.knative.autoscaling-metrics-targets
name: autoscaling-metrics-targets
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [autoscaling-metric, autoscaling-target, rps-target, container-concurrency-target-default, requests-per-second]
level: practitioner
status: docs-checked
description: "Pick concurrency, rps, cpu or memory as the scaling metric and set its target."
sources:
  - https://knative.dev/docs/serving/autoscaling/autoscaling-metrics/
  - https://knative.dev/docs/serving/autoscaling/autoscaling-targets/
  - https://knative.dev/docs/serving/autoscaling/rps-target/
  - https://knative.dev/docs/serving/autoscaling/concurrency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide what drives scaling and at what level.

Metric, set per revision with `autoscaling.knative.dev/metric`:
- Default KPA supports `concurrency` (default) and `rps`.
- HPA supports `cpu`; `memory` and custom metric names also need the HPA class.

Target, set with `autoscaling.knative.dev/target`, an integer that is metric agnostic. Globally, `container-concurrency-target-default` defaults to `"100"`. The annotation has no default.

Requests-per-second target: the revision must use the `rps` metric. Global key `requests-per-second-target-default`, default `"200"`.

```yaml
metadata:
  annotations:
    autoscaling.knative.dev/metric: "rps"
    autoscaling.knative.dev/target: "150"
```

Global values live in the `config-autoscaler` ConfigMap in `knative-serving`:

```yaml
data:
  requests-per-second-target-default: "150"
```

or via the Operator:

```yaml
spec:
  config:
    autoscaler:
      requests-per-second-target-default: "150"
```

The target is metric agnostic: its unit follows the metric you chose. Other metrics are set the same way with a different `metric` annotation value.

Target utilization: `autoscaling.knative.dev/target-utilization-percentage` (global `container-concurrency-target-percentage`) scales early. The concurrency page documents the default as `70` (a float), but the default `config-autoscaler` example on the autoscaler types page shows `"0.7"`; the two official pages disagree, so check the ConfigMap in your cluster. With `containerConcurrency` 10 and 70 percent, a new replica starts when average concurrency reaches 7.

## Checked

2026-11-04. Confirmed against the autoscaling metrics, targets, requests-per-second target and concurrency pages (knative/docs source): `autoscaling.knative.dev/metric` values and the `concurrency` default, KPA supporting `concurrency` and `rps`, HPA class for `cpu`, `memory` and custom metrics, the integer metric-agnostic `target` annotation with no default, `container-concurrency-target-default` default `"100"`, `requests-per-second-target-default` default `"200"`, the example manifests, and the 10 x 70 percent = 7 worked example. Conflict between pages: the concurrency page gives the `target-utilization-percentage` default as `70`, while the autoscaler types page's default ConfigMap shows `container-concurrency-target-percentage: "0.7"`; the skill now says so. Added the three extra pages to sources.

Method: documentation only; no commands were run.
