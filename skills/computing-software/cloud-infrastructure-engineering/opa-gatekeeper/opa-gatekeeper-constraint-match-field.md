---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-constraint-match-field
name: opa-gatekeeper-constraint-match-field
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, constraint, match, kinds, namespaces, label-selector, scope, glob]
level: practitioner
status: docs-checked
description: "Scope a Gatekeeper Constraint with the match field: kinds, scope, namespaces, excludedNamespaces, labelSelector, namespaceSelector and name globs."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/howto.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper constraint match field

A Constraint is an instance of a template kind. Its `spec.match` decides which objects are in scope:
- `kinds`: list of `apiGroups` and `kinds`; one entry matching is enough.
- `scope`: `*` (default), `Cluster` or `Namespaced`.
- `namespaces`: only resources in the listed namespaces; prefix globs work (`kube-*` matches `kube-system` and `kube-public`).
- `excludedNamespaces`: resources not in the listed namespaces; same glob support.
- `labelSelector`: `matchLabels` and `matchExpressions`, all ANDed.
- `namespaceSelector`: label selector against the object's namespace, or the object itself if it is a Namespace.
- `name`: object name, with prefix glob (`pod-*`).

Every top-level matcher you specify must be satisfied. An undefined or empty `match` is inclusive and matches everything. Gotcha: `namespaces`, `excludedNamespaces` and `namespaceSelector` also match cluster-scoped resources, which have no namespace; set `scope: Namespaced` to avoid that.

Example: `match: {kinds: [{apiGroups: [""], kinds: ["Namespace"]}]}`. List all constraints with `kubectl get constraints`.

## Checked

2026-11-08. Confirmed against howto.md, read in full (The match field: each matcher, globs, scope default, inclusive empty match, cluster-scoped gotcha; Listing constraints). Removed or corrected: nothing.

Method: documentation only; no commands were run.
