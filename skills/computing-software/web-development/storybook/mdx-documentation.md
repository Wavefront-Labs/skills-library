---
id: computing-software.web-development.storybook.mdx-documentation
name: mdx-documentation
category: computing-software
field: web-development
product: storybook
tags: [mdx, mdx-docs, meta-of, docs-blocks, documentation-pages]
level: practitioner
status: docs-checked
description: "Write MDX documentation pages that reference stories with the Meta and Canvas doc blocks."
sources:
  - https://storybook.js.org/docs/writing-docs/mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MDX documentation

Goal: write long-form docs next to your stories.

MDX mixes Markdown with JSX. CSF defines stories; MDX documents them.

```mdx
{/* Checkbox.mdx */}
import { Meta, Canvas, Controls } from '@storybook/addon-docs/blocks';
import * as CheckboxStories from './Checkbox.stories';

<Meta of={CheckboxStories} />

# Checkbox

A checkbox lets users toggle an option.

<Canvas of={CheckboxStories.Unchecked} />
<Controls of={CheckboxStories.Unchecked} />
```

Rules:
- Pass the full set of exports of the story file (`import * as ...`) to `Meta of`, not the component itself.
- `Meta` places the page next to the component's stories; the default sidebar node is titled "Docs", changeable with `name`. Use the `title` prop (e.g. `<Meta title="path/to/node" />`) to place a docs node anywhere.
- Comments are JSX blocks containing JS comments: `{/* ... */}`.
- Blocks are separated by blank lines; failing to separate them can cause cryptic parse errors.
- CommonMark by default; extend with GFM by installing `remark-gfm` separately and enabling it in the main config (for tables, footnotes).
- Doc Blocks and any React components can be embedded, for example your own dos and don'ts list.
- Omit `Meta` for a standalone page and Storybook places it by file location, as a Docs entry; if it overrides an autodocs page enabled through `tags`, remove that tag to avoid errors. `Meta` with no other props or blocks makes an unattached, documentation-only page.
- Storybook's MDX rendering is React-only, while stories render in their own runtime.
- Link to docs or stories with `?path=/docs/<id>` or `?path=/story/<id>`.

## Checked

Method: 2026-11-08 read docs/writing-docs/mdx.mdx from the Storybook repo. Corrected the GFM statement, the `Meta` title/name behaviour and the standalone-page guidance; added React-only and linking notes; removed a Verify step. The example block was not compared with the page snippets.
