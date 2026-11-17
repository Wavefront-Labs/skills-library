---
id: computing-software.devops-ci-cd.kustomize.configmap-generator-behavior
name: configmap-generator-behavior
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [configmapgenerator, behavior, merge, replace, overlay]
level: advanced
status: docs-checked
description: "Use behavior create, replace or merge to override base ConfigMap values in an overlay, and match name and namespace exactly."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/configmapgenerator/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Each generator has `behavior: [create|replace|merge]`:

- `create` (default): make a new ConfigMap; a name conflict with an existing one in the same namespace is an error.
- `replace`: replace an existing ConfigMap from the base.
- `merge`: add or update values of an existing base ConfigMap.

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: my-new-namespace
resources:
- ../base
configMapGenerator:
- name: existing-name
  namespace: existing-ns   # must match target ConfigMap from base
  behavior: replace
  literals:
  - ENV=dev
```

Namespace trap: for `merge` or `replace`, both name and namespace must match the target. If the base leaves namespace unspecified, do not specify it in the overlay; if the base specifies it, the overlay must too. This holds even when the overlay kustomization sets `namespace`, because `configMapGenerator` runs before the namespace transformer.

Suffix trap: an overlay generator that overrides an existing ConfigMap does not cause suffixing of that existing ConfigMap's name. To get name suffixing that follows content changes, define the `configMapGenerator` in the base; the overlay generator then updates the suffix from the new content.

Per-entry options labels and annotations are not overwritten by global `generatorOptions`, but a global `disableNameSuffixHash: true` trumps any local override.

## Checked

2026-11-03. Confirmed against: the configMapGenerator reference page and the built-ins page.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
