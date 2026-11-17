---
id: computing-software.cloud-infrastructure-engineering.kyverno.preconditions
name: preconditions
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [preconditions, operators, anyin, allin, duration-operators, skip-result]
level: practitioner
status: docs-checked
description: "Use Kyverno preconditions to refine which matched resources a rule applies to: any/all blocks, the operator set, skip results and set-operator semantics."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/preconditions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Preconditions are defined per rule and evaluated after a resource is matched and not excluded. They contain `any` and/or `all` blocks of expressions with `key`, `operator`, `value` and optional `message`. Keys and values may use variables, JMESPath and context data, and can be lists.

Operators:
- `Equals`, `NotEquals`
- `AnyIn`, `AllIn`, `AnyNotIn`, `AllNotIn` (string, integer, boolean)
- `GreaterThan`, `GreaterThanOrEquals`, `LessThan`, `LessThanOrEquals` (also Kubernetes quantities such as `1Gi`)
- `DurationGreaterThan`, `DurationGreaterThanOrEquals`, `DurationLessThan`, `DurationLessThanOrEquals` (seconds, or Go durations with `s`, `m`, `h`)

Behaviour: `all` needs every statement true, `any` needs one. If any block is not true the rule does not apply, with short-circuiting. In rules that report, a resource discarded by preconditions is scored `skip`, unlike `exclude`, which ignores it at once. A custom `message` goes to the Kyverno log for the failing expression and does not block.

Tips and caveats:
- Use `|| ''` to check non-existence of optional fields.
- `Equals` and `NotEquals` compare one key to one value; use the set operators for arrays.
- Comparison operators work on single values, not arrays.
- String values support wildcards such as `*.mycompany.com`.
- Predefined variables like `{{serviceAccountName}}` are available.
- In mutate rules, preconditions can filter entries inside `foreach`.
- Preconditions cannot be given in `match` or `exclude` (use those blocks for structural selection).

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
