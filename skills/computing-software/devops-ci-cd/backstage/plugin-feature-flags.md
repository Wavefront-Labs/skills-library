---
id: computing-software.devops-ci-cd.backstage.plugin-feature-flags
name: plugin-feature-flags
category: computing-software
field: devops-ci-cd
product: backstage
tags: [feature-flags, plugin-flags, feature-flagged, backstage]
level: practitioner
status: docs-checked
description: "Declare plugin and app feature flags that users can toggle, and gate UI with FeatureFlagged."
sources:
  - https://backstage.io/docs/plugins/feature-flags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Feature flags let users switch features on or off from the Backstage settings page. Declare them in the plugin that owns the feature:

```ts
import { createPlugin } from '@backstage/core-plugin-api';

export const examplePlugin = createPlugin({
  id: 'example',
  featureFlags: [
    {
      name: 'show-example-feature',
      description: 'Enables the new beta dashboard view',
    },
  ],
});
```

Or declare an application-level flag when creating the app:

```ts
const app = createApp({
  featureFlags: [
    {
      pluginId: '',
      name: 'tech-radar',
      description: 'Enables the tech radar plugin',
    },
  ],
});
```

- `pluginId` is required for flags used in plugins and may be left blank for an app-level flag.
- Flags default to off; users enable them under Settings > Feature Flags, the choice is saved in browser local storage and a page refresh may be needed. If `description` is omitted, a default `Registered in {pluginId} plugin` message is shown.
- The `FeatureFlagged` component renders its children only when a flag is on (or off, using the `without` prop).
- Evaluate state in code with the feature flags API, using `featureFlagsApi.isActive('name')`.

The page documents the old frontend system (`createPlugin` from `@backstage/core-plugin-api`, `createApp` from `@backstage/app-defaults`); `FeatureFlagged` and `featureFlagsApiRef` work the same in both systems.

## Checked

2026-11-03. Confirmed against the Backstage Feature Flags page: plugin and app declarations, `pluginId`, settings location, local storage, `FeatureFlagged` `with`/`without`, `isActive`. Removed: the security and naming advice (not in the page).

Method: documentation only; no commands were run.
