---
id: computing-software.cloud-infrastructure-engineering.kubernetes.crd-schema-design-and-validation
name: crd-schema-design-and-validation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, crd, customresourcedefinition, openapi-v3, structural-schema, x-kubernetes-preserve-unknown-fields, pruning, defaulting, cel-validation, x-kubernetes-validations, kubebuilder-markers, controller-gen, apiserver-validation, status-subresource, scale-subresource]
level: advanced
status: docs-checked
description: "Write CRD OpenAPI v3 schemas that are structural, prune unknowns safely, default correctly, and validate with CEL instead of a webhook."
sources: ["https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/", "https://book.kubebuilder.io/reference/generating-crd", "https://github.com/kubernetes-sigs/controller-tools/tree/main/pkg/crd/markers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRD schema design and validation — get the shape right before anyone writes a controller

**Goal:** a CRD whose schema rejects garbage at the API server, needs no webhook for
basic validation, and can gain fields for years without breaking old clients. Most
operator pain (silent data loss, impossible migrations, "why did my field disappear")
traces back to a sloppy schema written in the first afternoon.

## 1. Structural schema or nothing
With `apiextensions.k8s.io/v1` (the Kubernetes docs list 1.16 as the minimum server version for this task),
`spec.versions[].schema.openAPIV3Schema` must be a **structural schema**:
every property reachable from the root has a `type`, nested objects declare
`properties` (or `additionalProperties`), and `description`-only placeholder fields
are not enough. A non-structural schema is rejected at `kubectl apply -f crd.yaml`
with a specific error naming the offending path — read it, it's accurate.
- `x-kubernetes-preserve-unknown-fields: true` opts a subtree out of structural rules
  (needed for arbitrary JSON like Helm values or pod templates you don't want to
  re-model). Use it narrowly — on one field, not the whole spec — or pruning below
  does nothing for that subtree.

## 2. Pruning (default, and a trap)
Unknown fields are **pruned** (silently dropped) on write unless the field's subtree
has `x-kubernetes-preserve-unknown-fields: true`. This is good — it stops typo'd
fields from silently doing nothing — but it means:
- A field you forgot to add to the schema isn't rejected, it's *deleted* on the way
  into etcd. `kubectl apply` returns success with your typo gone. Debug by
  `kubectl get <cr> -o yaml` immediately after apply and diffing against what you sent.
- Embedding a full Pod/Container spec (sidecar injection patterns) needs either
  `x-kubernetes-preserve-unknown-fields: true` at that node or a hand-maintained
  mirror of the PodSpec schema (use `controller-gen`'s `+kubebuilder:pruning:PreserveUnknownFields`
  marker, or vendor `k8s.io/api/core/v1` structs directly so the generator does it).

## 3. Defaulting
`default:` in the schema applies at the API server to fields absent from the request (using
the request version's defaults), when reading from etcd (storage version defaults; these are not
written back until an update persists them) and after mutating admission webhooks that patch the
object. It needs `apiextensions.k8s.io/v1`. Controllers therefore see defaulted values. This is the
correct place for defaults, not "set it in Reconcile if empty": the latter means
`kubectl get -o yaml` shows an empty field until the first reconcile, and GitOps
diffing tools see permanent drift.
```yaml
properties:
  replicas:
    type: integer
    minimum: 1
    default: 1
```
Kubebuilder marker equivalent: `// +kubebuilder:default=1` above the Go field.
Defaults only apply to fields absent from the request, not fields set to zero
values (`0`, `""`, `false`) — those are explicit values, not omissions.

## 4. Validation: CEL beats a webhook
`x-kubernetes-validations` (CEL validation rules; stable since v1.29) runs validation inside
the API server — no network hop, no webhook to keep alive, no `failurePolicy` decision. Rules
are subject to a validation cost budget.
```yaml
x-kubernetes-validations:
- rule: "self.minReplicas <= self.maxReplicas"
  message: "minReplicas must be <= maxReplicas"
- rule: "self.replicas >= oldSelf.replicas || !has(oldSelf.frozen) || !oldSelf.frozen"
  message: "cannot scale down while frozen"
```
`oldSelf` is available for update validation (immutability rules, monotonic fields)
— this alone removes the single most common reason teams reach for a validating
webhook. Kubebuilder marker: `// +kubebuilder:validation:XValidation:rule="...",message="..."`.
Reserve an actual **ValidatingWebhookConfiguration** for cross-resource checks CEL
can't see (uniqueness across objects, lookups against other API types) — see
`computing-software.cloud-infrastructure-engineering.kubernetes.admission-webhook-development`.
Rules over lists or maps without `maxItems`/`maxLength` limits are costed at worst case and can
be rejected by the resource budget; set bounds in the schema and avoid nested lists and maps.

## 5. Immutability, enums, and the fields people forget
- Immutable fields: no native "immutable" keyword before CEL; use
  `self == oldSelf` in `x-kubernetes-validations` on update, or
  `// +kubebuilder:validation:XValidation:rule="self == oldSelf"`.
- `enum:` for closed sets (`Phase: [Pending, Running, Failed]`) — rejects typos the
  Go `string` type alone won't catch from `kubectl edit`.
- Mark optionality with `+required` / `+optional` (controller-tools marks the long forms
  `+kubebuilder:validation:Required` / `Optional` as deprecated). With no marker, controller-tools
  treats a field as required unless the json tag has `omitempty` (or `omitzero`); mismatches
  between tag and marker produce confusing schemas.
- `status` subresource: `subresources: {status: {}}` splits spec/status write paths:
  PUT/POST/PATCH to the custom resource ignore changes to `status`, PUT to `/status`
  ignores everything except `status`, and RBAC can grant controllers write on
  `<resource>/status` only.
- `scale` subresource for HPA-compatible custom resources: declares
  `specReplicasPath`, `statusReplicasPath`, `labelSelectorPath`.
- Additional printer columns (`additionalPrinterColumns`) so `kubectl get myresource`
  shows phase/age/ready instead of just NAME — cheap, and the first thing users ask for.

## Gotchas
- Renaming or removing a field is a breaking change the moment one object in the
  cluster has it set — list live objects (`kubectl get <kind> -A -o yaml`)
  before assuming a field is unused.
- CEL `rule` errors by default report a generic message unless you set `message:`;
  always set it, the generic one is useless to the end user.
- Schema changes to an already-served CRD version need a new API version or careful
  additive-only changes (see `crd-versioning-and-conversion-webhooks`) — you cannot
  silently make a field required that used to be optional.
- `controller-gen crd` regenerates the whole CRD from markers; hand edits to the
  YAML get silently overwritten on the next `make manifests`. Put every rule in markers.

## Verify
- [ ] `kubectl apply -f crd.yaml` succeeds with no structural-schema warning.
- [ ] Apply an object with a deliberate typo'd field; confirm it's pruned (missing on
      `kubectl get -o yaml`), not silently accepted as a real field.
- [ ] Apply an object omitting a defaulted field; confirm the default appears on read.
- [ ] A CEL rule violation returns your custom `message`, not a generic CEL error.
- [ ] `status` is a separate subresource; a plain `kubectl apply` to spec does not
      zero out status set by the controller.

## Checked
Checked 2026-10-24 against the kubernetes/website CustomResourceDefinition task page (structural
schema, pruning, defaulting points, validation rules stable in v1.29, cost budget, status and scale
subresources), the Kubebuilder CRD generation page, and controller-tools `main` (`+kubebuilder:default`,
`+kubebuilder:pruning:PreserveUnknownFields`, `XValidation`, `+required`/`+optional`, omitempty default).
Method: documentation only; no commands were run.
