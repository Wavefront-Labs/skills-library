---
id: computing-software.web-development.storybook.snapshot-portable-stories
name: snapshot-portable-stories
category: computing-software
field: web-development
product: storybook
tags: [portable-stories, composestories, snapshot-testing, setprojectannotations, vitest-snapshots]
level: advanced
status: docs-checked
description: "Reuse stories in Vitest or Jest with the Portable Stories API for snapshot tests."
sources:
  - https://storybook.js.org/docs/writing-tests/snapshot-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Snapshot tests with portable stories

Goal: render stories inside Vitest or Jest and compare snapshots.

Storyshots is deprecated; use Portable Stories. Compose a story with its annotations (args, decorators, parameters) via `composeStories` or `composeStory`, render it in your test renderer, and snapshot the output:

```ts
import { composeStories } from '@storybook/react-vite';
import { render } from '@testing-library/react';
import * as stories from './Button.stories';

const { Primary } = composeStories(stories);

test('Button snapshot', () => {
  const { container } = render(<Primary />);
  expect(container).toMatchSnapshot();
});
```

Setup: Portable Stories exist for Vitest and Jest. If you use Storybook Test, Vitest is already configured; otherwise follow the portable-stories docs step "apply project-level annotations" (the project-level annotations function is `setProjectAnnotations`).

Testing an expected error: give the story `tags: ['!dev', '!test']` so it is hidden from the sidebar and not run by Storybook Test, then assert the throw in a unit test, e.g. `await expect(ThrowError.run()).rejects.toThrowError('...')` on the composed story.

Gotcha: snapshots are noisy and hard to maintain when they hold too much information; the page says visual tests or interaction tests usually fit UI components better, and snapshots suit non-visual output such as ensuring an error is thrown. On a mismatch the test fails with a diff (a one-token class change is easy to miss in it).

## Checked

Method: 2026-11-08 read docs/writing-tests/snapshot-testing.mdx from the Storybook repo. Claims match; corrected the Vitest-addon setup statement (the page says Storybook Test), added the `.run()` error assertion, and replaced an unsupported Verify step. The first code block is illustrative (the page uses its own snippet).
