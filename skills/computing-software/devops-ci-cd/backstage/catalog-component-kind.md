---
id: computing-software.devops-ci-cd.backstage.catalog-component-kind
name: catalog-component-kind
category: computing-software
field: devops-ci-cd
product: backstage
tags: [component-kind, lifecycle, spec-owner, backstage]
level: intro
status: docs-checked
description: "Describe software as a Component entity with type, lifecycle, owner and relationship fields."
sources:
  - https://backstage.io/docs/features/software-catalog/descriptor-format
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A `Component` is a piece of software: a service, website, library or data pipeline. Its `spec` has required and optional fields.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: artist-web
spec:
  type: service
  lifecycle: production
  owner: artist-relations-team
  system: artist-engagement-portal
  providesApis:
    - artist-api
  consumesApis:
    - payments-api
  dependsOn:
    - resource:default/artists-db
```

- `spec.type` is required. Common values are `service` (a backend service, typically exposing an API), `website` and `library` (such as an npm module or Java library). Organisations may define their own.
- `spec.lifecycle` is required: `experimental` (early, non-production), `production` (established, owned and maintained) or `deprecated` (at the end of its life).
- `spec.owner` is required and is a reference to a Group or User, for example `group:default/artist-relations-team`.
- `spec.system` places the component in a System.
- `spec.subcomponentOf` nests a component in another.
- `providesApis`, `consumesApis` and `dependsOn` are arrays of entity references and generate relations (`providesApi`/`apiProvidedBy`, `consumesApi`/`apiConsumedBy`, `dependsOn`/`dependencyOf`).

The catalog accepts any `type` and `lifecycle` value, so an organisation should establish a taxonomy. `spec.owner` is mainly for display and should not be used to assign runtime authorization.

## Checked

2026-11-03. Confirmed on the descriptor format page (Kind: Component): required `spec.type`, `spec.lifecycle`, `spec.owner`; optional `system`, `subcomponentOf`, `providesApis`, `consumesApis`, `dependsOn`; the well-known type values `service`, `website`, `library`; lifecycle values `experimental`, `production`, `deprecated` with their meanings; the generated relation pairs; and the owner display-only note. Removed: claims about graph/API tabs, scorecards and broken ownership relations, which the page does not state.

Method: documentation only; no commands were run.
