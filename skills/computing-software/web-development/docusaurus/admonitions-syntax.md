---
id: computing-software.web-development.docusaurus.admonitions-syntax
name: admonitions-syntax
category: computing-software
field: web-development
product: docusaurus
tags: [admonitions, callouts, prettier, nested-admonitions, admonition-component]
level: intro
status: docs-checked
description: "Write Docusaurus admonitions with the triple-colon syntax: types, titles, CSS classes and IDs, nesting, Prettier-safe spacing, and the Admonition component in JSX."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-admonitions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Wrap text in three colons plus a type: `note`, `tip`, `info`, `warning`, `danger`.

```md
:::tip

Some **content** with _Markdown_ syntax.

:::
```

Leave blank lines around the opening and closing directives, otherwise Prettier may reformat into invalid syntax (for example `::: note Hello world:::`).

Title, classes and ID:

```md
:::note[Your Title **with** some _Markdown_ syntax!]
:::note[With css classes]{.padding--lg .text--italic}
:::note{#admonition-id}
:::note{.padding--lg #admonition-id-2}
```

Nesting uses more colons for each parent level:

```md
:::::info Parent

::::danger Child

:::tip Deep Child

:::

::::

:::::
```

MDX works inside, for example `<Tabs>`.

Outside Markdown use the component:

```jsx
import Admonition from '@theme/Admonition';

<Admonition type="tip" title="Did you know...">Text</Admonition>
```

`icon` accepts a JSX element or a string, and `title` is optional.

## Checked

2026-11-04. Read in full against the Docusaurus Admonitions page (markdown-features-admonitions.mdx): the five types, Prettier blank-line advice, title, CSS class and id syntax, nesting by colon count, MDX inside, and the Admonition component with icon and optional title match. Nothing removed.

Method: documentation only; no commands were run.
