---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.semantic-configuration-validation
name: semantic-configuration-validation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [semantic-validation, config-validation-tooling, configuration-design, cue, json-schema, kubernetes-validating-admission-policy]
level: advanced
status: docs-checked
description: "Validate config semantics, not just syntax: catch typos and wrong units at commit time, with CUE schemas and Kubernetes ValidatingAdmissionPolicy as example tools."
sources: ["https://sre.google/workbook/configuration-design/", "https://cuelang.org/docs/concept/how-cue-works-with-json-schema/", "https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Semantic validation tooling

SRE Workbook chapter 14: most languages give syntax validation for free, but do not overlook semantic
validation. Syntactically valid configuration may reference a nonexistent directory (a typo) or ask for a
thousand times more RAM than exists (wrong units). Validate that configuration is semantically meaningful
to the maximum extent possible, and for every possible misconfiguration ask whether you could prevent it at
the moment the user commits the configuration, rather than after the change is submitted.

## Layers to consider
- Types and required fields (schema).
- Ranges and units.
- Cross-field consistency (for example a minimum not above a maximum).
- References to things that must exist.
- Policy (organisation rules).
Choose a tool per layer; the Workbook does not prescribe one.

## CUE
CUE can validate data against constraints: its docs show `cue vet` checking data files against a CUE
definition, and against a JSON Schema directly. See the CUE page on how CUE works with JSON Schema.

## Kubernetes ValidatingAdmissionPolicy
Validating admission policies use the Common Expression Language (CEL) to declare validation rules. A
ValidatingAdmissionPolicy and a corresponding ValidatingAdmissionPolicyBinding must both be defined for a
policy to take effect. The Kubernetes page marks the feature stable since v1.30. Because it runs at apply
time, it also catches changes that skipped CI.

## Good error messages
Say what is wrong, where and what was expected, so people do not bypass validation.

## Verify
- [ ] A set of known-bad configurations, each rejected before it can be submitted.

## Checked
2026-11-01. Confirmed against SRE Workbook chapter 14 (semantic validation), the CUE JSON Schema page (`cue vet` against a definition and against JSON Schema) and the Kubernetes ValidatingAdmissionPolicy page (CEL, policy plus binding required, stable since v1.30).
Removed: the layer table of tools, the CUE and CEL example snippets, `kubeconform`/Conftest/Kyverno mentions, `validationActions`, and the effect-analysis row, because no page read states them.
Method: documentation only; no commands were run.
