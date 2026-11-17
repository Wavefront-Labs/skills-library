---
id: computing-software.cloud-infrastructure-engineering.kubernetes.crd-selectablefields-field-selectors
name: crd-selectablefields-field-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, crds, selectablefields, field-selectors, kubectl, custom-resources]
level: practitioner
status: docs-checked
description: "Declare selectableFields on a CRD so clients can filter custom resources with field selectors on the server, and use them from kubectl and controllers."
sources: ["https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#crd-selectable-fields", "https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apiextensions-apiserver/pkg/apis/apiextensions/validation/validation.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# selectableFields on custom resources

Custom resources support only `metadata.name` and `metadata.namespace` field selectors unless the
CRD declares more (beta and on by default in 1.31, stable in 1.32).

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata: {name: databases.data.example.com}
spec:
  group: data.example.com
  names: {kind: Database, plural: databases}
  scope: Namespaced
  versions:
  - name: v1
    served: true
    storage: true
    selectableFields:
    - jsonPath: .spec.engine
    - jsonPath: .spec.tier
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              engine: {type: string, enum: [postgres, mysql]}
              tier: {type: string}
```

## Use
```bash
kubectl get databases -A --field-selector spec.engine=postgres
kubectl get databases --field-selector spec.engine=postgres,spec.tier!=dev
```
Selectable fields allow filtering of custom resource list, watch and deletecollection requests.

## Rules
- Up to 8 fields per version; each must be a string, integer or boolean scalar.
- `selectableFields` is declared per version, under `spec.versions[*]`.

## Verify
```bash
kubectl get crd databases.data.example.com -o jsonpath='{.spec.versions[0].selectableFields}'
```
and the field selector query returns only matching objects instead of an error about unsupported
field labels.

## Checked
Checked 2026-10-24 against the CRD task page (website main, v1.37), the feature-gate list (`CustomResourceFieldSelectors`: alpha 1.30, beta 1.31, stable 1.32) and the apiextensions validation source (maximum 8 selectable fields per version, field types string, boolean or integer, only `metadata.name` and `metadata.namespace` by default). Removed the client-go informer, conversion and indexing remarks.
Method: documentation only; no commands were run.
