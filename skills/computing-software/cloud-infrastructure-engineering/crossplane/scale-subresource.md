---
id: computing-software.cloud-infrastructure-engineering.crossplane.scale-subresource
name: scale-subresource
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [scale, hpa, keda, xrd, replicas]
level: advanced
status: docs-checked
description: "Expose the scale subresource on an XRD so kubectl scale, HPA and KEDA can control a composite resource."
sources:
  - https://docs.crossplane.io/latest/guides/scalable-composition/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Configure the `scale` block per version in the XRD's `subresources` field. It has three fields:

- `specReplicasPath`: JSON path in `spec` holding the desired count. It must exist in the XRD schema.
- `statusReplicasPath`: JSON path in `status` holding the observed count; also must exist in the schema.
- `labelSelectorPath`: optional path to a string field in `status` with a serialized label selector. The HPA requires it.

Crossplane propagates the configuration to the generated CRD. It does not implement scaling: the Composition author must forward the count. With function-patch-and-transform, patch `spec.replicas` from the XR into a composed Deployment, and write the current count back to `status.replicas` (and `status.labelSelector` if used) so autoscalers and `kubectl scale --current-replicas` read correct values.

Use function-auto-ready to mark composed resources ready when healthy.

Then:

```shell
kubectl scale myapp/my-app --replicas=3
kubectl get myapp/my-app
```

The listing shows DESIRED and CURRENT columns.

Because the paths must exist in the schema, add `replicas` to `spec.properties` and `status.properties` of the XRD before enabling scale.

## Checked

2026-11-08: read the whole Crossplane Scalable Composition guide (raw source of docs.crossplane.io/latest/guides/scalable-composition). Confirmed the three `scale` fields and their rules, that the block is set per version under `subresources`, that the composition author implements scaling (patch `spec.replicas`, write back `status.replicas` and `status.labelSelector`), function-auto-ready, and the `kubectl scale` and DESIRED/CURRENT output. Reworded the opening to name the `subresources` field.
Method: documentation only; no commands were run.
