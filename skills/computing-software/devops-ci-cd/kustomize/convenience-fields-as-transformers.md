---
id: computing-software.devops-ci-cd.kustomize.convenience-fields-as-transformers
name: convenience-fields-as-transformers
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [transformers, plugins, builtin, prefixsuffixtransformer]
level: advanced
status: docs-checked
description: "Every kustomization field is shorthand for a built-in transformer or generator; learn the equivalence so you can use the transformers field when you need full argument control."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The docs state that every field in a kustomization could be expressed as a transformer, so any kustomization file can be converted into one with a single `transformers:` field.

These two stanzas do exactly the same thing:

```yaml
namePrefix: bob-
```

```yaml
transformers:
- |-
  apiVersion: builtin
  kind: PrefixSuffixTransformer
  metadata:
    name: myFancyNamePrefixer
  prefix: bob-
  fieldSpecs:
  - path: metadata/name
```

Why keep the dedicated fields? They are useful for ordering and signalling (these particular things are transformers and should run after the generators but before the validators), and they make common use cases easier to express.

Build stage order, per the page: resources are processed first, then generators (adding to the resource list), then transformers (modifying the list), and finally validators check the list. A validator is a transformer that does not transform but can fail the build; kustomize attempts to disallow validators from making changes.

The `transformers` field accepts inline YAML (the `|-` block above); the page notes that inlining is mainly useful in the transformers field.

## Checked

2026-11-08: read the Kustomization File reference page in full; confirmed the everything-is-a-transformer statement, the PrefixSuffixTransformer example, the ordering rationale, stage order, validator behaviour and inline YAML note. Removed the list mapping individual fields to built-in kinds and the fieldSpecs advice, because the built-ins page was not read in full for this check.

Method: documentation only; no commands were run.
