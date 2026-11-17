---
id: computing-software.web-development.storybook.play-function-basics
name: play-function-basics
category: computing-software
field: web-development
product: storybook
tags: [play-function, play, canvas, screen, story-interaction]
level: practitioner
status: docs-checked
description: "Write play functions that run after render, query the canvas, reach outside it with screen and compose across stories."
sources:
  - https://storybook.js.org/docs/writing-stories/play-function
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Play functions

Goal: script user interaction after a story renders.

A `play` function runs once the story finishes rendering. Steps show up in the Interactions panel.

```ts
import { expect } from 'storybook/test';

export const FilledForm = meta.story({
  play: async ({ canvas, userEvent }) => {
    await userEvent.type(canvas.getByTestId('email'), 'a@b.com');
    await userEvent.click(canvas.getByRole('button'));
    await expect(canvas.getByText('Welcome')).toBeInTheDocument();
  },
});
```

- `canvas` is a Testing Library query object scoped to the story root.
- To query outside the story root (a dialog rendered in a portal) use `screen` from `storybook/test`.
- Compose workflows: because stories are ES modules you can combine play functions, in the same way as args, to build longer flows with little code.

The page says the Interactions panel shows the step-by-step flow, and points to the interaction testing docs for the available API.

## Checked

Method: 2026-11-08 read docs/writing-stories/play-function.mdx from the Storybook repo. Kept the canvas, screen and composition claims; removed the `play-fn` tag line (it comes from the tags page, not this one), an unsupported "always await" rule and a Verify step. The sample code is illustrative and was not compared with the page snippet.
