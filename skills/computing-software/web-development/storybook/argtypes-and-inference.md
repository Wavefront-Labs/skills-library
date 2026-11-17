---
id: computing-software.web-development.storybook.argtypes-and-inference
name: argtypes-and-inference
category: computing-software
field: web-development
product: storybook
tags: [argtypes, arg-types, docgen, inference, component-meta]
level: practitioner
status: docs-checked
description: "Annotate args with argTypes and understand how Storybook infers them from your component source."
sources:
  - https://storybook.js.org/docs/api/arg-types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# argTypes and automatic inference

Goal: describe args so Controls and Docs show the right names, types and inputs.

Storybook infers argTypes from the meta `component` using static analysis:
- React: TypeScript sources read on the server, or react-docgen / react-docgen-typescript if the server is off
- Vue: vue-component-meta
- Angular (Vite): TypeScript sources, or compodoc if the server is off; Angular (Webpack): compodoc
- Web Components: `custom-element.json`
- Ember: YUIDoc

Manual argTypes override inference and can be set at project (preview), component (meta) or story level:

```ts
const meta = preview.meta({
  component: Button,
  argTypes: {
    variant: { control: 'radio', options: ['primary', 'secondary'] },
    internalId: { table: { disable: true } },
  },
});
```

Use `argTypes` to constrain accepted values, document args (`description`), or hide a row (`table.disable`).

Verify: the Controls panel lists the arg with the control you set.

## Checked
Date: 2026-11-04. Read the ArgTypes API page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: per-framework inference tools, manual override, `table.disable`.
Removed: a gotcha about Angular (webpack), Ember and Web Components needing extra setup, and an `onClick: { action }` example line; neither is on the page.
Method: documentation only; no commands were run.
