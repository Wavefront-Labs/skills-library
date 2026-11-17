---
id: computing-software.devops-ci-cd.kustomize.kustomization-file-structure
name: kustomization-file-structure
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [kustomization, krm, resources, generators, transformers, validators]
level: intro
status: docs-checked
description: "Anatomy of kustomization.yaml: the header and the four ordered lists resources, generators, transformers and validators, and how convenience fields map onto them."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A kustomization.yaml is a Kubernetes Resource Model (KRM) object of kind Kustomization. The docs describe it as basically four lists:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- {pathOrUrl}
generators:
- {pathOrUrl}
transformers:
- {pathOrUrl}
validators:
- {pathOrUrl}
```

Order inside each list is relevant and respected. Every `{pathOrUrl}` entry is either a file system path to YAML holding one or more KRM objects, or a directory (local or in a remote git repo) containing its own kustomization.yaml.

When the entry is a directory, kustomize builds it recursively (hydrates it) into a flat list of objects that is injected into the encapsulating list in order. The encapsulating kustomization is then called an overlay and the thing it refers to is a base.

Under `resources` the result becomes input objects for the current build stage. Under `generators`, `transformers` and `validators` the result is configuration objects that tell kustomize which executable (for example a plugin) to run and with what settings.

Some of these fields allow inline YAML, so a KRM object can be declared directly in kustomization.yaml; in practice this is mainly useful in `transformers`.

Build stage order: resources first, then generators, then transformers, finally validators.

Fields such as `namePrefix`, `configMapGenerator` or `patches` are conveniences: shorthand for running a particular generator or transformer with a particular configuration. The `resources` field is itself a convenience.

## Checked

2026-11-08: read the Kustomization File reference page in full; confirmed the four lists, ordering, pathOrUrl semantics, overlay and base terms, inline YAML note, stage order and conveniences. Nothing removed beyond tightening wording.

Method: documentation only; no commands were run.
