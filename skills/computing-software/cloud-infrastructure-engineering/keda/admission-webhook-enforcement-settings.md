---
id: computing-software.cloud-infrastructure-engineering.keda.admission-webhook-enforcement-settings
name: admission-webhook-enforcement-settings
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [failurepolicy, validation-enforcement, cache-miss-to-direct-client, extraargs, webhook-race-condition]
level: sme
status: docs-checked
description: "Make KEDA validation mandatory by switching webhooks from failurePolicy Ignore to Fail, and fix the ScaledObject cache-miss race with --cache-miss-to-direct-client."
sources:
  - https://keda.sh/docs/2.17/operate/admission-webhooks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default behaviour: KEDA registers its admission webhooks with `failurePolicy: Ignore`. If the admission controller is unavailable, creation and updates of resources are not blocked, so validation can silently be skipped. To guarantee validation, set `failurePolicy` to `Fail`.

This page says the HPA ownership validation can be skipped per object by setting the annotation `validations.keda.sh/hpa-ownership` to `"false"`, while the ScaledObject specification and the scaling-deployments page show the same annotation set to `"true"` to disable the validation. The docs disagree, so confirm the value against your KEDA version. The docs warn that skipping it exposes the system to risks.

Race condition: with enforcement on, applying a ScaledObject together with its `scaleTargetRef` in the same deployment artifact can fail because the webhook's cached client has not seen the target yet (kedacore/keda issue 5973 is referenced). Add this argument to the webhook Deployment:

```
--cache-miss-to-direct-client=true
```

If the cached read returns `IsNotFound`, the webhook then reads the object directly from the Kubernetes API. It defaults to `false` to avoid extra API traffic on cache misses. With the Helm chart:

```yaml
extraArgs:
  webhooks:
    cache-miss-to-direct-client: "true"
```

## Checked

2026-11-03. Confirmed on the 2.17 Operate Admission Webhooks page: failurePolicy Ignore default, cache-miss-to-direct-client (default false, Helm extraArgs.webhooks). Removed: an unsupported claim about the cost of failurePolicy Fail. Added: the docs disagree on the value of the hpa-ownership annotation (this page says false, the spec and scaling-deployments pages say true).

Method: documentation only; no commands were run.
