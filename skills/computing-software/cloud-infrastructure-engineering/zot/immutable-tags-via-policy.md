---
id: computing-software.cloud-infrastructure-engineering.zot.immutable-tags-via-policy
name: immutable-tags-via-policy
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, immutable-tags, default-policy, update-action, write-once]
level: practitioner
status: docs-checked
description: "Make Zot image tags immutable with no dedicated flag, by allowing only read and create in accessControl and granting update to chosen users."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/immutable-tags.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Zot has no explicit immutable-tag flag; the effect comes from authorization policies. Granting `create` without `update` lets an image be pushed once; further updates are rejected.

Immutable for everyone: allow `read` and `create` only.

```json
"repositories": { "**": { "defaultPolicy": ["read", "create"] } }
```

Images can be pushed once and pulled; later updates are rejected.

Immutable with overrides: keep that default and add a user policy granting `update` to selected users.

```json
"repositories": { "**": {
  "policies": [ { "users": ["alice", "bob"], "actions": ["read", "create", "update"] } ],
  "defaultPolicy": ["read", "create"]
} }
```

Pushes happen once and pulls work; updates are rejected except for the listed users.

Notes: `read` must always be present. Longest-match rules mean a more specific repository pattern can loosen or tighten this for a subtree.

## Checked

2026-11-04. Read against the zot immutable tags and authn-authz articles. Removed: the claim that a deleted tag could be recreated if delete is granted, and the first-push-is-create wording, neither stated on the pages.

Method: documentation only; no commands were run.
