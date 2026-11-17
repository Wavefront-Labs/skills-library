---
id: computing-software.web-development.storybook.csf-define-preview-and-main
name: csf-define-preview-and-main
category: computing-software
field: web-development
product: storybook
tags: [definepreview, definemain, preview-config, addon-types, csf]
level: practitioner
status: docs-checked
description: "Use defineMain and definePreview to get typed config, and register addons so their types reach your stories."
sources:
  - https://storybook.js.org/docs/writing-stories/csf/api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# defineMain and definePreview

Goal: type-safe project configuration in CSF 4.

```ts
// .storybook/main.ts
// Replace your-framework with the framework package you use
import { defineMain } from '@storybook/your-framework/node';

export default defineMain({
  framework: '@storybook/your-framework',
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: ['@storybook/addon-a11y'],
});
```

```ts
// .storybook/preview.ts
import { definePreview } from '@storybook/your-framework';
import addonA11y from '@storybook/addon-a11y';

export default definePreview({
  addons: [addonA11y()],
  parameters: { layout: 'centered' },
});
```

Notes:
- `defineMain` configures `main.ts`; `definePreview` takes the global annotations.
- The `addons` annotation (preview only) types addons, so their parameters and globals are type-checked.
- `npx storybook add <addon-name>` or `storybook dev` updates the preview config to reference addons.
- Official addons are imported by default (`import addonA11y from '@storybook/addon-a11y'`, used as `addons: [addonA11y()]`); community addons are imported as a namespace.
- For Svelte, add `svelte` to the story globs.

Verify: hovering `parameters` in a story shows addon-provided keys such as `a11y`.

## Checked
Date: 2026-11-04. Read the CSF 4 API page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: `defineMain`/`definePreview`, the `addons` annotation, `storybook add` behavior, default versus namespace imports, Svelte globs.
Fixed: the main example lacked its import; the preview example used addon-docs where the page uses a11y; both now follow the page's import pattern with a framework placeholder.
Method: documentation only; no commands were run.
