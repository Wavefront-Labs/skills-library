---
id: computing-software.web-development.storybook.globals-and-toolbars
name: globals-and-toolbars
category: computing-software
field: web-development
product: storybook
tags: [globals, globaltypes, toolbar, initialglobals, theme-switcher]
level: practitioner
status: docs-checked
description: "Add custom toolbar menus with globalTypes and consume the value in a decorator."
sources:
  - https://storybook.js.org/docs/essentials/toolbars-and-globals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Globals and custom toolbars

Goal: let users switch a global (theme, locale) from the toolbar.

Globals are story-independent inputs, not args; read them from `context.globals`. `globalTypes` and `initialGlobals` can only be set in the preview file:

```tsx
export default definePreview({
  initialGlobals: { theme: 'light' },
  globalTypes: {
    theme: {
      description: 'Global theme for components',
      toolbar: {
        title: 'Theme',
        icon: 'circlehollow',
        items: ['light', 'dark'],
        dynamicTitle: true,
      },
    },
  },
  decorators: [
    (Story, context) => (
      <ThemeProvider theme={context.globals.theme}>
        <Story />
      </ThemeProvider>
    ),
  ],
});
```

- Menu items need `value` and `title`; `right` and `icon` are optional. `dynamicTitle` shows the current choice in the toolbar title. Icons come from `@storybook/icons`.
- Setting `globals` on a story overrides the global and disables the toolbar menu for it.
- Addons running in the manager read globals with `useGlobals()` from `storybook/manager-api`.

Verify: the new dropdown appears and changing it re-renders the story with the new theme.

## Checked
Date: 2026-11-04. Read the Toolbars and globals page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: preview-only declaration, toolbar fields, MenuItem fields, story-level override, icons package, manager-api hook.
Removed: an unconfirmed locale-with-flag example, and a claim that changing a global reruns decorators.
Method: documentation only; no commands were run.
