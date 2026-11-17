---
id: computing-software.web-development.storybook.play-mount-and-before-each
name: play-mount-and-before-each
category: computing-software
field: web-development
product: storybook
tags: [mount, beforeeach, play-mount, mock-date, cleanup]
level: advanced
status: docs-checked
description: "Run setup before render with mount in play, and use beforeEach for mocks that clean up after each story."
sources:
  - https://storybook.js.org/docs/writing-tests/interaction-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mount and beforeEach

Goal: set up state or mocks before the component renders.

`mount` in play (not available this way for Angular, which uses an async `beforeEach` for the story instead):

```ts
export const Dated = meta.story({
  play: async ({ mount, canvas }) => {
    MockDate.set('2024-02-14');
    await mount();
    await expect(canvas.getByText('Feb 14')).toBeVisible();
  },
});
```
Two requirements:
1. You must destructure `mount` from the context (the argument passed to your play function); this makes sure Storybook does not start rendering the story before the play function begins.
2. Your Storybook framework or builder must be configured to transpile to ES2017 or newer; otherwise destructuring and async/await are transpiled away and Storybook cannot recognise your use of `mount`.

Calling `mount()` with no arguments renders the story's render function. Mounting a specific component ignores the story's render function, so forward `args` to it.

`beforeEach` (in component meta or the preview file) runs before each story and may return a cleanup function, which runs after each story, when the story is remounted or navigated away from:

```ts
async beforeEach() {
  MockDate.set('2024-02-14');
  return () => MockDate.reset();
},
```
Set it in the meta to apply to every story in the file; set it in the preview file (`.storybook/preview.*`) to apply to every story in the project. Prefer the preview file for resetting state; use the meta cleanup when a component's needs are unusual. `fn()` mocks do not need restoring, Storybook does that before rendering a story.

Do not reset state in `afterEach`: it runs after the play function and would hide the story's end state. Use the `beforeEach` cleanup function instead.

Verify: the story renders with the mocked date and the date resets afterwards.

## Checked
Read the whole interaction-testing page (storybookjs/storybook docs/writing-tests/interaction-testing.mdx) and the page's before-each-in-meta-mock-date snippet on 2026-11-08. Confirmed the two `mount` requirements, `beforeEach` in meta and preview with returned cleanup timing, the preview-versus-meta guidance, the `fn()` restore note, the `afterEach` caveat, and the `meta.story` / `play({ canvas })` form (CSF 4 snippet). Removed: the claim that story-level `beforeEach` exists beyond the Angular note.
Method: docs-only read of cited pages, 2026-11-08
