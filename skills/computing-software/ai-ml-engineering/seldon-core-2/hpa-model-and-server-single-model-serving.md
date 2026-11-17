---
id: computing-software.ai-ml-engineering.seldon-core-2.hpa-model-and-server-single-model-serving
name: hpa-model-and-server-single-model-serving
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, hpa, server-autoscaling, single-model-serving, coordinated-scaling, custom-metrics]
level: advanced
status: docs-checked
description: "Scale a Seldon Core 2 Model and its Server together with two HPAs on the same infer_rps metric for one-to-one serving, with custom metrics only and no multi-model serving."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/scaling/single-model-serving-hpa.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Model and Server autoscaling with HPA

For single-model serving, where each Server hosts exactly one Model replica (1:1 mapping). Use two HPAs on the same custom metric, applied together, and keep `minReplicas`, `maxReplicas` and policies in sync.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mlserver-server-hpa
  namespace: seldon-mesh
spec:
  scaleTargetRef:
    apiVersion: mlops.seldon.io/v1alpha1
    kind: Server
    name: mlserver
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

The Model HPA is the one from the model autoscaling skill. Note the Server HPA describes the Model, so both react to the same value.

## Constraints
- Only Prometheus custom metrics, not CPU or memory: each HPA must exclusively control a set of pods, and the Model and Server need different selectors.
- No multi-model serving.
- The scheduler does not create Server replicas here. A Model asking for more replicas than the Server has shows `ScheduleFailed` until HPA adds Server replicas.

## Practice
Create both HPAs at the same time, because each samples on its own timer (15 seconds by default). Do not scale up faster than Server pods become ready; a policy such as `behavior.scaleUp` with `stabilizationWindowSeconds: 60` and a `Pods` policy of 5 per 90 seconds reflects that. On some Kubernetes versions the Model HPA shows a per-pod value that overflows; this is only a display artefact.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/scaling/single-model-serving-hpa.md (read in full).
