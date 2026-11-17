---
id: computing-software.devops-ci-cd.kustomize.patch-name-and-kind-changes
name: patch-name-and-kind-changes
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [patches, options, allownamechange, allowkindchange]
level: advanced
status: docs-checked
description: "Patches leave a resource name and kind untouched by default; set allowNameChange or allowKindChange in options to rename or retype it."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patches/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Normally a patch cannot change the identity of the resource it edits. The `options` block on a patch overrides that:

```yaml
resources:
- deployment.yaml
patches:
- path: patch.yaml
  target:
    kind: Deployment
  options:
    allowNameChange: true
    allowKindChange: true
```

Both options default to `false`, in which case the patch leaves the kind and name of the resource untouched.

When to use:

- A patch that sets `metadata.name` to give an overlay copy of a resource a different name, without a `namePrefix` that would rename everything.
- A patch that changes `kind` (the docs state the option exists; they do not list supported kind pairs, so test the result).

Related behavior: a patch can refer to a resource by any of its previous names or kinds. If a resource went through name-prefix transformations, you may use its current name, original name or any intermediate name in the patch metadata or `target`.

Keep these options on the single patch that needs them rather than enabling them everywhere, since an accidental rename would otherwise pass silently and break references from other objects.

## Checked

2026-11-08: confirmed against the kustomize patches reference page, read in full (options allowNameChange and allowKindChange, default false, name references). Removed the claim that renaming with allowNameChange creates intermediate names, which the page does not state. The advice paragraph is judgement, not a documented claim.

Method: documentation only; no commands were run.
