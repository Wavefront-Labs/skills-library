---
id: computing-software.cloud-infrastructure-engineering.kyverno.validate-rules
name: validate-rules
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [validate, pattern, anypattern, deny, foreach, anchors, podsecurity, wildcards]
level: practitioner
status: docs-checked
description: "Write legacy Kyverno validate rules: pattern, anyPattern, deny, foreach, podSecurity, cel and manifests forms, with operators, wildcards, anchors."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/validate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forms:
- `pattern`: declared fields must match; undeclared fields are wildcards. `anyPattern`: OR across patterns; cannot be combined with `pattern`.
- `deny`: `any`/`all` conditions with `key`, `operator`, `value`, optional `message`; true blocks.
- `foreach`: `list` is a JMESPath expression without braces; each iteration exposes `element`; children `pattern`, `anyPattern`, `deny`, `context`, `preconditions`, `elementScope` (default true); nested loops use `{{elementIndex}}`.
- `podSecurity`: `level` (baseline, restricted), `version`, `exclude[]` with `controlName`, `images[]`, `restrictedField`, `values[]`. `restricted` includes `baseline`; container-level exclusions need `images[]`.
- `cel`: `expressions[]` with `expression` and `message`/`messageExpression`, optional `variables`, `paramKind`, `paramRef`.
- `manifests`: `attestors`, `ignoreFields`, `dryRun` to verify Sigstore-signed manifests. `assert` subrules arrive in 1.13+.

Operators: `>`, `<`, `>=`, `<=`, `!`, `|` (or), `&` (and), `-` (range), `!-`. No equals operator: a plain value means equality.

Wildcards: `*` zero or more alphanumerics (matches empty, not missing); `?` exactly one; `?*` present and non-empty; `null`/`""` means undefined or empty.

Anchors: `()` conditional, `=()` equality if present, `^()` at least one list element matches, `X()` must not exist, `<()` global (false skips the whole rule).

Caveats:
- Use rule-level `failureAction` and `failureActionOverrides` (the latter ClusterPolicy-only); the policy-level fields are deprecated.
- With `failureAction: Audit`, set `spec.emitWarning` to `true` to show violations as admission response warnings.
- Pods blocked by Pod Security Admission in enforce mode send no AdmissionReview to Kyverno, so Kyverno cannot apply policies to them.
- Generated ValidatingAdmissionPolicies come only from `validate.cel` subrules and are reverted if edited by hand.

## Checked

2026-11-08. Read the Kyverno validate rules page (cluster-policy/validate) for patterns, wildcards, operators, anchors, anyPattern, deny, foreach, manifests, podSecurity, cel and the generate-VAP section; the foreach, manifests and podSecurity exclusion examples were read only in part. Removed the `allowExistingViolations` claim (not on the page), narrowed the VAP claim (the page does not restrict it to ClusterPolicies) and reworded the `emitWarning` and Pod Security Admission caveats to the page text. The `assert` subrule (Kyverno 1.13) and `cel` (1.11) version gates were confirmed.

Method: documentation only; no commands were run.
