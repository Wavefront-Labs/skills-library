---
id: computing-software.devops-ci-cd.kustomize.build-stage-ordering
name: build-stage-ordering
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [order, resources, generators, transformers, validators, build]
level: practitioner
status: docs-checked
description: "Understand the fixed processing order of a kustomize build stage so generated resources are transformed and validators see the final list."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/configmapgenerator/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Per the Kustomization File page, a build stage runs in this order:

1. `resources` are processed first.
2. `generators` are processed, adding to the resource list under consideration.
3. `transformers` modify the list.
4. `validators` run last and check the list for errors.

Notes from the same page:

- A validator is just a transformer that does not transform, but can fail the build with an error message. Kustomize attempts to disallow validators from making changes.
- A generator cannot be a transformer, because it accepts no input other than its own configuration. A transformer does not implement the generator interface, but it can behave like one, since the resource map it works on lets it append, replace and remove resources.
- The order within each of the four lists is relevant and respected.
- Convenience fields such as `configMapGenerator`, `namePrefix` and `patches` are shorthand for running a generator or transformer, and are placed in the same stages.

A related trap documented on the configMapGenerator page: `configMapGenerator` runs before the namespace transformer. When an overlay uses `behavior: merge` or `replace` on a base ConfigMap, the generator's name and namespace must match the target ConfigMap in the base (if the base has no namespace, do not specify one in the overlay), even when the overlay Kustomization sets a `namespace`.

## Checked

2026-11-08: read the Kustomization File reference page and the configMapGenerator page in full. Confirmed stage order, validator behaviour, the generator and transformer relationship and the namespace trap. Corrected the draft, which said a transformer cannot be a generator; the page says a generator cannot be a transformer. Removed the debugging tip, which neither page states.

Method: documentation only; no commands were run.
