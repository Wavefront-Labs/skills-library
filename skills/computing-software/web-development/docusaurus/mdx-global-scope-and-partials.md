---
id: computing-software.web-development.docusaurus.mdx-global-scope-and-partials
name: mdx-global-scope-and-partials
category: computing-software
field: web-development
product: docusaurus
tags: [mdxcomponents, global-scope, partials, mdxcontent, import-raw-code]
level: advanced
status: docs-checked
description: "Register MDX components globally by wrapping @theme/MDXComponents, import Markdown partials and raw code files, and read frontMatter, toc and contentTitle."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-react.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global scope: `@theme/MDXComponents` is a record from tag names to React components. To add a tag usable without imports, create a wrapper manually (the swizzle CLI cannot wrap non-component files yet):

```js title="src/theme/MDXComponents.js"
import MDXComponents from '@theme-original/MDXComponents';
import Highlight from '@site/src/components/Highlight';

export default {
  ...MDXComponents,
  Highlight,
};
```

Use upper-case tag names: MDX always renders lower-case tags as native HTML.

Importing Markdown inside a React page needs the provider, otherwise the global scope is missing:

```jsx
import MDXContent from '@theme/MDXContent';

<MDXContent><FeatureDisplay /></MDXContent>
```

Partials: an MDX file default-exports a component (capitalised import name). A `_` filename prefix creates no page, so it is a partial. Props are available as `props`:

```jsx
import PartialExample from './_markdown-partial-example.mdx';

<PartialExample name="Sebastien" />
```

Import code as raw text with import attributes (experimental), rendered by `CodeBlock` since triple backticks ship content as-is:

```jsx
import CodeBlock from '@theme/CodeBlock';
import MyComponentSource from './myComponent.js' with {type: 'text'};

<CodeBlock language="jsx">{MyComponentSource}</CodeBlock>
```

Globals in an MDX page: `frontMatter`, `toc` (tree of headings) and `contentTitle` (first h1, or `undefined`).

## Checked

2026-11-04: read the Docusaurus MDX and React page in full. Confirmed the MDXComponents wrapper, upper-case tag rule, MDXContent provider, partials with the underscore prefix, raw code import with CodeBlock (added the missing CodeBlock import line), and the frontMatter, toc and contentTitle globals. Nothing else removed.

Method: documentation only; no commands were run.
