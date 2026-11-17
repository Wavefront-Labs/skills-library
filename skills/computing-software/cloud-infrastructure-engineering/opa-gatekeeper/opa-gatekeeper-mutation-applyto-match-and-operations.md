---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-mutation-applyto-match-and-operations
name: opa-gatekeeper-mutation-applyto-match-and-operations
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, mutation, applyto, match, operations, create, update]
level: advanced
status: docs-checked
description: "Scope Gatekeeper mutators with applyTo and match, including the operations field that limits mutation to CREATE or UPDATE."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/mutation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper mutation applyto match and operations

`applyTo` lists groups, kinds and versions the mutator edits; it lets Gatekeeper learn each kind schema so it can detect mutators that disagree and could cause non-convergent mutation. It does not accept globs. `match` uses the constraint criteria: `scope`, `kinds`, `labelSelector`, `namespaces`, `namespaceSelector`, `excludedNamespaces`, and `name` (prefix glob). Empty criteria are inclusive.

The `operations` field inside an `applyTo` entry accepts `CREATE`, `UPDATE` or `*`. Only CREATE and UPDATE are handled by the mutation webhook, so DELETE and CONNECT are rejected by validation. Omitting the field, `["*"]` and `["CREATE","UPDATE"]` currently behave the same, but `*` and omission widen automatically if the webhook gains operations; list operations explicitly to pin them.

```yaml
applyTo:
  - groups: [""]
    kinds: ["Pod"]
    versions: ["v1"]
    operations: ["CREATE"]
```

Use CREATE-only for values that hit immutable fields on update. Caveats: a CREATE-only mutator does not touch objects that existed before it was deployed, even when they are later updated, and mutators restricted to some operations do not apply in audit or expansion contexts where no operation is available.

## Checked

2026-11-08: read the whole of website/docs/mutation.md in the Gatekeeper repo (extent of changes, operations field, backward and forward compatibility notes). Confirmed every claim; nothing removed.

Method: documentation only; no commands were run.
