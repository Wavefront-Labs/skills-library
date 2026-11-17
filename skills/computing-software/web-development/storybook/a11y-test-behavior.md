---
id: computing-software.web-development.storybook.a11y-test-behavior
name: a11y-test-behavior
category: computing-software
field: web-development
product: storybook
tags: [a11y-test, todo-mode, accessibility-ci, vitest-a11y, violations]
level: practitioner
status: docs-checked
description: "Make accessibility violations warn or fail tests with parameters.a11y.test off, todo or error."
sources:
  - https://storybook.js.org/docs/writing-tests/accessibility-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Accessibility test behavior

Goal: decide whether a11y violations fail the build.

When the a11y addon runs alongside the Vitest addon, `parameters.a11y.test` controls the outcome per story:

| Value | Effect |
| --- | --- |
| `'off'` | no accessibility test (still checkable manually in the panel) |
| `'todo'` | runs; violations show as a warning in the UI only |
| `'error'` | runs; violations fail the test in UI, CLI and CI |

```ts
// preview: fail on violations everywhere
parameters: { a11y: { test: 'error' } },
// one known-bad story
export const Legacy = meta.story({ parameters: { a11y: { test: 'todo' } } });
```

`todo` is named like a literal TODO marker: use it for stories with known unfixed problems. In CI, `todo` produces no errors, warnings or output. Use `off` only for stories that deliberately show an antipattern.

The Vitest addon needs a Vite-based framework; Webpack projects must migrate first.

To exempt a rule rather than a story, disable it in `config.rules`. Exclude elements with `context`. To stop auto-analysis when browsing, set the `a11y.manual` global to true.

Verify: with `test: 'error'`, `vitest --project=storybook` exits non-zero on a violation.

## Checked
Date: 2026-11-04. Read the Accessibility testing, In CI and Interaction tests pages (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: off/todo/error table, `--project=storybook` command, Vite requirement.
Added: `todo` gives no CI output.
Method: documentation only; no commands were run.
