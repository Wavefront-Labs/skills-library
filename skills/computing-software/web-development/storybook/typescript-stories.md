---
id: computing-software.web-development.storybook.typescript-stories
name: typescript-stories
category: computing-software
field: web-development
product: storybook
tags: [typescript, meta-storyobj, satisfies, typed-args, csf3-types]
level: practitioner
status: docs-checked
description: "Type stories with CSF 4 inference, or Meta and StoryObj in CSF 3, including satisfies and custom args."
sources:
  - https://storybook.js.org/docs/writing-stories/typescript
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Writing stories in TypeScript

Goal: get autocompleted, checked args with minimal annotations.

Storybook has built-in TypeScript support with zero configuration. CSF 4 infers component types automatically (for React, Vue, Angular, web components and Svelte) and the page recommends it for new TypeScript stories; add types only for custom args (pass the custom args type to `preview.type`; for args only some stories use, Svelte docs point to `meta.type`).

CSF 3 files use the `Meta` and `StoryObj` utility types:

```ts
import type { Meta, StoryObj } from '@storybook/react-vite';
import { Button } from './Button';

const meta = { component: Button } satisfies Meta<typeof Button>;
export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = { args: { primary: true } };
```

Details:
- `Meta` and `StoryObj` are generics taking an optional component type (`typeof Button`) or props type; with it, TypeScript rejects invalid args and types decorators, play functions and loaders.
- `satisfies` gives stricter checking: missing required and invalid args are reported, a shared play function is not flagged as possibly undefined, and passing `typeof meta` to `StoryObj` tells TypeScript that args may be set at meta or story level.
- Custom args not among the component's props: in CSF 3 combine the props type and the custom args type with an intersection type.
- Angular and web components cannot get the extra `satisfies` safety; their CSF 4 inferred types are optional (`Partial<T>`) unless you pass a props type to `preview.type`.

## Checked

Method: 2026-11-08 read docs/writing-stories/typescript.mdx from the Storybook repo. Corrected the custom-args guidance (intersection type in CSF 3), expanded the `satisfies` reasons and renderer caveats, and removed a Verify step. The CSF 3 code block is illustrative (framework import path not on the page text).
