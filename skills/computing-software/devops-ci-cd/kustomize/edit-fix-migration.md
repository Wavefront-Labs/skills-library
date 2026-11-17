---
id: computing-software.devops-ci-cd.kustomize.edit-fix-migration
name: edit-fix-migration
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [edit, fix, migration, deprecations]
level: practitioner
status: docs-checked
description: "Automatically convert deprecated kustomization fields to their replacements and verify the converted output matches."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patchesstrategicmerge/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patchesjson6902/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/bases/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/commonlabels/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/vars/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`kustomize edit fix` converts deprecated kustomization fields automatically. The reference pages name these conversions:

| Deprecated | Replacement | Deprecated in |
|---|---|---|
| `bases` | `resources` | v2.1.0 |
| `commonLabels` | `labels` | v5.0.0 |
| `patchesStrategicMerge` | `patches` | v5.0.0 |
| `patchesJson6902` | `patches` | v5.0.0 |
| `vars` | `replacements` | v5.0.0 (experimental `kustomize edit fix --vars`) |

Each of these stays in the `kustomize.config.k8s.io/v1beta1` API permanently but will not be included in `v1`. When v1 is available the v1beta1 deprecation will be announced, with at least two releases between deprecation and removal of v1beta1 support from the CLI.

For `vars`, the page warns that the automatic conversion will potentially overwrite many resource files and that the resulting files may not produce the same output from `kustomize build`. It recommends running it in a clean git repository where the change is easy to undo.

For `commonLabels`, the `labels` field adds labels without automatically injecting corresponding selectors, so compare selectors after converting; `commonLabels` always adds them.

Verification approach: build before and after, then compare the output.

```bash
kustomize build overlay > before.yaml
kustomize edit fix
kustomize build overlay > after.yaml
diff before.yaml after.yaml
```

## Checked

2026-11-08: read the patchesStrategicMerge, patchesJson6902, bases, commonLabels and vars reference pages in full. Confirmed the deprecation versions, replacements, `edit fix` conversions, the v1beta1 and v1 statement and the vars warning. Removed the claims that no diff is expected for bases and patch fields, that `edit fix` yields `includeSelectors: true`, and that it must be run in every directory.

Method: documentation only; no commands were run.
