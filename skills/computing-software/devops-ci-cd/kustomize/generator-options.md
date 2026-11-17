---
id: computing-software.devops-ci-cd.kustomize.generator-options
name: generator-options
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [generatoroptions, labels, annotations, immutable, disablenamesuffixhash]
level: practitioner
status: docs-checked
description: "Set labels, annotations, name-hash behavior and the immutable flag for all generated ConfigMaps and Secrets."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/generatoroptions/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`generatorOptions` controls behavior of every ConfigMap and Secret generator in the kustomization:

```yaml
generatorOptions:
  # labels added to all generated resources
  labels:
    kustomize.generated.resources: somevalue
  # annotations added to all generated resources
  annotations:
    kustomize.generated.resource: somevalue
  # disables the default hash suffix on generated names
  disableNameSuffixHash: true
  # adds the immutable property to generated resources
  immutable: true
```

Example output for a ConfigMap built from `application.properties`: it carries the label and annotation from `generatorOptions`, and a suffixed name such as `my-application-properties-f7mm6mhf59`. With `disableNameSuffixHash: true` the Secret in Example II keeps the plain name `app-tls`.

The same options can be set per entry in `options`, using the same subfields. Precedence: labels and annotations set per entry are not overwritten by the global ones, but a global `disableNameSuffixHash: true` overrides any local attempt to turn the hash back on.

The `immutable` field adds the immutable property to generated resources.

## Checked

2026-11-03. Confirmed against: the generatorOptions and configMapGenerator reference pages.
Removed or reworded: advice about combining immutable with the hash suffix.

Method: documentation only; no commands were run.
