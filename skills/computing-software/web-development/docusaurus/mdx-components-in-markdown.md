---
id: computing-software.web-development.docusaurus.mdx-components-in-markdown
name: mdx-components-in-markdown
category: computing-software
field: web-development
product: docusaurus
tags: [mdx, jsx-in-markdown, export-component, import-component, site-alias]
level: practitioner
status: docs-checked
description: "Use React components inside Docusaurus Markdown: exporting inline, importing with the @site alias, JSX style objects, and the MDX strictness that breaks CommonMark habits."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-react.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Docusaurus supports MDX (v3), so JSX works in Markdown. If you get compilation errors, check your syntax in the MDX playground.

Define a component in an MDX file by exporting it; only paragraphs starting with `export` are parsed as components.

```jsx
export const Highlight = ({children, color}) => (
  <span style={{backgroundColor: color, color: '#fff'}}>{children}</span>
);

<Highlight color="#25c2a0">Docusaurus green</Highlight>
```

Anything that looks like HTML is JSX, so use style objects: `<span style={{backgroundColor: 'red'}}>`, not `style="..."`.

Import your own or npm components. Prefer the `@site` alias (your site directory) over relative paths; it survives moving files, versioning and translating.

```md
import Highlight from '@site/src/components/Highlight';
```

For complex logic, use a separate `.js` file.

MDX is stricter than CommonMark. Notably:

- indented code blocks do not work: use triple backticks
- autolinks `<http://localhost:3000>` do not work: use regular links
- HTML syntax like `<p style="color: red;">` does not work: use JSX
- unescaped `{` and `<` must be escaped as `\{` and `\<`

Prettier supports only legacy MDX v1; add `{/* prettier-ignore */}` before problem areas, or `*.mdx` to `.prettierignore`.

Experimental CommonMark opt-in: `mdx.format: md` front matter, or `.md` extension with `markdown.format: "detect"`.

## Checked

2026-11-04: read the Docusaurus MDX and React page in full. Confirmed MDX v3, exporting components, JSX style objects, importing with the @site alias, the CommonMark differences, Prettier note and the experimental CommonMark opt-in. Nothing removed.

Method: documentation only; no commands were run.
