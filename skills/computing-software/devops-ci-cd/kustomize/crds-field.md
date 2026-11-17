---
id: computing-software.devops-ci-cd.kustomize.crds-field
name: crds-field
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [crds, custom-resource, namereference, transformer-config]
level: advanced
status: docs-checked
description: "Make kustomize aware of CRD structure so prefixes, suffixes and hashed names are propagated into custom resources."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/crds/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `crds` field lists relative paths to custom resource definition files so kustomize can apply proper transformations to objects of those types.

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
crds:
- crds/typeA.yaml
- crds/typeB.yaml
```

Typical use case from the reference: a CRD object refers to a ConfigMap. In a kustomization the ConfigMap name may change through `namePrefix`, `nameSuffix` or hashing, so the name reference inside the CRD object must be updated the same way.

OpenAPI annotations that can be placed in the definitions:

- `x-kubernetes-annotation`
- `x-kubernetes-label-selector`
- `x-kubernetes-identity`
- `x-kubernetes-object-ref-api-version` (for example `v1`)
- `x-kubernetes-object-ref-kind` (for example `Secret`)
- `x-kubernetes-object-ref-name-key` (for example `name`)

Workflow: add the CRD YAML paths, rebuild, and check that name references inside the custom resource follow the new generated names. For patch merge behavior on custom types, see the `openapi` field.

## Checked

2026-11-03. Confirmed against: the crds reference page.
Removed or reworded: the glossary attribution and the secretName example.

Method: documentation only; no commands were run.
