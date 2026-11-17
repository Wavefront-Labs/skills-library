---
id: computing-software.web-development.storybook.stories-in-unit-tests
name: stories-in-unit-tests
category: computing-software
field: web-development
product: storybook
tags: [composestory, unit-tests, testing-library, story-reuse, portable-stories-vitest]
level: advanced
status: docs-checked
description: "Reuse stories in Vitest unit tests with composeStories, override global config per test, and avoid common setup pitfalls."
sources:
  - https://storybook.js.org/docs/writing-tests/integrations/stories-in-unit-tests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Stories in unit tests

Goal: run Testing Library assertions against story setups.

Use `composeStories` (all stories of a file) or `composeStory` (one story) from your framework package. The returned components carry combined properties from story, meta and global config.

```tsx
import { composeStories } from '@storybook/react-vite';
import { render, screen } from '@testing-library/react';
import * as stories from './Form.stories';

const { Empty } = composeStories(stories);

test('shows validation', async () => {
  render(<Empty />);
  expect(screen.getByRole('button')).toBeDisabled();
});
```

- You must configure the test environment to use portable stories (the "apply project-level annotations" step) so stories compose with decorators and the rest of your Storybook config.
- `setProjectAnnotations` injects your global config (preview parameters, decorators) into tests. To override it for a test (for example a fixed locale via `globalTypes`, or specific decorators or parameters), extend `composeStory` / `composeStories` with test-specific configuration.
- For a single story use `composeStory`, supplying the story metadata (default export) as well; for several stories in one test use `composeStories`.
- The composed component carries the combined properties from story, meta and global config, so args and parameters can be read from it (React and Vue pages).
- In unit tests the examples use Testing Library `screen`; inside a story's `play`, prefer the provided `canvas`.
- For Next.js with Vite (React), if you see `Cannot find module 'sb-original/image-context'`, include `storybookNextJsPlugin`.
- Vue 2 and Angular have community-led addons that lack support for the latest stable Storybook.

## Checked

Method: 2026-11-08 read docs/writing-tests/integrations/stories-in-unit-tests.mdx from the Storybook repo. Removed an invented "per-test props" example and a claim about renderer coverage and a Vitest-addon recommendation (not on this page), added the single/multiple story guidance, removed a Verify step. The code block is illustrative.
