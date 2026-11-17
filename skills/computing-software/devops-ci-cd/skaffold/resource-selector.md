---
id: computing-software.devops-ci-cd.skaffold.resource-selector
name: resource-selector
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [resourceselector, allow, deny, labels, podspec]
level: advanced
status: docs-checked
description: "Control which Kubernetes resource kinds and fields Skaffold manages when it rewrites images and adds labels."
sources:
  - "https://skaffold.dev/docs/tutorials/skaffold-resource-selector/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Skaffold changes the manifests it renders and deploys in two ways: it adds a run-id label (used by status checking to find the resources it manages) and it substitutes `image:` values with the images it just built. The top-level `resourceSelector` extends or restricts which resource kinds and fields are touched.

```yaml
resourceSelector:
  allow:
  - groupKind: "CustomDeployment.skaffold.dev"
    image: [".*"]
    labels: [".*"]
  deny:
  - groupKind: "StatefulSet.apps"
    labels: [".spec.volumeClaimTemplates.*.metadata.labels"]
```

Each entry (an `allow` or `deny` list item) has a required `groupKind` and optional `image`, `labels` and `podSpec`, each a list of JSON-path-like paths. Image paths say where to rewrite images; label paths say where to add a labels block if it is missing; `podSpec` paths say where pod spec properties can be overwritten. The docs say only label-related and image modifications are supported currently.

The special value `.*` means: for `image`, replace every `*.image` field whose value is an image Skaffold builds; for `labels`, append to or create `*.metadata.labels` wherever `*.metadata` exists.

Default managed kinds include Pod, DaemonSet.apps, Deployment.apps, ReplicaSet.apps, StatefulSet.apps (except `.spec.volumeClaimTemplates.*.metadata.labels`), CronJob.batch, Job.batch, the older `extensions` variants, Service.serving.knative.dev, the Agones Fleet and GameServer, the Argo Rollout, Workflow, CronWorkflow, WorkflowTemplate and ClusterWorkflowTemplate kinds, and `*.cnrm.cloud.google.com`.

Uses documented:

- Manage a custom resource so Skaffold rewrites its images and labels and waits properly: add an `allow` entry with `image` and `labels` set to `[".*"]`. Without it Skaffold applies the YAML but does not replace the images.
- Avoid overwriting an immutable field that causes Kubernetes errors on redeploy: add a `deny` entry for that kind and path, as in the StatefulSet example above (which is already part of the defaults).
- A custom resource that names its image field differently (for example `foo:`): add an `allow` entry whose `image` path points at that field.

Check the result with `skaffold render` and inspect the image values and labels.

## Checked

2026-11-09: confirmed against the Skaffold docs page "Manage CRDs w/ Skaffold - Configuring Which K8s Resources & Fields Skaffold Manages" (source docs-v2/content/en/docs/tutorials/skaffold-resource-selector.md) and its three sample files. Replaced the cited source, which returns 404, with this page. Removed the `skaffold.dev/run-id` label name (the page spells it differently), the Secret deny example and unverified rollout advice.

Method: docs-checked 2026-11-09 against skaffold.dev resource-selector tutorial page (read in full as source markdown).
