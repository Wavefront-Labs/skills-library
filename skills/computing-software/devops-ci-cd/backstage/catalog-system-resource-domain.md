---
id: computing-software.devops-ci-cd.backstage.catalog-system-resource-domain
name: catalog-system-resource-domain
category: computing-software
field: devops-ci-cd
product: backstage
tags: [system-kind, domain-kind, resource-kind, backstage]
level: practitioner
status: docs-checked
description: "Model infrastructure and groupings with Resource, System and Domain entities and the core system model."
sources:
  - https://backstage.io/docs/features/software-catalog/system-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The system model has three core entities: Components (software), APIs (boundaries between components) and Resources (infrastructure a component needs at runtime, such as databases, topics, buckets or CDNs). Larger groupings are Systems and Domains.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Resource
metadata:
  name: artists-db
spec:
  type: database
  owner: artist-relations-team
  system: artist-engagement-portal
---
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: artist-engagement-portal
spec:
  owner: artist-relations-team
  domain: artists
```

Field summary from the descriptor docs:

- `Resource`: `owner` and `type` required, with optional `system`, `dependsOn` and `dependencyOf`.
- `System`: `owner` required, with optional `domain` and `type`.
- `Domain` groups related systems.

Components reference resources through `dependsOn` using a full reference such as `resource:default/artists-db`, which produces `dependsOn` and `dependencyOf` relations. Modelling resources lets you visualise resource footprint and build tooling around them. A System is a collection of resources and components that may expose or consume APIs, and a Domain groups systems that share terminology, domain models or business purpose (a bounded context). `spec.system` is optional on a Resource, and `System` also takes an optional `domain` reference.

## Checked

2026-11-03. Confirmed on the descriptor format page: Resource `spec.owner` and `spec.type` required with optional `system`, `dependsOn`, `dependencyOf`; System `spec.owner` required with optional `domain` and `type`; Domain definition; relation pairs for `dependsOn`/`dependencyOf`; the Resource description (databases, Pub/Sub topics, S3 buckets, CDNs) and visualising resource footprint. Removed: rollout advice and the "treat owner and system as required in practice" opinion, which the pages do not state.

Method: documentation only; no commands were run.
