---
id: computing-software.ai-ml-engineering.kserve.kserve-hpa-autoscaling
name: kserve-hpa-autoscaling
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [hpa, autoscalerclass, scaletarget, scalemetric, minreplicas, maxreplicas, autoscaling-metrics, metrics-server, per-component-autoscaling, servingkserveioautoscalerclass]
level: practitioner
status: docs-checked
description: "Standard-mode autoscaling with Kubernetes HPA: autoscalerClass hpa/none/external, scaleTarget and scaleMetric cpu or memory, per-component autoScaling and defaults."
sources: ["https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/autoscaling/hpa-autoscaler.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HPA autoscaling (Standard mode)

Standard mode uses Deployment, Service, Ingress and a Kubernetes HPA instead of Knative KPA. It needs Metrics Server and does NOT support scale to zero. Concurrency and RPS metrics are Knative-only.

```yaml
metadata:
  annotations:
    serving.kserve.io/deploymentMode: Standard
    serving.kserve.io/autoscalerClass: hpa
spec:
  predictor:
    scaleTarget: 80
    scaleMetric: cpu          # cpu or memory (utilization percentage)
```

## Disable KServe-managed HPA
`serving.kserve.io/autoscalerClass: none` creates and manages no HPA (recommended for full disable). `external` makes KServe delete its HPA but allows an externally managed one.

## Per component
Predictor, transformer and explainer each get their own HPA, but only for components present in the spec. A component without `autoScaling` gets defaults: `minReplicas: 1`, `maxReplicas: 1`, `scaleMetric: cpu`, `scaleTarget: 80`, so it effectively never scales.

```yaml
spec:
  predictor:
    minReplicas: 1
    maxReplicas: 5
    autoScaling:
      metrics:
        - type: Resource
          resource:
            name: cpu
            target: {type: Utilization, averageUtilization: 80}
  transformer:
    minReplicas: 2
    maxReplicas: 10
    autoScaling: {metrics: [{type: Resource, resource: {name: cpu, target: {type: Utilization, averageUtilization: 60}}}]}
```

Verify with `kubectl get hpa` (names like `custom-model-hpa-predictor`).

## Checked
Method: docs-only read of cited pages, 2026-11-08

Read the cited KServe HPA autoscaler page in full; every claim matches it. No content removed.
