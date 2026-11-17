---
id: computing-software.devops-ci-cd.kustomize.kustomize-version
name: kustomize-version
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [kustomize, version, cli, troubleshooting]
level: intro
status: docs-checked
description: "Print the installed kustomize version in text, yaml or json form to confirm which release a field or deprecation applies to."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/cmd/version/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/sortoptions/
  - https://kubectl.docs.kubernetes.io/references/kustomize/builtins/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/replacements/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/commonlabels/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patchesstrategicmerge/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patchesjson6902/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/vars/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/bases/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`kustomize version` prints the version.

```bash
kustomize version
# v5.0.0
kustomize version -o yaml
# version: kustomize/v5.0.0
# gitCommit: <commit hash>
# buildDate: <timestamp>
# goOs: darwin
# goArch: arm64
# goVersion: go1.19.5
kustomize version -o json
```

Flags: `-o, --output string` (one of `yaml` or `json`) and `-h, --help`. A global flag `--stack-trace` prints a stack trace on error. `kustomize version --short` is deprecated and will be removed.

Why check the version: many documented behaviors are version gated.

- `sortOptions`: v5.0.0+.
- NamespaceTransformer `unsetOnly` and `setRoleBindingSubjects`: v4.5.6+.
- Regular-expression matching in replacement `[name=...]` paths: after v4.5.3.
- Deprecations of `commonLabels`, `patchesStrategicMerge`, `patchesJson6902` and `vars`: v5.0.0.
- `bases` deprecated: v2.1.0.

If a field from the docs is rejected, compare `kustomize version` with the version gates above first.

## Checked

2026-11-08: confirmed against the kustomize version reference page (read in full) and the version statements on the sortOptions, builtins (NamespaceTransformer), replacements, commonLabels, patchesStrategicMerge, patchesJson6902, vars and bases pages. Partial reads: sortOptions and builtins were read in full; the replacements, commonLabels, patchesStrategicMerge, patchesJson6902, vars and bases pages were checked only for the sentence that states the version. Removed the claims about kubectl embedding its own kustomize and about `kustomize edit fix`, which none of these pages state.

Method: documentation only; no commands were run.
