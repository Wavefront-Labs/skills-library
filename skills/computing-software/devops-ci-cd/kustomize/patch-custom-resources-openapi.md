---
id: computing-software.devops-ci-cd.kustomize.patch-custom-resources-openapi
name: patch-custom-resources-openapi
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [patches, crd, openapi, merge-key, custom-resource]
level: advanced
status: docs-checked
description: "Strategic merge patches on custom resources need OpenAPI merge-key information; supply a schema through the openapi field, while JSON6902 works unchanged."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/openapi/
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patches/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Kustomize uses Kubernetes OpenAPI data to get merge key and patch strategy information about resource types. It has a built-in schema, but that schema only covers built-in Kubernetes types. For custom resources you provide your own OpenAPI schema. Strategic merge patches may need this for a custom resource that uses a merge key other than `name` or needs a list merged rather than replaced. JSON6902 patch usage is the same for built-in and custom resources.

Provide your own schema:

```yaml
resources:
- my_resource.yaml
openapi:
  path: my_schema.json
patches:
  - patch: |-
      apiVersion: example.com/v1alpha1
      kind: MyResource
      metadata:
        name: service
      spec:
        template:
          spec:
            containers:
            - name: server
              image: nginx
```

The openapi page's own example uses the deprecated `patchesStrategicMerge` field for the patch; the `patches` form above is the field the patches page documents.

Kustomize reads the extensions `x-kubernetes-patch-merge-key` and `x-kubernetes-patch-strategy` to perform a strategic merge. Set `x-kubernetes-patch-strategy` to `merge`; you can set the merge key to whatever you like. The page's example custom resource inherits merge keys by pointing `spec.template` at `io.k8s.api.core.v1.PodTemplateSpec` with `$ref`.

Instead of a file, `openapi: version: v1.20.4` tells kustomize to use a built-in Kubernetes schema of that version. `kustomize openapi info` shows which built-in schemas are available, and `kustomize openapi fetch` gets an OpenAPI document from your cluster.

## Checked

2026-11-08: read the openapi reference page in full and the patches page; confirmed the schema limits, `openapi.path` and `openapi.version` forms, the two extensions, the example, both `kustomize openapi` subcommands and the JSON6902 statement. Noted the page example uses a deprecated field.

Method: documentation only; no commands were run.
