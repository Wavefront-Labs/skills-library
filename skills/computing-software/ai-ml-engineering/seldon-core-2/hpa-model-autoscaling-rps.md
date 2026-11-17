---
id: computing-software.ai-ml-engineering.seldon-core-2.hpa-model-autoscaling-rps
name: hpa-model-autoscaling-rps
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, hpa, model-autoscaling, infer-rps, averagevalue, horizontalpodautoscaler, object-metric]
level: advanced
status: docs-checked
description: "Autoscale a Seldon Core 2 Model with an autoscaling/v2 HPA on the infer_rps Object metric: why spec.replicas is needed, AverageValue only, the replica formula, label selectors."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/scaling/model-hpa-autoscaling.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Model autoscaling with HPA

Deploy the Model without `minReplicas` or `maxReplicas` so native lag-based scaling does not interact with HPA, but you must set `spec.replicas`, the key HPA modifies. Without it HPA does nothing.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: irisa0-model-hpa
  namespace: seldon-mesh
spec:
  scaleTargetRef:
    apiVersion: mlops.seldon.io/v1alpha1
    kind: Model
    name: irisa0
  minReplicas: 1
  maxReplicas: 3
  metrics:
  - type: Object
    object:
      metric:
        name: infer_rps
      describedObject:
        apiVersion: mlops.seldon.io/v1alpha1
        kind: Model
        name: irisa0
      target:
        type: AverageValue
        averageValue: 3
```

## Rules
- Only `AverageValue` is supported, not `Value`. The target replicas are `infer_rps / averageValue`, for example 150 / 50 gives 3, which does not need the pod count. That is what lets separate HPAs target a Model and a Server.
- `describedObject` can be any resource in the adapter `resources` section; it fills the GroupBy and label matchers of the query.
- Filter by label with `metric.selector.matchLabels`, for example `method_type: rest` to count only REST traffic.
- Tune rates with HPA `behavior` scaling policies.
- Each HPA samples about every 15 seconds.

If a model scales before its Server, it shows `ScheduleFailed` for the new replicas but existing replicas keep serving. Pair with native Server autoscaling.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/scaling/model-hpa-autoscaling.md (read in full).
