---
id: computing-software.cloud-infrastructure-engineering.kyverno.policy-exceptions
name: policy-exceptions
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [policyexception, enablepolicyexception, exceptionnamespace, matchconditions, allowedvalues, reportresult]
level: practitioner
status: docs-checked
description: "Grant Kyverno PolicyExceptions: enabling flags, CEL exception fields (policyRefs, matchConditions, images, reportResult), the legacy form and the wildcard risks."
sources:
  - https://kyverno.io/docs/guides/exceptions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Legacy PolicyExceptions are off by default. Set the flag `enablePolicyException=true` and `exceptionNamespace` to restrict which namespace may hold them. They are namespaced objects but can exempt cluster-scoped resources.

CEL PolicyException (`policies.kyverno.io`):
- `policyRefs`: list of `name` and `kind` (ValidatingPolicy, ImageValidatingPolicy, GeneratingPolicy...).
- `matchConditions`: named CEL expressions; true skips the referenced policy for that resource.
- `images`: glob-style patterns exempting matching images from image checks.
- `allowedValues`: values the policy CEL reads via `exceptions.allowedValues`.
- `reportResult`: `skip` (default) or `pass`.
Works in admission and background; reports show `result: skip` with an `exceptions` property.

Legacy PolicyException (`kyverno.io`, deprecated v1.19, removed v1.20; applies only to ClusterPolicy and Policy):
- `exceptions[]`: `policyName` (`<namespace>/<policy-name>` for namespaced Policies) and `ruleNames`, wildcards allowed.
- `match` and `conditions` as in policies; `background` defaults on and turns Fail into Skip in reports.
- `podSecurity[]`: `controlName`, `images`, `restrictedField`, `values`. Values outside the list are rejected (the example blocks an added `SYS_ADMIN`).
- `namespaceSelector` works fully from 1.15.2.

Limits: legacy background evaluation forbids Roles, ClusterRoles and user info in the match. Wildcards broaden exceptions; prefer exact names. Exceptions are plain CRs, so restrict who can create them with RBAC, namespace limits, GitOps or a Kyverno validate rule.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
