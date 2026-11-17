---
id: computing-software.cloud-infrastructure-engineering.kyverno.mutating-policy
name: mutating-policy
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [mutatingpolicy, applyconfiguration, jsonpatch, mutateexisting, targetmatchconstraints, reinvocationpolicy]
level: advanced
status: docs-checked
description: "Write Kyverno MutatingPolicy: ApplyConfiguration vs JSONPatch, reinvocationPolicy, mutateExisting targets, autogen and ordering caveats."
sources:
  - https://kyverno.io/docs/policy-types/mutating-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`MutatingPolicy` is cluster-scoped; `NamespacedMutatingPolicy` has the same fields within one namespace. It extends Kubernetes MutatingAdmissionPolicy.

Spec:
- `matchConstraints.resourceRules`, `variables` (CEL; `request.object` is usable in mutations only after being passed as a variable).
- `mutations[]` run in order, each with a `patchType`: `ApplyConfiguration` (`applyConfiguration.expression` returning `Object{...}`) or `JSONPatch` (`jsonPatch.expression` returning `JSONPatch{op, path, value}` list, RFC 6902; use `jsonpatch.escapeKey` for keys with `/`).
- `reinvocationPolicy`: `Never` (documented default) or `IfNeeded`.
- `webhookConfiguration.timeoutSeconds`: default 10, range 1 to 30.
- `autogen`: `podControllers.controllers` or `mutatingAdmissionPolicy.enabled: true`; mutually exclusive, with the reason reported in status. Native MAP does not support variables in `matchConditions`.

`evaluation`: `admission.enabled` (CREATE/UPDATE) and `mutateExisting.enabled` (background).

Existing resources: `targetMatchConstraints` takes `resourceRules`, `namespaceSelector` or an `expression` returning a Kubernetes object (via `resource.get(...)`, Kyverno 1.17+); `targetMatchConditions` skip non-matching targets silently. Subresources work, for example `pods/resize` (needs `update` on it and Kubernetes 1.33+).

Caveats: existing-resource mutation is asynchronous with variable delay; the background controller often needs extra RBAC (checked at install); order across policies is not guaranteed, so put dependent mutations in one policy.

## Checked

2026-11-08. Claims were read against: https://kyverno.io/docs/policy-types/mutating-policy/.

Method: documentation only; no commands were run.
