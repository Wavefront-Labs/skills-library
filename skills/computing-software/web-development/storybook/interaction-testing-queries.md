---
id: computing-software.web-development.storybook.interaction-testing-queries
name: interaction-testing-queries
category: computing-software
field: web-development
product: storybook
tags: [interaction-testing, testing-library, canvas-queries, getbyrole, findby]
level: practitioner
status: docs-checked
description: "Query story DOM in play functions with canvas and pick the right Testing Library query variant."
sources:
  - https://storybook.js.org/docs/writing-tests/interaction-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Interaction tests: querying the canvas

Goal: find elements the way a user would.

Every story is a render test. Add a `play` function for behavior. `canvas` (a play function argument) is a queryable element containing the story; queries come from Testing Library and take the form `<type><subject>`.

| Query | 0 matches | 1 match | >1 matches | Awaited |
| --- | --- | --- | --- | --- |
| `getBy...` | throws | element | throws | no |
| `queryBy...` | `null` | element | throws | no |
| `findBy...` | throws | element | throws | yes |
| `getAllBy...` | throws | array | array | no |
| `queryAllBy...` | `[]` | array | array | no |
| `findAllBy...` | throws | array | array | yes |

Subjects in the docs' priority order (closest to real use first): `ByRole`, `ByLabelText`, `ByPlaceholderText`, `ByText`, `ByDisplayValue`, `ByAltText`, `ByTitle`, `ByTestId`. Use `ByTestId` as a last resort.

```ts
await canvas.findByRole('button', { name: 'Submit' });
canvas.getByText('An example heading');
canvas.getAllByRole('listitem');
```

Web Components with shadow DOM: add `shadow-dom-testing-library` in the preview file to get queries such as `findByShadowRole`.

Verify: queries resolve and each step appears in the Interactions panel.

## Checked
Date: 2026-11-04. Read the Interaction tests page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: query table, subject priority order, example queries, shadow DOM library (web-components only).
Method: documentation only; no commands were run.
