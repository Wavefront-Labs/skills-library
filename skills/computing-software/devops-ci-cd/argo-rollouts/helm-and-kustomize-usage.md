---
id: computing-software.devops-ci-cd.argo-rollouts.helm-and-kustomize-usage
name: helm-and-kustomize-usage
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [helm, kustomize, rollout-transform, configurations, gitops, templating, argo-rollouts]
level: practitioner
status: docs-checked
description: "Manage Rollout manifests with Helm and teach Kustomize about Rollouts using a transformer config."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/features/helm/
  - https://argo-rollouts.readthedocs.io/en/stable/features/kustomize/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Helm.** Argo Rollouts responds to Rollout resources regardless of how they were created, so it is compatible with any templating tool. If a Helm chart contains Rollout resources, as soon as you install or upgrade, the controller takes over and starts progressive delivery. Write the Rollout in the chart with the usual template helpers for names, replicas and image tags.

**Kustomize.** Kustomize does not know the structure of a Rollout by default. A transformer configuration teaches it, enabling ConfigMap and Secret generators, variable references, and common labels and annotations.

1. Download `rollout-transform.yaml` into your kustomize directory.
2. List it under `configurations`:

```yaml
kind: Kustomization
apiVersion: kustomize.config.k8s.io/v1beta1
configurations:
  - rollout-transform.yaml
```

Remote references are possible. With Kustomize 3.6.1 reference the raw `rollout-transform.yaml` URL from the Argo Rollouts repository `docs/features/kustomize` directory; with Kustomize 5 use `rollout-transform-kustomize-v5.yaml` instead.

An example kustomize app is in the repository under `docs/features/kustomize/example`.

Alternative: from Kustomize 4.5.5, Kustomize can use OpenAPI data to get merge key and patch strategy information for resource types, so a patch in a kustomization can update a Rollout (for example change a container image) with an `openapi: path:` entry pointing at the Argo schema JSON (`argo_all_k8s_kustomize_schema.json` in the argo-schema-generator repository).

Verify: build the kustomization and confirm the Rollout shows the generated names or patched fields you expect.

## Checked

2026-11-08. Confirmed against the Argo Rollouts Helm and Kustomize pages (both read in full): Helm compatibility, transformer configuration steps, remote references for Kustomize 3.6.1 and 5, example directory, OpenAPI option from Kustomize 4.5.5.

Removed or corrected: removed the ConfigMap hash suffix pitfall paragraph and the kustomize build and lint verify commands (not on the cited pages).

Method: documentation only; no commands were run.
