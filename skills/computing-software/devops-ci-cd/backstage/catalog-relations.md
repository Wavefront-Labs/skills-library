---
id: computing-software.devops-ci-cd.backstage.catalog-relations
name: catalog-relations
category: computing-software
field: devops-ci-cd
product: backstage
tags: [relations, owned-by, depends-on, backstage]
level: practitioner
status: docs-checked
description: "Know the paired relation types the catalog emits, such as ownedBy and ownerOf or dependsOn and dependencyOf."
sources:
  - https://backstage.io/docs/features/software-catalog/well-known-relations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Relations are directed edges between entities. Most come in pairs, with one side stored on each entity, and they are derived from `spec` fields rather than written directly.

The documented pairs are:

- `ownedBy` and `ownerOf`, from `spec.owner`.
- `providesApi` and `apiProvidedBy`, from `spec.providesApis`.
- `consumesApi` and `apiConsumedBy`, from `spec.consumesApis`.
- `dependsOn` and `dependencyOf`, from `spec.dependsOn`.
- `parentOf` and `childOf`, for Group hierarchies.
- `memberOf` and `hasMember`, between Users and Groups.
- `partOf` and `hasPart`, for example a component in a system.

On an entity as returned by the API:

```json
{
  "relations": [
    { "type": "ownedBy", "targetRef": "group:default/artist-relations-team" },
    { "type": "partOf", "targetRef": "system:default/artist-engagement-portal" }
  ]
}
```

Tips: edit the source `spec` field and let the catalog produce both sides; do not try to hand-write a reverse relation. Relations are read-only on the entity: the descriptor page says catalog processors deduce them and they are the authoritative source, so a plugin should read the relation rather than `spec.owner`.

## Checked

2026-11-03. Confirmed on the Well-known relations page: the seven relation pairs listed (ownedBy/ownerOf, providesApi/apiProvidedBy, consumesApi/apiConsumedBy, dependsOn/dependencyOf, parentOf/childOf, memberOf/hasMember, partOf/hasPart) and that relations are directional with an opposite on the other entity. On the descriptor format page: `relations` is a read-only list with `type` and `targetRef` produced by catalog processors and authoritative. Removed: graph and diagram gaps and the custom relation type remark, which the pages do not state.

Method: documentation only; no commands were run.
