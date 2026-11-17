---
id: computing-software.devops-ci-cd.backstage.catalog-api-kind
name: catalog-api-kind
category: computing-software
field: devops-ci-cd
product: backstage
tags: [api-kind, openapi, spec-definition, backstage]
level: practitioner
status: docs-checked
description: "Register an API entity with its type, lifecycle, owner and an inline or referenced definition."
sources:
  - https://backstage.io/docs/features/software-catalog/descriptor-format
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

An `API` entity describes the boundary between components. It is implemented by a Component and consumed by others, and carries its machine-readable definition so Backstage can render it.

```yaml
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: petstore
  description: The Petstore API
spec:
  type: openapi
  lifecycle: production
  owner: petstore@example.com
  system: pet-platform
  definition:
    $text: https://petstore.swagger.io/v2/swagger.json
```

Required spec fields are `type`, `lifecycle`, `owner` and `definition`; `system` is optional.

- `spec.type` names the definition format, for example `openapi`.
- `spec.definition` holds the full text. Use the `$text` substitution to load it from a file or URL instead of pasting it into the YAML.
- A component declares `providesApis` or `consumesApis`, and the catalog derives the `apiProvidedBy` and `apiConsumedBy` relations.

The system model docs also describe API visibility: public, restricted or private. Specify the API base URL inside the definition, otherwise some widgets (such as OpenAPI) fall back to the base URL of the Backstage instance. Remote `$text` targets outside the normal integrations must be allowed in the `backend.reading.allow` list.

## Checked

2026-11-03. Confirmed on the descriptor format page (Kind: API): required `spec.type`, `spec.lifecycle`, `spec.owner`, `spec.definition`, optional `spec.system`; well-known types (openapi, asyncapi, graphql, grpc); the `$text` substitution and the `backend.reading.allow` requirement; the base-URL note. On the System model page: API visibility public, restricted or private. On the descriptor page the provides/consumes relation pairs. Removed: the advice to generate definitions in CI, which the pages do not give.

Method: documentation only; no commands were run.
