---
id: computing-software.web-development.storybook.autodocs-custom-template
name: autodocs-custom-template
category: computing-software
field: web-development
product: storybook
tags: [docs-template, custom-docs-page, docs-container, toc, doc-blocks-template]
level: advanced
status: docs-checked
description: "Replace the default autodocs page with a custom template built from doc blocks or an MDX file."
sources:
  - https://storybook.js.org/docs/writing-docs/autodocs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom autodocs template

Goal: control the layout of generated docs pages.

Set `parameters.docs.page` in the preview file to a component built from doc blocks. The default template is:

```jsx
import { Title, Subtitle, Description, Primary, Controls, Stories } from '@storybook/addon-docs/blocks';

export const autoDocsTemplate = () => (
  <>
    <Title />
    <Subtitle />
    <Description />
    <Primary />
    <Controls />
    <Stories />
  </>
);
```

- `Title`, `Subtitle`, `Description` read component metadata.
- `Primary` shows the first story.
- `Controls` shows the args table.
- `Stories` lists the remaining stories.

Alternatives:
- An MDX template: put `isTemplate` on the `Meta` block of an MDX file and use it as the template.
- To change one component only, write an MDX file with `<Meta of={...} />` referencing that component's stories.

Table of contents: set `parameters.docs.toc` to `true` or an options object (`contentsSelector`, `disable`, `headingSelector`, `ignoreSelector`, `title`, `unsafeTocbotOptions`).

Verify: the docs page reflects your template.

## Checked
Date: 2026-11-04. Read the Autodocs page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: default template, import path, `parameters.docs.page`, toc options.
Added: the `isTemplate` MDX route and the toc option names. Removed "with zoom controls" for `Primary`, which the page does not state.
Method: documentation only; no commands were run.
