---
id: computing-software.web-development.storybook.csf-4-overview
name: csf-4-overview
category: computing-software
field: web-development
product: storybook
tags: [csf, csf4, component-story-format, preview-file, story-files]
level: practitioner
status: docs-checked
description: "Understand CSF 4 file types, the preview file, meta and stories, and how renderers get type safety."
sources:
  - https://storybook.js.org/docs/writing-stories/csf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Component Story Format 4

Goal: know the shape of a CSF 4 project.

Two kinds of files:
- **Preview file** (`.storybook/preview.ts|tsx`): global config such as addons, decorators, parameters. It must default export a `definePreview(...)` result.
- **Story files** (`*.stories.ts|tsx|js|jsx`, or `.stories.svelte`): a `meta` plus named story exports.

```ts
// Button.stories.ts
import preview from '#.storybook/preview';
import { Button } from './Button';

const meta = preview.meta({ component: Button });

export const Primary = meta.story({ args: { primary: true } });
```

In CSF 4 the meta is not exported; CSF 3 and earlier require a default export of meta. CSF 1, 2 and 3 are still supported; do not mix formats in one file. CSF 4 is documented for React, Vue, Angular, Web Components and Svelte.

Annotations (`args`, `parameters`, `decorators`, `tags`) cascade: story overrides meta overrides preview. Not every annotation is valid at every level (for example `play` and `component` are not preview-level).

Use subpath imports (`"imports": {"#*": ["./*", "./*.ts", "./*.tsx"]}` in package.json) so the preview import `#.storybook/preview` works from any story file.

Verify: the sidebar lists each named export as a story under the meta title.

## Checked
Date: 2026-11-04. Read the CSF page (writing-stories/csf) and CSF 4 API page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: file types, default-exported preview, meta not exported, CSF 1/2/3 support, supported renderers, subpath import config, cascade order.
Removed: a claim that types carry through each chain step with no typing, and overbroad cascade wording; added the caveat that some annotations are not preview-level.
Method: documentation only; no commands were run.
