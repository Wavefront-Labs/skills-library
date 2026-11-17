---
id: computing-software.devops-ci-cd.kustomize.vars-deprecated-migration
name: vars-deprecated-migration
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [vars, replacements, migration, edit-fix]
level: advanced
status: docs-checked
description: "vars is deprecated since v5.0.0; convert placeholders and objref entries to replacements by hand, or try the experimental kustomize edit fix --vars."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/vars/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`vars` captured text from one resource field and substituted `$(NAME)` elsewhere:

```yaml
vars:
- name: SOME_SECRET_NAME
  objref:
    kind: Secret
    name: my-secret
    apiVersion: v1
```

The `fieldref.fieldpath` is optional and defaults to `metadata.name`. Only string fields work, and `$(FOO)` references only work in fields listed in kustomize configuration; by default, container command args and env value fields.

`vars` was deprecated in v5.0.0 (kept in v1beta1, absent from v1). Migrate to `replacements`.

Manual steps from the page:

1. Replace every `$(SOME_SECRET_NAME)` with an arbitrary placeholder value (for example `SOME_PLACEHOLDER_VALUE`).
2. Convert the var's `objref` into a replacement `source`.
3. Replace the var's `name` with a `targets` entry whose `fieldPaths` points to each placeholder.

```yaml
replacements:
- source:
    kind: Secret
    name: my-secret
    version: v1
  targets:
  - select:
      kind: Pod
      name: my-pod
    fieldPaths:
    - spec.containers.[name=hello].env.[name=SECRET_TOKEN].value
```

Automatic attempt: `kustomize edit fix --vars` is experimental and may overwrite many resource files; the result may not build to the same output. Run it only in a clean git repository where the change is easy to undo, then diff `kustomize build` before and after.

Also: do not use vars for names that kustomize already updates itself (a Deployment's ConfigMap reference).

## Checked

2026-11-03. Confirmed against: the vars reference page.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
