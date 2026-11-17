---
id: computing-software.web-development.storybook.mocking-providers
name: mocking-providers
category: computing-software
field: web-development
product: storybook
tags: [mock-provider, context-provider, theme-provider, redux-provider, decorator-provider]
level: practitioner
status: docs-checked
description: "Mock React-style context providers globally with a decorator and vary the provided value per story via parameters."
sources:
  - https://storybook.js.org/docs/writing-stories/mocking-data-and-modules/mocking-providers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mocking providers

Goal: give components the context they expect (theme, store, router) in every story.

Applies to renderers using JSX such as React or Solid. Add a global decorator in the preview file (use a `.tsx` or `.jsx` extension so JSX is allowed):

```tsx
decorators: [
  (Story, { parameters }) => {
    const theme = parameters.theme ?? 'light';
    return (
      <ThemeProvider theme={themes[theme]}>
        <Story />
      </ThemeProvider>
    );
  },
],
```

Then a story picks a value without repeating the decorator:

```ts
export const Dark = meta.story({ parameters: { theme: 'dark' } });
```

This uses the decorator's second (context) argument to read `parameters`, so you avoid defining a decorator per story, and you can provide any value: theme, user role or mock data. The same pattern works with a Redux store provider (see the Screens chapter of the Intro to Storybook tutorial).

The page applies only to JSX renderers such as React, Preact and Solid.

## Checked

Method: 2026-11-08 read docs/writing-stories/mocking-data-and-modules/mocking-providers.mdx from the Storybook repo. Claims match; removed an unsupported `context.globals` toolbar suggestion, an unsupported Verify step, and noted the renderer scope. Code samples are illustrative and were not compared with the page snippets.
