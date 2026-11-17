---
id: computing-software.devops-ci-cd.backstage.plugin-catalog-integration
name: plugin-catalog-integration
category: computing-software
field: devops-ci-cd
product: backstage
tags: [entity-page, catalog-integration, entity-annotation, backstage]
level: practitioner
status: docs-checked
description: "Show a plugin on catalog entity pages with useEntity and the entity page layout."
sources:
  - https://backstage.io/docs/plugins/integrating-plugin-into-software-catalog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A plugin can appear as a tab or card on a catalog entity page. This page is marked legacy for the old frontend system and describes an advanced, experimental feature whose API may change; the new frontend system uses `EntityCardBlueprint` and `EntityContentBlueprint` instead.

1. Create a plugin the usual way (`yarn new`, then `frontend-plugin`).
2. Read the current entity inside the plugin with the `useEntity` hook from `@backstage/plugin-catalog-react`. It uses a React context supplied by the entity page.

```tsx
import { useEntity } from '@backstage/plugin-catalog-react';

export const MyPluginEntityContent = () => {
  const entity = useEntity();
  // Do something with the entity data...
};
```

3. Import the plugin in `packages/app/src/components/Catalog/EntityPage.tsx` and add it to the entity page. `EntitySwitch` chooses the page by kind (for example `isKind('component')`). To add a tab to an existing page, add an `EntityLayout.Route` with a `path` and `title` that renders your component.

```tsx
<EntityLayout.Route path="/your-custom-route" title="CustomTitle">
  <MyPluginEntityContent />
</EntityLayout.Route>
```

If you are extending the catalog model with a new kind, add a new case to `EntitySwitch` instead.

## Checked

2026-11-03. Confirmed on the Integrate into the Software Catalog page: the legacy notice and the new-frontend blueprints, the experimental and advanced warning, `yarn new` with `frontend-plugin`, `useEntity` from `@backstage/plugin-catalog-react` and its React context, the `EntityPage.tsx` path, `EntitySwitch` with `isKind`, and adding a tab with `EntityLayout.Route`. Removed: the annotation-driven pattern, the `isXAvailable` helper and `EntityXCard`/`EntityXContent` export conventions, the annotation reuse advice and the search collator remark, none of which the page states. Note `useEntity()` is shown on the page without destructuring. The description was narrowed to match.

Method: documentation only; no commands were run.
