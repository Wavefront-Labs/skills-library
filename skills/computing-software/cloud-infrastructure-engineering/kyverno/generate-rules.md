---
id: computing-software.cloud-infrastructure-engineering.kyverno.generate-rules
name: generate-rules
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [generate, clone, clonelist, synchronize, generateexisting, orphandownstreamonpolicydelete, updaterequest]
level: practitioner
status: docs-checked
description: "Write legacy Kyverno generate rules: data, clone, cloneList and foreach forms, synchronize semantics, generateExisting, RBAC and UpdateRequest behaviour."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/generate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forms (data and clone are mutually exclusive per rule):
- `data`: full downstream resource in the rule; variables work in all fields.
- `clone`: copy by `namespace` and `name`; content cannot be altered in transit (a mutate rule can).
- `cloneList`: several kinds from one source namespace, optional `selector.matchLabels`.
- `foreach`: JMESPath `list` with `element` and `elementIndex`; children use `data` or `clone`.

`synchronize: true` reverts unauthorized downstream edits, propagates source changes, and removes downstream when the trigger no longer matches (judged on `match` only, not preconditions). Data source with sync: deleting downstream recreates it, deleting the trigger deletes it, deleting the policy deletes it unless `orphanDownstreamOnPolicyDelete: true`. Clone with sync: deleting the policy keeps downstream, deleting the source deletes it, source edits propagate. Without sync nothing is reverted and deleting the policy retains downstream. `spec.useServerSideApply` helps when other controllers must modify the output.

`generateExisting` (default false) applies the rule to existing triggers on policy create and update; the spec-level field is deprecated, use `rules[*].generate[*].generateExisting`.

RBAC: the background controller ServiceAccount needs permission on any non-default kind it generates (checked at install). For RoleBinding or ClusterRoleBinding output it must already hold the same role, or Kubernetes blocks it as privilege escalation.

Caveats: clone sources carry Kyverno tracking labels that other controllers must not strip; with `foreach` and sync, target spec changes are not applied to existing targets; UpdateRequest statuses are Completed, Failed, Pending, Skip, and failed ones retry up to three times; cleanup TTL flags `enableUpdateRequestCleanup` and `updateRequestCleanupTTL` need a cleanup controller.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
