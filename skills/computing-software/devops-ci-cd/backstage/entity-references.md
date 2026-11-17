---
id: computing-software.devops-ci-cd.backstage.entity-references
name: entity-references
category: computing-software
field: devops-ci-cd
product: backstage
tags: [entity-ref, string-references, kind-namespace-name, backstage]
level: intro
status: docs-checked
description: "Write references between entities as kind:namespace/name strings or compound objects and know the defaults."
sources:
  - https://backstage.io/docs/features/software-catalog/references
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Every entity is identified by the triplet of kind, namespace and name. When one entity points at another, for example an `owner` or `memberOf`, you write a reference.

String form: `[<kind>:][<namespace>/]<name>`. The name is always required, and the kind and namespace may be omitted when the context supplies defaults.

```yaml
spec:
  owner: group:default/artist-relations-team
  dependsOn:
    - resource:default/artists-db
    - component:payments
  providesApis:
    - artist-api
```

The compound form is an object with `kind`, `namespace` and `name` fields.

Guidance:

- The default namespace is `default`.
- Which kind applies when it is omitted depends on the field (for example `spec.owner` defaults to Group, with User also allowed), so the kind-specific field documentation says which defaults apply.
- When refs are passed between systems as identifiers they should be complete (all three parts) and lowercased, for example with `stringifyEntityRef`; receivers should treat refs case-insensitively.
- The compound form is mainly for Backstage code; prefer the string form between plugins and external systems.

## Checked

2026-11-03. Confirmed on the References page: the kind, namespace and name triplet, the string and compound forms, complete lowercase refs between systems with case-insensitive receivers, and the preference for the string form outside Backstage code. On the descriptor format page: the default namespace, `owner` kinds (Group by default, or User) and the `<namespace>/<name>` shorthand. Removed: the claim that a reference to a missing entity does not fail ingestion and the advice on full refs in templates, which the pages do not state.

Method: documentation only; no commands were run.
