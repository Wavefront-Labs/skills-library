---
id: computing-software.web-development.frontend-development.storybook-stories-and-interaction-tests
name: storybook-stories-and-interaction-tests
category: computing-software
field: web-development
product: frontend-development
tags: [storybook-interaction-tests, storybook, csf3, play-function, component-testing, frontend-testing]
level: practitioner
status: docs-checked
description: "Writing Storybook CSF stories with args, play-function interaction tests with canvas, userEvent and expect, and running them with the Vitest addon."
sources:
  - https://storybook.js.org/docs/writing-stories
  - https://storybook.js.org/docs/writing-tests/interaction-testing
  - https://storybook.js.org/docs/writing-tests/integrations/vitest-addon
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storybook stories and interaction tests

## 1. Stories (Component Story Format)
```tsx
// Replace your-framework with the framework you use, e.g. react-vite
import type { Meta, StoryObj } from "@storybook/your-framework";
import { fn } from "storybook/test";
import { LoginForm } from "./LoginForm";

const meta = {
  component: LoginForm,
  args: { onSubmit: fn() },     // spy on the callback arg
} satisfies Meta<typeof LoginForm>;
export default meta;
type Story = StoryObj<typeof meta>;

export const EmptyForm: Story = {};
```
- Each named export (UpperCamelCase recommended) is a story; by default it renders the meta's component with the args. Use `render` for something else and spread `args` onto the component so Controls keep working.
- Args are live-editable in the Controls panel; the Actions addon detects callback args and logs their calls. Spread `Primary.args` to build variants of a story.

## 2. Interaction tests with a play function
```tsx
import { expect } from "storybook/test";

export const FilledForm: Story = {
  play: async ({ args, canvas, userEvent }) => {
    await userEvent.type(canvas.getByLabelText("Email"), "email@provider.com");
    await userEvent.type(canvas.getByLabelText("Password"), "a-random-password");
    await userEvent.click(canvas.getByRole("button", { name: "Log in" }));
    await expect(args.onSubmit).toHaveBeenCalled();
  },
};
```
- `canvas` queries the story with Testing Library methods named `<type><subject>` (`getBy`, `queryBy`, `findBy`, plus `...AllBy`). Prefer queries that resemble how people use the UI (role first); `ByTestId` is a last resort.
- `userEvent` simulates interactions (`click`, `type`, `hover`, `tab`, `selectOptions`, `clear`...). Always `await` userEvent and `expect` calls so the Interactions panel can log them.
- `expect` combines Vitest's `expect` with `@testing-library/jest-dom` matchers. `fn` comes from `storybook/test`.
- Group steps with `step("label", async () => { ... })`.
- To run code before render (for example mocking the date with `mockdate`), destructure `mount` in `play` and `await mount()`; the framework must transpile to ES2017 or newer.
- `beforeEach` on the meta or in `.storybook/preview.*` runs before each story and can return a cleanup function; `beforeAll` in preview runs once. Do not reset state in `afterEach`. `fn()` mocks are restored automatically.
- The Interactions panel shows the steps, with controls to pause, resume, rewind and step, and shows failures.

## 3. Run them as tests
- Vitest addon: `npx storybook add @storybook/addon-vitest`. It configures Vitest browser mode with Playwright's Chromium, transforms stories into Vitest tests via portable stories, and needs a Vite-based Storybook framework. Run from the Storybook UI (Run component tests), editor, CLI or CI; a typical script is `vitest --project=storybook`.
- Results can differ between the addon (Vitest) and the Interactions panel because they run in different environments.
- Without the Vitest addon you can use the test-runner in the terminal or CI.
- The docs recommend combining interaction tests with visual testing, since interaction tests are costly to maintain on every component.

## Verify
- [ ] CI runs the story tests; breaking a component's label makes the play function fail.

## Checked

2026-11-09. Read in full the Writing stories, Interaction testing and Vitest addon pages (the Vitest page's setup, scripts, how-it-works and browser-mode sections). Confirmed the story, args, play, query, userEvent, expect, fn, mount, step, beforeEach/beforeAll/afterEach guidance, run options and the Vitest addon behaviour. Removed: the MSW handler example and loaders, the decorators example, a11y-failure configuration, Chromatic and Playwright screenshot advice, the Storybook 9 version and import-path history, `storybook@latest init`, and the test-runner URL command, which these pages do not state.

Method: documentation only; no commands were run.
