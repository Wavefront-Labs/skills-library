---
id: computing-software.cloud-infrastructure-engineering.zot.per-user-namespaces
name: per-user-namespaces
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, username-template, per-user-repos, multi-tenant, glob-matching]
level: practitioner
status: docs-checked
description: "Give each Zot user a private repository namespace with the ${username} template in accessControl, and the matching and precedence rules to know."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```json
"accessControl": { "repositories": { "${username}/**": { "defaultPolicy": ["read", "create", "update"] } } }
```

`${username}` is expanded to the authenticated username before glob matching. Rules:

- Matching is case-sensitive.
- Anonymous identities, uppercase names, and names containing slashes or glob syntax do not match.
- Deletion is not granted unless `delete` is added to the actions.
- A static rule wins over a template that resolves to the same pattern.
- Catalog filtering uses the same patterns, so users see only the repositories they may read.

Pair with an `adminPolicy` for operators, and remember `read` is required alongside any write action.

Typical use: shared team registry where `alice` can push to `alice/app` but not to `bob/app`.

## Checked

2026-11-04. Read against the zot authn-authz article (per-user repository namespaces); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
