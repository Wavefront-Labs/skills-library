---
id: computing-software.cloud-infrastructure-engineering.kyverno.generating-policy
name: generating-policy
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [generatingpolicy, generator-apply, synchronize, generateexisting, orphandownstream, template]
level: advanced
status: docs-checked
description: "Write Kyverno GeneratingPolicy: expression vs template generation, generator.Apply, clone sources, synchronize and generateExisting."
sources:
  - https://kyverno.io/docs/policy-types/generating-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`GeneratingPolicy` is cluster-scoped; `NamespacedGeneratingPolicy` defaults documents to its own namespace and rejects others. Stable as of v1.19.

Spec: `matchConstraints.resourceRules` (trigger), optional `matchConditions`, `variables`, `evaluation` (`synchronize`, `generateExisting`, `orphanDownstreamOnPolicyDelete`), and `generate[]` entries each with exactly one of `expression` or `template`.
- `template.value`: YAML string, documents separated by `---` (beta in v1.19). `template.interpolate`: `none` (default) or `cel`, which evaluates `(( ... ))`; escape a literal `((` as `\((`. Placeholders are not allowed in mapping keys.
- Target namespace comes from each document's `metadata.namespace`; none means cluster-scoped.
- `generator.Apply(namespace, [resources])` returns `true`, so it composes with `list.all(...)`; loop with `variables.nsList.all(ns, generator.Apply(ns, ...))`.
- Clone: `resource.Get("v1", "secrets", "default", "regcred")` or `resource.List(...)`.

Sync (`evaluation.synchronize.enabled: true`): generated data is recreated if deleted, reverted if modified, deleted with its trigger, and updated with the policy. Cloned copies follow the source (source deletion deletes copies; deleting the policy keeps them).

`orphanDownstreamOnPolicyDelete.enabled: true` keeps generated resources when the policy goes; default false deletes them when sync is on.

Existing resources: default triggers are CREATE, UPDATE, DELETE events only; `evaluation.generateExisting.enabled: true` does a one-time scan on policy creation.

Fan-out to a runtime-computed namespace set cannot be done with templates; use `generator.Apply()` in a CEL loop. Exemptions use `PolicyException`.

## Checked

2026-11-08. Claims were read against: https://kyverno.io/docs/policy-types/generating-policy/.

Method: documentation only; no commands were run.
