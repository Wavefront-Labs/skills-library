---
id: computing-software.cloud-infrastructure-engineering.kubernetes.crd-x-kubernetes-schema-extensions
name: crd-x-kubernetes-schema-extensions
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, crd, x-kubernetes-extensions, preserve-unknown-fields, x-kubernetes-list-type, structural-schema]
level: practitioner
status: docs-checked
description: "Use CRD schema extensions correctly: x-kubernetes-preserve-unknown-fields, int-or-string, embedded-resource, list-type and map-type for server-side apply merges."
sources: ["https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#specifying-a-structural-schema", "https://kubernetes.io/docs/reference/using-api/server-side-apply/#merge-strategy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRD x-kubernetes schema extensions

## x-kubernetes-preserve-unknown-fields
```yaml
config:
  type: object
  x-kubernetes-preserve-unknown-fields: true
```
Opts that subtree out of pruning (free-form config blobs). Use narrowly: preserved unknown fields are not validated.

## x-kubernetes-int-or-string
```yaml
port:
  x-kubernetes-int-or-string: true
  anyOf: [{type: integer}, {type: string}]
```
For values like `8080` or `"http"` (same as core `IntOrString`).

## x-kubernetes-embedded-resource
Marks a field holding a full Kubernetes object: `apiVersion`, `kind` and `metadata` are implicitly specified and validated. The CRD documentation example adds `x-kubernetes-preserve-unknown-fields: true` alongside it (optional).

## List and map types (server-side apply merge semantics)
```yaml
ports:
  type: array
  x-kubernetes-list-type: map
  x-kubernetes-list-map-keys: [name]
  items:
    type: object
    required: [name]
    properties:
      name: {type: string}
      port: {type: integer}
tags:
  type: array
  x-kubernetes-list-type: set           # unique scalars, merged as a set
  items: {type: string}
```
- `atomic`: the whole list is replaced during merge and owned by a single manager. Server-side apply treats all lists of custom resources as atomic unless the schema says otherwise.
- `set`: lists of scalar elements that must be unique; different managers can own entries.
- `map`: items keyed by `list-map-keys`, so different managers can own different entries.
- `x-kubernetes-map-type: granular|atomic` for objects.

## x-kubernetes-validations
CEL rules (see CRD CEL validation), for example
`- rule: "self.minReplicas <= self.maxReplicas"`.

## Verify
```bash
kubectl apply --server-side --dry-run=server -f widget.yaml
```

## Checked
Checked 2026-10-24 against the CRD task page and the Server-Side Apply page (website main, v1.37): `x-kubernetes-preserve-unknown-fields`, `x-kubernetes-int-or-string` with the anyOf pattern, `x-kubernetes-embedded-resource`, `x-kubernetes-list-type` (atomic, set, map), `x-kubernetes-list-map-keys`, `x-kubernetes-map-type` (atomic, granular), custom resources default to atomic lists, `x-kubernetes-validations`. Removed the unconfirmed root-of-spec advice and the jq inspection command.
Method: documentation only; no commands were run.
