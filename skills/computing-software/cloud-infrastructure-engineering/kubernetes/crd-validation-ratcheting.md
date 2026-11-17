---
id: computing-software.cloud-infrastructure-engineering.kubernetes.crd-validation-ratcheting
name: crd-validation-ratcheting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, crds, validation-ratcheting, openapi-schema, cel, crd-versioning]
level: practitioner
status: docs-checked
description: "Rely on CRD validation ratcheting to tighten schemas without breaking updates to existing invalid objects, and know which rules ratchet and which do not."
sources: ["https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#validation-ratcheting", "https://github.com/kubernetes/enhancements/tree/master/keps/sig-api-machinery/4008-crd-ratcheting", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRD validation ratcheting

Tightening a CRD schema (a new `maxLength`, an enum, a CEL rule) used to make every update to an
older object fail if any field violated the new rule, even fields the update did not touch.
With ratcheting (beta and on by default from 1.30, GA in 1.33), the apiserver allows an update
when the invalid parts are unchanged from the stored object.

## Example
Stored object has `spec.name: "this-name-is-far-too-long-for-the-new-limit"`. You add
`maxLength: 20`.
- Update that changes only `spec.replicas`: accepted (invalid field unchanged).
- Update that changes `spec.name` to another too-long value: rejected.
- New objects: fully validated.

## What ratchets
- Most OpenAPI v3 schema validations (for example `maxLength`).
- CEL `x-kubernetes-validations` rules that do not reference `oldSelf`.

## What does not
- The quantifiers `allOf`, `oneOf`, `anyOf` and `not`, and any validations in their descendants: violations still error.
- Transition rules (those using `oldSelf`) are never ratcheted; `optionalOldSelf` lets you write custom ratcheting logic in CEL.

## Still do
- Migrate stored objects to valid values (a controller or a one-off script), because any edit to
  the bad field will be rejected later.
- Version the change: stricter validation is better introduced in a new API version with
  conversion, when the change is large.

## Verify
```bash
kubectl patch <kind> <name> --type=merge -p '{"spec":{"replicas":3}}'      # succeeds
kubectl patch <kind> <name> --type=merge -p '{"spec":{"name":"still-way-too-long-value"}}'   # rejected
```

## Checked
Checked 2026-10-24 against the CRD task page (website main, v1.37) and the `CRDValidationRatcheting` feature gate (alpha 1.28-1.29, beta 1.30-1.32 on by default, stable 1.33): behaviour when invalid parts of an object are unchanged, the exceptions (allOf, oneOf, anyOf, not and descendants; `x-kubernetes-validations` ratcheted only if they do not use `oldSelf`; transition rules never ratcheted), `optionalOldSelf`. Removed the unconfirmed claims about type or structure changes and webhooks.
Method: documentation only; no commands were run.
