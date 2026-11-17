---
id: computing-software.web-development.storybook.doc-blocks-reference
name: doc-blocks-reference
category: computing-software
field: web-development
product: storybook
tags: [doc-blocks, canvas-block, controls-block, source-block, argtypes-block]
level: practitioner
status: docs-checked
description: "Use Storybook doc blocks (Canvas, Story, Source, Controls, ArgTypes, Stories, Markdown, ColorPalette and more) in MDX or templates."
sources:
  - https://storybook.js.org/docs/writing-docs/doc-blocks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Doc blocks

Goal: choose the right block for documentation pages.

Import from `@storybook/addon-docs/blocks`. Available blocks: `ArgTypes`, `Canvas`, `ColorPalette`, `Controls`, `Description`, `IconGallery`, `Markdown`, `Meta`, `Primary`, `Source`, `Stories`, `Story`, `Subtitle`, `TableOfContents`, `Title`, `Typeset`, `Unstyled`, plus the `useOf` hook for building custom blocks.

Doc blocks are designed for MDX and do not work in stories.

Used in MDX:

```mdx
<Meta of={ButtonStories} />
<Canvas of={ButtonStories.Primary} />
<ArgTypes of={ButtonStories} />
```

Or in the autodocs template. Parameter namespaces: `parameters.docs.{argTypes,canvas,controls,source,story,toc}`.

`Story` `inline` defaults to `parameters.docs.story.inline` or true. Gotcha: with `inline: false`, Controls do not update the story.

Verify: each block renders in the docs page without errors.

## Checked
Date: 2026-11-04. Read the Doc blocks page and the Story doc block page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: block list, import path, MDX-only note, parameter namespaces, `inline` default and effect.
Removed: per-block one-line descriptions that the index page does not state.
Method: documentation only; no commands were run.
