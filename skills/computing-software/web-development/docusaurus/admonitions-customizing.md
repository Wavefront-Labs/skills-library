---
id: computing-software.web-development.docusaurus.admonitions-customizing
name: admonitions-customizing
category: computing-software
field: web-development
product: docusaurus
tags: [custom-admonition, admonition-keywords, extenddefaults, admonition-types, swizzle-wrapper]
level: advanced
status: docs-checked
description: "Customize admonition rendering with a wrapper and add custom admonition types by registering keywords and mapping them to React components."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-admonitions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two kinds of customization exist: rendering and parsing.

Rendering: swizzle by wrapping. Example swapping the icon for `info` only:

```jsx title="src/theme/Admonition.js"
import Admonition from '@theme-original/Admonition';
import MyCustomNoteIcon from '@site/static/img/info.svg';

export default function AdmonitionWrapper(props) {
  if (props.type !== 'info') {
    return <Admonition title="My Custom Admonition Title" {...props} />;
  }
  return <Admonition icon={<MyCustomNoteIcon />} {...props} />;
}
```

Parsing: admonitions are a Remark plugin; pass options per content plugin (docs, blog, pages) through the `admonitions` key.

```js title="docusaurus.config.js"
docs: {
  admonitions: {
    keywords: ['my-custom-admonition'],
    extendDefaults: true,
  },
},
```

`keywords` lists allowed types; `extendDefaults` (default `true`) merges them into the defaults. The keyword becomes the `type` prop of `Admonition`.

The theme does not know how to render a custom keyword, so map it to a component. This file is not swizzlable:

```js title="src/theme/Admonition/Types.js"
import DefaultAdmonitionTypes from '@theme-original/Admonition/Types';

const AdmonitionTypes = {
  ...DefaultAdmonitionTypes,
  'my-custom-admonition': MyCustomAdmonition,
};
export default AdmonitionTypes;
```

Then use `:::my-custom-admonition[My Title]`.

## Checked

2026-11-04. Read in full against the Docusaurus Admonitions page, Customizing admonitions section: rendering wrapper example, admonitions options per content plugin (keywords, extendDefaults default true), keyword passed as type, and the non-swizzlable Admonition/Types.js mapping match. Nothing removed.

Method: documentation only; no commands were run.
