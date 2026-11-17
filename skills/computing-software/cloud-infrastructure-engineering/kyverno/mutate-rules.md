---
id: computing-software.cloud-infrastructure-engineering.kyverno.mutate-rules
name: mutate-rules
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [mutate, patchstrategicmerge, patchesjson6902, mutate-existing, conditional-anchor, foreach]
level: practitioner
status: docs-checked
description: "Write legacy Kyverno mutate rules: patchStrategicMerge, patchesJson6902, foreach, mutate-existing targets, anchors and ordering or loop-protection caveats."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/mutate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forms:
- `patchStrategicMerge`: overlay a partial resource. In `containers[]` the key needs a conditional anchor such as `(name): "*"`.
- `patchesJson6902`: `add`, `replace`, `remove`; append with `/-`; escape `~` and `/` as `~0` and `~1`. No conditional anchors, use preconditions.
- `foreach`: iterates a JMESPath `list`, exposing `element` (and `elementIndex` for JSON patches); nested loops use `elementIndex0`/`elementIndex1`, `as:` names variables. Loops run in declaration order and emit no patches until all finish; use `Descending` order when removing array elements.
- Mutate existing: `mutate.targets[]` with `name`, `namespace`, `selector.matchLabels`; omitted name or namespace acts as a wildcard; targets in a rule share a schema and ignore resource filters.

Anchors (strategic merge): `(field)` conditional, a failing one skips its children and remaining list siblings, nesting unsupported; `+(field)` add if absent (avoid on lists outside `foreach`); `<(field)` global. Conditionals are evaluated first.

Caveats:
- Mutation runs before validation, so rules must not contradict.
- `name`, `namespace`, `uid`, `kind`, `apiVersion` cannot change.
- JSON-patch mutations on Pods are not auto-translated to controllers.
- Mutate-existing is asynchronous, may need background-controller RBAC, reports failures through UpdateRequests, and defaults `mutateExistingOnPolicyUpdate` to off (when true, `targets` is required). Since v1.11.2 it skips deletions unless `DELETE` is listed.
- Background requests are ignored as loop protection; a mutate-existing after a generate needs `skipBackgroundRequests: false`, and you must prevent loops.
- Put dependent rules top to bottom in one policy; put generate before mutate.
- Flux dry-run diffs still invoke mutations.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
