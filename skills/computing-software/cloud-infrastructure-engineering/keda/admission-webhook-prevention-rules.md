---
id: computing-software.cloud-infrastructure-engineering.keda.admission-webhook-prevention-rules
name: admission-webhook-prevention-rules
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [admission-webhooks, validation, scaledobject-validation, triggerauthentication, misconfiguration, hpa-conflict]
level: practitioner
status: docs-checked
description: "Know which ScaledObject and TriggerAuthentication changes the KEDA admission webhooks reject, so errors on kubectl apply are understood."
sources:
  - https://keda.sh/docs/2.17/concepts/admission-webhooks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
KEDA ships admission webhooks that validate new or updated KEDA resources and reject those that break rules which model validation cannot catch. The headline reason: a single workload should never be scaled by two or more HPAs.

Rejected ScaledObject changes:
- The target in `spec.scaleTargetRef` is already autoscaled by another ScaledObject or an HPA.
- A CPU and/or memory trigger is used but the workload has no resource requests defined. This applies only to Deployments and StatefulSets.
- CPU and/or memory are the only triggers and `minReplicaCount: 0` is set (again only for Deployments and StatefulSets).
- Several triggers have a specified `name` and two share the same name.
- `fallback` is configured with a metric type other than AverageValue; fallback supports only AverageValue and not CPU or memory.

Rejected TriggerAuthentication / ClusterTriggerAuthentication changes:
- An empty identity ID for Azure AD Workload Identity or pod identity. This applies only when the resource overrides the default `identityId` supplied to KEDA at installation; an unset ID is passed through.

When `kubectl apply` fails with a webhook denial, match the message to one of these rules. The ownership check can be bypassed with `validations.keda.sh/hpa-ownership` or satisfied with the transfer annotation (see transfer-existing-hpa-ownership).

## Checked

2026-11-03. Confirmed on the 2.17 Concepts Admission Webhooks page: all five ScaledObject rules and the empty identity ID rule.

Method: documentation only; no commands were run.
