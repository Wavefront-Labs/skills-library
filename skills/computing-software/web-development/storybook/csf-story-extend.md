---
id: computing-software.web-development.storybook.csf-story-extend
name: csf-story-extend
category: computing-software
field: web-development
product: storybook
tags: [story-extend, extend, story-reuse, annotations-merge, csf]
level: practitioner
status: docs-checked
description: "Create a new story from an existing one with .extend and know how args, parameters, decorators and tags merge."
sources:
  - https://storybook.js.org/docs/writing-stories/csf/api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Story.extend

Goal: build a variant story on top of another without copying its definition.

```ts
export const Example = meta.story({
  args: { primary: true, exampleArray: ['a', 'b'], exampleObject: { a: 'a', b: 'b' } },
  parameters: { exampleArray: ['a', 'b'], exampleObject: { a: 'a', b: 'b' } },
  tags: ['a'],
});

export const ExtendedExample = Example.extend({
  args: { disabled: true, exampleArray: ['c'], exampleObject: { a: 'c' } },
  parameters: { disabled: true, exampleArray: ['c'], exampleObject: { a: 'c' } },
  tags: ['b'],
});
```

Result for `ExtendedExample`:
- `args`: shallow merged, so `{ primary: true, disabled: true, exampleArray: ['c'], exampleObject: { a: 'c' } }` (the `b` key is dropped).
- `parameters`: deep merged except arrays, which are replaced: `{ exampleArray: ['c'], exampleObject: { a: 'c', b: 'b' }, disabled: true }`.
- `decorators` and `tags` are concatenated: tags become `['a', 'b']`.

In Svelte CSF use the `extend` attribute on `<Story>`; its value is the `name` of another story, so that story needs a `name`.

Gotcha: because args are shallow merged, override a whole object arg rather than expecting nested keys to merge.

Verify: the extended story's Controls panel shows the merged args.

## Checked
Date: 2026-11-04. Read the CSF 4 API page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: merge rules and the results above, Svelte `extend`.
Fixed: the earlier example was internally inconsistent (parameters lacked `exampleArray`); replaced with the page's example and results.
Method: documentation only; no commands were run.
