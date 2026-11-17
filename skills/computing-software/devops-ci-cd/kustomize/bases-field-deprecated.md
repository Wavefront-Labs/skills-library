---
id: computing-software.devops-ci-cd.kustomize.bases-field-deprecated
name: bases-field-deprecated
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [bases, deprecated, resources, edit-fix]
level: intro
status: docs-checked
description: "The bases field was deprecated in v2.1.0; move entries to resources and let kustomize edit fix convert them."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/bases/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `bases` field was deprecated in kustomize v2.1.0. The reference page promises it will never be removed from the `kustomize.config.k8s.io/v1beta1` Kustomization API, but it will not be included in the `v1` API when that exists. Before any removal there will be at least two releases between deprecation and removal of v1beta1 support in the CLI.

Migrate by moving each entry into `resources`:

```yaml
# before
bases:
- ../base
# after
resources:
- ../base
```

Or let the tool do it:

```bash
kustomize edit fix
```

Why move: `resources` lets bases be ordered relative to other input resources, while the concept of a base stays central. The same page pattern applies to other deprecated fields, so after upgrading kustomize it is worth running `kustomize edit fix` on every kustomization and reviewing the diff.

The same deprecation wording appears for `commonLabels`, `patchesStrategicMerge`, `patchesJson6902` and `vars` (deprecated in v5.0.0); each page names its replacement (`labels`, `patches`, `replacements`).

Good habit: commit the repository before running the fix, then run `kustomize build` before and after and diff the output to confirm the conversion preserved the result.

## Checked

2026-11-03. Confirmed against: the bases, commonLabels, patchesStrategicMerge and vars reference pages.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
