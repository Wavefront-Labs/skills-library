---
id: computing-software.web-development.storybook.parameters-and-inheritance
name: parameters-and-inheritance
category: computing-software
field: web-development
product: storybook
tags: [parameters, parameter-inheritance, story-parameters, global-parameters, metadata]
level: practitioner
status: docs-checked
description: "Set parameters at story, component and global level and understand how they merge."
sources:
  - https://storybook.js.org/docs/writing-stories/parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Parameters

Goal: configure Storybook features and addons per story, file or project.

Parameters are static, named metadata about a story, mostly used to control addon behavior.

```ts
// story
export const OnDark = meta.story({
  parameters: { backgrounds: { options: { dark: { name: 'Dark', value: '#222' } } } },
});
// component: parameters inside preview.meta({...})
// global: parameters inside definePreview({...}) in .storybook/preview.ts
```

Inheritance rules:
- More specific wins: story over component over global.
- Parameters are merged, so keys are only overwritten and never dropped. You can change one sub-parameter on one story and keep the rest.

Available parameters are listed in the separate parameters API reference. Global parameters are a common way to configure addons (for example the list of backgrounds every story can use). If you write an addon that relies on parameters, account for the merge behavior.

## Checked

Method: 2026-11-08 read docs/writing-stories/parameters.mdx from the Storybook repo. Kept the three levels and the two inheritance rules; dropped the `.extend` array claim, the `disable` pattern and namespace list (not on this page) and an unsupported Verify step. The sample code was not compared with the page snippets.
