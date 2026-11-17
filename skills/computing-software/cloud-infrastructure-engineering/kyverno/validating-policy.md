---
id: computing-software.cloud-infrastructure-engineering.kyverno.validating-policy
name: validating-policy
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [validatingpolicy, cel, validationactions, matchconstraints, messageexpression, autogen, json-mode]
level: practitioner
status: docs-checked
description: "Write Kyverno ValidatingPolicy: matchConstraints, validations, variables, evaluation modes, webhook timeout, autogen and messageExpression."
sources:
  - https://kyverno.io/docs/policy-types/validating-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`apiVersion: policies.kyverno.io/v1`, `kind: ValidatingPolicy` (stable since v1.19). It extends Kubernetes ValidatingAdmissionPolicy.

Fields:
- `spec.validationActions`: e.g. `Deny` or `Audit`.
- `spec.matchConstraints.resourceRules`: `apiGroups`, `apiVersions`, `operations`, `resources`.
- `spec.validations[]`: `expression` (CEL), `message`, optional `messageExpression`. `messageExpression` must yield a string and wins over `message`; it falls back to `message` if it fails or returns an empty, whitespace-only or multi-line string.
- `spec.variables[]` (`name`, `expression`, used as `variables.<name>`); `spec.matchConditions[]`; `spec.auditAnnotations[]` (`key`, static value or `valueExpression`), stored in PolicyReports.
- `spec.evaluation`: `admission.enabled`, `background.enabled`, and `mode` (`Kubernetes` in examples, `JSON` for other payloads; no explicit default stated).
- `spec.webhookConfiguration.timeoutSeconds`: default 10, range 1 to 30; mirrored into the generated ValidatingWebhookConfiguration.
- `spec.autogen`: `podControllers.controllers` (deployments, jobs, cronjobs, statefulsets) or `validatingAdmissionPolicy.enabled: true`. They are mutually exclusive; if `podControllers` is set, VAP generation is skipped and the reason appears in status.

Scope: `ValidatingPolicy` is cluster-wide; `NamespacedValidatingPolicy` has the same fields within one namespace. Exempt resources with `PolicyException`.

JSON payloads (for example a Terraform plan): set `evaluation.mode: JSON`, add `matchConditions` and `validations`, and evaluate with the CLI; a Kyverno Engine SDK is planned.

## Checked

2026-11-08. Claims were read against: https://kyverno.io/docs/policy-types/validating-policy/.

Method: documentation only; no commands were run.
