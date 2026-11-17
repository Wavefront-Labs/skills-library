---
id: computing-software.cloud-infrastructure-engineering.kubernetes.crd-naming-api-groups-and-kubectl-explain
name: crd-naming-api-groups-and-kubectl-explain
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, crds, api-group-design, crd-naming, kubectl-explain, openapi, short-names, categories, printer-columns]
level: practitioner
status: docs-checked
description: "Name CRDs and API groups well (domain-based groups, plural/kind/shortNames, categories, printer columns) and make them self-documenting through kubectl explain and OpenAPI."
sources: ["https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/", "https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_explain/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/explain", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apiextensions-apiserver/pkg/apihelpers/helpers.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRD naming, API groups and kubectl explain

## Group and names
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.platform.example.com        # must be <plural>.<group>
spec:
  group: platform.example.com                 # a DNS domain you control; k8s.io, kubernetes.io and their subdomains are protected
  scope: Namespaced
  names:
    kind: Database                            # CamelCase singular
    listKind: DatabaseList
    plural: databases                         # lowercase, used in URLs and RBAC
    singular: database
    shortNames: [db]                          # check `kubectl api-resources` for collisions
    categories: [platform, all]               # `kubectl get platform` lists all platform kinds
```
Conventions (API conventions doc): resource collections are lowercase and plural, kinds are CamelCase and singular, group names are lowercase valid DNS names; think twice about `bool` fields, because many start as booleans and later need more values (`spec.tier: standard|premium` beats `spec.premium: true`); use `metav1.Condition` for status conditions. A CRD in a group that is `k8s.io`, `kubernetes.io` or a subdomain of either must carry an `api-approved.kubernetes.io` annotation.

Renaming a group or kind later means a new CRD plus migration.

## Printer columns
```yaml
  versions:
  - name: v1
    additionalPrinterColumns:
    - {name: Engine, type: string, jsonPath: .spec.engine}
    - {name: Ready, type: string, jsonPath: '.status.conditions[?(@.type=="Ready")].status'}
    - {name: Age, type: date, jsonPath: .metadata.creationTimestamp}
```

## Self-documenting with kubectl explain
`kubectl explain` reads the CRD's OpenAPI v3 schema — field `description`s are your docs.
```bash
kubectl explain databases
kubectl explain databases.spec.backup --recursive
kubectl explain database.spec --api-version=platform.example.com/v1beta1
kubectl explain pods.spec.containers.resources --output=plaintext-openapiv2   # output formats: plaintext, plaintext-openapiv2
```
Empty explain output usually means the schema has no descriptions or that `x-kubernetes-preserve-unknown-fields: true` hides the structure.

## Verify
- [ ] `kubectl api-resources --api-group=platform.example.com` lists kinds with short names; no collisions.
- [ ] `kubectl explain <kind>.spec` shows a description for every field.

## Checked
Checked 2026-10-24 against the CRD task page (website main, v1.37), the apiextensions validation source, the kubectl explain source (main) and the API conventions document: CRD name `<plural>.<group>`, names fields, shortNames, categories (`kubectl get <category>`), additionalPrinterColumns with jsonPath, protected groups (`k8s.io`, `kubernetes.io` and subdomains) and the `api-approved.kubernetes.io` annotation, `--recursive`, `--api-version`, `--output` formats, lowercase plural resources and CamelCase singular kinds, the `bool` field advice, `metav1.Condition`. Removed the one-group-per-team advice and the kubebuilder marker remarks.
Method: documentation only; no commands were run.
