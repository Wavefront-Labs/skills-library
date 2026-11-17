---
id: computing-software.devops-ci-cd.spinnaker.kubernetes-artifacts-and-versioning
name: kubernetes-artifacts-and-versioning
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [kubernetes, artifacts, versioned-resources, configmap, manifests, binding, immutable-deployments]
level: advanced
status: docs-checked
description: "Explain how the Kubernetes provider consumes manifests as artifacts, emits deployed objects as kubernetes artifacts, and versions resources like ConfigMaps with a -vNNN suffix."
sources:
  - https://spinnaker.io/docs/reference/artifacts/in-kubernetes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Artifacts matter throughout the Kubernetes provider: the manifests you deploy, and the Docker images and ConfigMaps they reference, can all be expressed as artifacts.

**Manifests as artifacts.** A manifest reaches a deploy stage either as static text in the pipeline or as an artifact, for example a file stored in a GCS bucket. If the pipeline trigger watches that file it runs only when the file changes.

**Kubernetes objects as artifacts.** After a manifest deploys, the resulting objects are injected back into the pipeline context as outputs of the deploy stage. Two different artifacts are involved:
1. an input such as `{"type": "github/file", "name": "manifests/frontend-configs.yml", ...}`, which the deploy stage consumes;
2. an output such as `{"type": "kubernetes/configMap", "name": "frontend-configs", "location": "prod", "version": "v001"}`, which it produces.

To see exactly what a stage produced, open the execution's source JSON.

**Versioned objects.** According to the provider reference, certain resources are versioned: each time a changed manifest is deployed through Spinnaker, the object is redeployed under a new `-vNNN` suffix. The page calls this critical to immutable deployments: rolling out new ConfigMaps, secrets or other versioned resources should require the manifests that reference them to be updated as well.

**Binding.** Spinnaker replaces a manifest field's value with an incoming artifact's reference when the field's referenced type and value match the artifact's type and name. For example `spec.template.spec.containers.*.image` matches `docker/image`, and `spec.template.spec.volumes.*.configMap.name` matches `kubernetes/configMap`; a ConfigMap named `configmap` with version `v001` becomes `configmap-v001`.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Artifacts In Kubernetes page. Confirmed the two manifest delivery modes, both example artifact shapes, the source JSON tip, the -vNNN versioning and the binding heuristic. Removed the rollback remark, which that page does not state.
