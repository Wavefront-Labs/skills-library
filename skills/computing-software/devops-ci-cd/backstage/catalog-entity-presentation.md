---
id: computing-software.devops-ci-cd.backstage.catalog-entity-presentation
name: catalog-entity-presentation
category: computing-software
field: devops-ci-cd
product: backstage
tags: [entity-presentation, display-name, entity-ref-link, backstage]
level: practitioner
status: docs-checked
description: "Show readable entity names across Backstage using the Entity Presentation API and EntityDisplayName."
sources:
  - https://backstage.io/docs/features/software-catalog/entity-presentation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The Entity Presentation API controls how entities appear throughout the UI. Instead of raw references such as `component:default/my-service`, it resolves a friendly name from fields such as `metadata.title` and `spec.profile.displayName`.

For React components, the simplest option is the `EntityDisplayName` component, which renders a styled name with an optional icon and tooltip:

```tsx
import { EntityDisplayName } from '@backstage/plugin-catalog-react';

<EntityDisplayName entityRef="component:default/my-service" />
```

Related pieces:

- `humanizeEntityRef` and `humanizeEntity` are deprecated because they only shorten the ref and do not resolve titles.
- The `useEntityPresentation` hook returns the presentation snapshot (`primaryTitle`, optional `secondaryTitle` and `Icon`) when you need the raw data, and may update over time.

In practice set `metadata.title` on Components and `spec.profile.displayName` on Users and Groups. The descriptor page says the title is for display only and entity references still use `metadata.name`.

## Checked

2026-11-03. Confirmed on the Entity Presentation page: the API resolves names from `metadata.title` and `spec.profile.displayName`, the `EntityDisplayName` component from `@backstage/plugin-catalog-react` (optional icon and tooltip), the `useEntityPresentation` hook and snapshot fields, and the deprecated `humanize*` functions. On the descriptor format page: title is display-only and references use `name`. Removed: claims that tables and cards all use the API and that a wrong name means a plugin ignores it.

Method: documentation only; no commands were run.
