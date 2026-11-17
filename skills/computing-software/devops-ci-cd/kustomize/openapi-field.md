---
id: computing-software.devops-ci-cd.kustomize.openapi-field
name: openapi-field
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [openapi, schema, kustomize-openapi, merge-key]
level: advanced
status: docs-checked
description: "Tell kustomize where to get OpenAPI merge-key and patch-strategy data: a custom schema file path or a built-in Kubernetes version."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/openapi/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`openapi` controls the schema used for strategic merge. Two forms:

```yaml
openapi:
  path: my_schema.json
```

```yaml
openapi:
  version: v1.20.4
```

The first points to your own schema file (needed for custom resources); the second explicitly selects a built-in Kubernetes OpenAPI schema version. See which are available with:

```bash
kustomize openapi info
```

and obtain an OpenAPI document from a cluster with:

```bash
kustomize openapi fetch
```

Kustomize's built-in schema only has information on built-in Kubernetes types. For custom resource types, supply merge-key and patch-strategy information. The extensions it reads are `x-kubernetes-patch-merge-key` and `x-kubernetes-patch-strategy`; set the strategy to `merge` and the merge key to whatever identifies list elements. List-map hints such as `x-kubernetes-list-map-keys` and `x-kubernetes-list-type` appear in the docs example for the `ports` field, whose merge key is `containerPort`.

A custom type can inherit merge keys by referencing `io.k8s.api.core.v1.PodTemplateSpec` with `$ref`, as `MyResource.spec.template` does in the example.

Symptom of a missing schema: a patch replaces a whole list instead of merging the element. Add the schema, rebuild and confirm.

## Checked

2026-11-03. Confirmed against: the openapi reference page.
Removed or reworded: nothing needed removing; all claims matched the pages.

Method: documentation only; no commands were run.
