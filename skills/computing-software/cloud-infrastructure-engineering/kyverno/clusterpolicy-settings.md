---
id: computing-software.cloud-infrastructure-engineering.kyverno.clusterpolicy-settings
name: clusterpolicy-settings
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [policy-settings, validationfailureaction, applyrules, failurepolicy, skipbackgroundrequests, useserversideapply]
level: practitioner
status: docs-checked
description: "Set legacy ClusterPolicy spec options: Audit vs Enforce, applyRules, background, failurePolicy, webhook timeout, and which options are deprecated since 1.13."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/policy-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ClusterPolicy is deprecated (see the policy types overview), but its settings remain in many clusters.

- `admission`: default `true`; `false` means background mode only.
- `background`: default `true`; scans existing resources and produces Policy Reports.
- `applyRules`: `One` or `All` (default `All`); `One` stops after the first rule that applies.
- `skipBackgroundRequests`: default `true`; must be `false` for generate and mutateExisting rules to apply to background-controller requests.
- `useServerSideApply`: generate rules only; default `false`; when true Kyverno owns its fields via server-side apply so other controllers can see them.
- `schemaValidation`: default `true`, deprecated since 1.11, no effect.

Deprecated as of 1.13, with replacements:
- `validationFailureAction` (`Audit` default, `Enforce` blocks) becomes `failureAction` under the validate rule.
- `validationFailureActionOverrides` becomes `failureActionOverrides` in the rule.
- `failurePolicy` (`Fail` default or `Ignore`) becomes `webhookConfiguration.failurePolicy`. `Ignore` also lets failing registry calls be skipped, which helps verifyImages during registry outages.
- `webhookTimeoutSeconds` (default 10, range 1 to 30) becomes `webhookConfiguration.timeoutSeconds`.
- Spec-level `generateExisting` moves under the generate rule; `mutateExistingOnPolicyUpdate` moves under the mutate rule.

`kubectl explain policy.spec` gives schema help. The page lists no annotations.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
