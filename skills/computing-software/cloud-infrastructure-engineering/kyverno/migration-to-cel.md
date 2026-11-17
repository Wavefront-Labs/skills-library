---
id: computing-software.cloud-infrastructure-engineering.kyverno.migration-to-cel
name: migration-to-cel
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [migration-to-cel, clusterpolicy-deprecation, field-mapping, warnings-as-errors, deprecated-api-metric]
level: advanced
status: docs-checked
description: "Migrate Kyverno ClusterPolicy and CleanupPolicy to CEL policy types: detection, field mapping, unsupported features, deprecation timeline and common CEL errors."
sources:
  - https://kyverno.io/docs/guides/migration-to-cel/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Timeline: ClusterPolicy, Policy, CleanupPolicy and legacy PolicyException are deprecated as of v1.19 and scheduled for removal in v1.20. CEL types reached feature parity in v1.19.

Steps: find legacy use via admission warnings, `kyverno apply`/`kyverno test` warnings and the metric `kyverno_deprecated_api_requests_total`. Split each rule into its own CEL policy (one action each), pick ValidatingPolicy, MutatingPolicy, GeneratingPolicy, ImageValidatingPolicy or DeletingPolicy, rewrite patterns as CEL (invert `deny` logic), convert exceptions to `policies.kyverno.io` with `policyRefs`, and replace `request.object` with `object` and `request.namespace` with `object.metadata.namespace`. Test with `kyverno apply` and `kyverno test`; add `--warnings-as-errors` in CI.

Mapping highlights:
- `admission`/`background` become `spec.evaluation.admission.enabled` / `spec.evaluation.background.enabled`; `emitWarning` becomes `validationActions: Warn`; `webhookConfiguration.failurePolicy` becomes `spec.failurePolicy`; `matchConditions` carry over; `applyRules` has no equivalent.
- `exclude` becomes `matchConstraints.excludeResourceRules`; `context` becomes `spec.variables`; `reportProperties` becomes `auditAnnotations`.
- Validate patterns, `cel`, `foreach` become `spec.validations` (foreach via `all()`, `exists()`, `exists_one()`); `failureAction` becomes `validationActions`.
- `mutateExisting` becomes `evaluation.mutateExisting.enabled`; `patchesJson6902` becomes `patchType: JSONPatch`.
- `generateExisting`, `synchronize`, `orphanDownstreamOnPolicyDelete` move under `spec.evaluation`.
- verifyImages: `imageReferences` to `matchImageReferences`, `attestors`, `attestations`, `imageRegistryCredentials` to `credentials`, `verifyDigest`/`mutateDigest`/`required` to `validationConfigurations`.

Not supported: `validate.manifests`, `validate.podSecurity` (write per-control validations), `allowExistingViolations`, `failureActionOverrides`, `patchStrategicMerge`, rule names (so no `ruleNames`). Use `Enforce`/`Audit` capitalised. Deprecation warnings come only from the admission controller, not the CLI.

CEL errors: unknown field (use `has()` or `?.orValue()`), index out of bounds (check `size()`), comprehension types (wrap `orValue([])`). The page does not explain `kyverno migrate`.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
