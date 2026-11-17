---
id: computing-software.devops-ci-cd.kustomize.components-field
name: components-field
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [components, compose, reusable, kustomization]
level: advanced
status: docs-checked
description: "The components field composes reusable kustomization fragments into a kustomization; the components guide defines them with kind Component and lists them in overlays."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/components/"
  - "https://kubectl.docs.kubernetes.io/guides/config_management/components/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `components` field composes reusable pieces of configuration into an overlay. The reference page is short and points to the components guide, which this skill summarises.

From the components guide:

- As of v3.7.0 kustomize supports a special type of kustomization for reusable pieces of configuration logic that can be included from multiple overlays.
- Components suit applications with optional features that different overlays enable in different subsets (different environments or audiences).
- A component directory has its own kustomization.yaml that uses `apiVersion: kustomize.config.k8s.io/v1alpha1` and `kind: Component`.
- The guide's example components use generators (`secretGenerator`, `configMapGenerator` with `behavior: merge`) and patches.
- An overlay (an ordinary `Kustomization`) lists the base under `resources` and the optional features under `components`.

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

components:
  - ../../components/external_db
  - ../../components/recaptcha
```

Commenting out a component entry (as the guide's dev overlay does with `ldap`) disables that feature in that overlay. Generate each variant with `kustomize build overlays/community` and similar commands.

Practical workflow: put one optional feature in its own directory, reference it from the overlay's `components:` list, and diff `kustomize build` output with and without it.

## Checked

2026-11-03. Confirmed against: the components reference page and the Kustomize components guide.
Removed or reworded: the hedged speculation about component semantics and ordering, replaced with guide content (v3.7.0, v1alpha1 Component kind).

Method: documentation only; no commands were run.
