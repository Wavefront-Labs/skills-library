---
id: computing-software.cloud-infrastructure-engineering.kyverno.match-and-exclude
name: match-and-exclude
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [match, exclude, any-all, kinds, namespaceselector, subresources, wildcard-policies]
level: practitioner
status: docs-checked
description: "Select resources in legacy Kyverno rules with match and exclude: any vs all, kinds formats, selectors, subresources and the wildcard and background restrictions."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/match-exclude/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`match` and `exclude` share a structure holding either `any` (OR) or `all` (AND), never both. Under them: `resources`, `subjects`, `roles`, `clusterRoles`. Filters placed directly under `match` are deprecated. Every rule needs a `match`. No variables in `match` or `exclude`. A resource must satisfy `match` and not be caught by `exclude`.

`resources`: `kinds` is mandatory (formats `Group/Version/Kind`, `Version/Kind`, `Kind`). Peer fields are ANDed, list values ORed. `names` and `namespaces` accept wildcards. `operations` defaults to `CREATE` and `UPDATE`. Also `annotations`, `selector` (`matchLabels`/`matchExpressions`, `*` and `?` allowed) and `namespaceSelector`.

Kind wildcards: `Group/*/Kind`, `Group/*/*`, `*/Kind`, `*`. Subresources use `/` or `.` (`Pods/status`, `v1/Pod.eviction`, `*/Node/status`); name the parent explicitly for shared ones like `Scale`.

Restrictions:
- Wildcard policies, subresource policies and policies with `subjects` are not allowed in background mode; `roles`/`clusterRoles` need `background: false`.
- Wildcard policies cannot use `generate`, `verifyImages` or `forEach`; wildcard validate may only `deny` or check `metadata`; wildcard mutate may only touch `metadata`.
- Matching `*` sends every resource type to Kyverno; use sparingly.

Webhook operations derive from the policies' operations; defaults are validating CONNECT, CREATE, UPDATE, DELETE and mutating CREATE, UPDATE.

Some `exclude` examples on the page write `kind:`; the field is `kinds`.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
