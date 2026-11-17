---
id: computing-software.cloud-infrastructure-engineering.knative.autoscaler-types
name: autoscaler-types
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [autoscaler-class, kpa, hpa, autoscaling-knative-dev-class, pod-autoscaler-class]
level: practitioner
status: docs-checked
description: "Choose the Knative Pod Autoscaler or Kubernetes HPA with the class annotation."
sources:
  - https://knative.dev/docs/serving/autoscaling/autoscaler-types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right autoscaler implementation for a Revision.

Knative Serving supports two:

Knative Pod Autoscaler (KPA):
- Part of Serving core and on by default after install.
- Supports scale to zero.
- Does not support CPU-based autoscaling.

Horizontal Pod Autoscaler (HPA):
- Not part of Serving core; install it after Knative Serving.
- Does not support scale to zero.
- Supports CPU-based autoscaling.

Select with the class setting:
- Global ConfigMap key: `pod-autoscaler-class`
- Per-revision annotation: `autoscaling.knative.dev/class`
- Values: `"kpa.autoscaling.knative.dev"` or `"hpa.autoscaling.knative.dev"`
- Default: `"kpa.autoscaling.knative.dev"`

```yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/class: "hpa.autoscaling.knative.dev"
```

The same value can be set globally in the `config-autoscaler` ConfigMap in `knative-serving`, or through the Operator's `KnativeServing` resource under `spec.config.autoscaler`.

Global versus per-revision: with no per-revision settings the global ones apply; per-revision settings override global ones. Global settings live in the `config-autoscaler` ConfigMap. If you installed with the Operator, set them under `spec.config.autoscaler` in the `KnativeServing` custom resource.

## Checked

2026-11-03. Confirmed on the Knative Serving autoscaling/autoscaler-types page: KPA and HPA properties, class key, annotation, values and default, global versus per-revision rules. Removed: the metric-per-class sentence (not on the page).
Method: documentation only; no commands were run.
