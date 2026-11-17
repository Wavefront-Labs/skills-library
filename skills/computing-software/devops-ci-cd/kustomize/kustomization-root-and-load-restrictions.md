---
id: computing-software.devops-ci-cd.kustomize.kustomization-root-and-load-restrictions
name: kustomization-root-and-load-restrictions
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [root, load-restrictions, security, paths]
level: advanced
status: docs-checked
description: "A kustomization root restricts file access to its own directory tree; learn the rule and the flag that relaxes it."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/glossary/
  - https://kubectl.docs.kubernetes.io/references/kustomize/cmd/localize/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The glossary defines a kustomization root as the directory that immediately contains a kustomization.yaml. Data files such as resource YAML, text files of `name=value` pairs for a ConfigMap or Secret, and patch files must live within or below the root, so they are specified by relative paths exclusively. The glossary calls this a security feature.

A flag relaxes it, for example to let a patch file be shared by more than one kustomization. The glossary spells it `--load_restrictions none` (introduced in v2.1). The `kustomize localize` page spells the current build flag `kustomize build --load-restrictor LoadRestrictionsNone`; prefer that form and confirm it with your kustomize version's help output.

Other kustomizations (other directories containing a kustomization.yaml) may be referred to by URL, by absolute path, or by relative path, so referencing a shared directory as a base avoids the flag.

Dependency rules from the glossary:

- If A depends on B, B may not contain A.
- B may not depend on A, even transitively.
- A may contain B, but it might be simplest for A to depend directly on B's resources and drop B's kustomization.yaml (absorb B into A).

Conventionally B is in a directory that is a sibling to A, or off in a completely independent git repository.

The glossary lists four field categories: resources (for example `resources`, `crds`), generators (for example `configMapGenerator`, `secretGenerator`, `generators`), transformers (for example `namePrefix`, `nameSuffix`, `images`, `labels`, `patchesJson6902`, `transformers`) and meta (for example `vars`, `namespace`, `apiVersion`, `kind`).

The `kustomize localize` page notes that localize fails on a kustomization that needs `--load-restrictor LoadRestrictionsNone` to run, because it copies files following security best practices.

## Checked

2026-11-08: read the glossary in full and the kustomize localize reference page. Confirmed the root definition, relative-path rule, dependency rules and field categories. Added the current flag spelling from the localize page, since the glossary's `--load_restrictions none` is the v2.1 form. Removed the troubleshooting paragraph about `../shared/patch.yaml` errors, which neither page states.

Method: documentation only; no commands were run.
