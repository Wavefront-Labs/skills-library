---
id: computing-software.cloud-infrastructure-engineering.keda.restore-original-replicas-and-hpa-config
name: restore-original-replicas-and-hpa-config
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [restoretooriginalreplicacount, horizontalpodautoscalerconfig, hpa-behavior, stabilization-window, hpa-name]
level: advanced
status: docs-checked
description: "Set advanced ScaledObject options: restore replicas on deletion, rename the generated HPA and pass scale-down behaviour such as stabilization windows to it."
sources:
  - https://keda.sh/docs/2.17/reference/scaledobject-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `spec.advanced` section carries two operational controls.

`restoreToOriginalReplicaCount` (default `false`) decides what happens to the target when the ScaledObject is deleted. Page example: a Deployment created with 3 replicas is scaled by KEDA to 10, then the ScaledObject is deleted. With the default the Deployment stays at 10; with `true` it is set back to the original 3.

`horizontalPodAutoscalerConfig` shapes the HPA KEDA creates:
- `name`: defaults to `keda-hpa-{scaled-object-name}`.
- `behavior`: copied into the HPA `behavior` field, which affects scaling between 1 and N replicas, the part the HPA handles internally. Example in the specification:

```yaml
advanced:
  horizontalPodAutoscalerConfig:
    behavior:
      scaleDown:
        stabilizationWindowSeconds: 300
        policies:
        - type: Percent
          value: 100
          periodSeconds: 15
```

Assumption stated on the page: the cluster runs Kubernetes 1.18 or newer, the release that introduced HPA configurable behaviour. Follow the Kubernetes documentation for the policy semantics.

## Checked

2026-11-03. Confirmed on the 2.17 ScaledObject specification: restoreToOriginalReplicaCount default and 3 to 10 example, HPA name default, behavior example, Kubernetes 1.18. Removed: unsupported usage advice.

Method: documentation only; no commands were run.
