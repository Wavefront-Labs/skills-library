---
id: computing-software.cloud-infrastructure-engineering.keda.transfer-existing-hpa-ownership
name: transfer-existing-hpa-ownership
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [transfer-hpa-ownership, hpa-ownership, validations-keda-sh, existing-hpa, migration]
level: advanced
status: docs-checked
description: "Hand an existing Kubernetes HPA to a ScaledObject using the transfer-hpa-ownership annotation, and what the hpa-ownership validation switch does."
sources:
  - https://keda.sh/docs/2.17/concepts/scaling-deployments/
  - https://keda.sh/docs/2.17/reference/scaledobject-spec/
  - https://keda.sh/docs/2.17/concepts/admission-webhooks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the admission webhook rejects a ScaledObject whose target is already autoscaled by another ScaledObject or an HPA, because two autoscalers on one workload cause conflicts. To migrate a workload that already has an HPA, make the ScaledObject take it over:

```yaml
metadata:
  annotations:
    scaledobject.keda.sh/transfer-hpa-ownership: "true"
spec:
   advanced:
      horizontalPodAutoscalerConfig:
        name: {name-of-hpa-resource}
```

The page stresses that you must specify a custom HPA name that matches the existing HPA you want KEDA to manage.

A separate annotation, `validations.keda.sh/hpa-ownership: "true"` (as in the ScaledObject specification and scaling-deployments pages; the operate admission-webhooks page says to set it to `"false"`), disables the HPA-ownership validation on a ScaledObject. It buys flexibility but the documentation says it also brings vulnerabilities and must be used at your own risk.

Both annotations appear as optional metadata in the ScaledObject specification, next to the paused annotation, and neither is required for normal operation.

## Checked

2026-11-03. Confirmed on the 2.17 Scaling Deployments and ScaledObject specification pages: transfer annotation, custom HPA name note, hpa-ownership annotation and risk warning. Removed: two consequences the pages do not state. Noted the true/false disagreement between pages.

Method: documentation only; no commands were run.
