---
id: computing-software.devops-ci-cd.argo-rollouts.ephemeral-metadata-labels
name: ephemeral-metadata-labels
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [ephemeral-metadata, stablemetadata, canarymetadata, activemetadata, previewmetadata, downward-api, argo-rollouts]
level: advanced
status: docs-checked
description: "Label or annotate stable, canary, active and preview pods only while they play that role."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/ephemeral-metadata/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Ephemeral metadata is optional. It adds user-defined labels and annotations to pods only for the time they are the desired or stable set; the labels are updated or removed as soon as the ReplicaSet switches roles (for example desired to stable).

Two motivations: build Prometheus, Wavefront or Datadog queries and dashboards on stable labels instead of `rollouts-pod-template-hash`, which changes every revision; and let applications know a deployment is happening by reading labels through the Kubernetes Downward API (for example point the app at a different queue server while its pods are in preview, and at the production queue when marked stable).

Canary strategy:

```yaml
strategy:
  canary:
    stableMetadata:
      labels:
        role: stable
    canaryMetadata:
      labels:
        role: canary
```

Blue-green strategy uses `activeMetadata` and `previewMetadata` the same way. During an update the controller merges `canaryMetadata`/`previewMetadata` into the new ReplicaSet's `spec.template.metadata`; when the rollout is fully promoted that ReplicaSet becomes stable and its pods are updated in place (not recreated) to the `stableMetadata`/`activeMetadata` values. Labels and annotations are both supported.

Tools and apps only benefit if they notice labels that change after a pod has started; application code reading them through the Downward API also needs a library that reloads changed files.

Verify: `kubectl get pods --show-labels` shows the example `role=canary` label on new pods during an update and `role=stable` after promotion.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/features/ephemeral-metadata/, https://argo-rollouts.readthedocs.io/en/stable/features/specification/.

Removed or corrected: the claim that blue-green metadata is merged into active or preview pods (corrected: only the desired ReplicaSet template is merged, stable/active is applied in place).

Method: documentation only; no commands were run.
