---
id: computing-software.web-development.docusaurus.code-line-highlighting
name: code-line-highlighting
category: computing-software
field: web-development
product: docusaurus
tags: [highlight-next-line, highlight-start, line-ranges, highlight-color, magic-comments]
level: practitioner
status: docs-checked
description: "Highlight lines in Docusaurus code blocks with highlight comments or a metastring range, supported comment styles, and the highlighted-line background variable."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-code-blocks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With comments (preferred, because you need not count lines):

````md
```js
function HighlightSomeText(highlight) {
  if (highlight) {
    // highlight-next-line
    return 'This text is highlighted!';
  }
  // highlight-start
  return 'Range';
  // highlight-end
}
```
````

Supported comment styles: C-style (`/* ... */`, `// ...`), JSX-style (`{/* ... */}`), Bash-style (`# ...`), HTML-style (`<!-- ... -->`). The style is inferred from the language, defaulting to all.

With a metastring (space after the language; commas and ranges, parsed by `parse-number-range`):

````md
```jsx {1,4-6,11}
````

Magic comments are only parsed if a highlight metastring is not present.

Highlight color in `src/css/custom.css`:

```css
:root {
  --docusaurus-highlighted-code-line-bg: rgb(72, 77, 91);
}
[data-theme='dark'] {
  --docusaurus-highlighted-code-line-bg: rgb(100, 100, 100);
}
```

That color suits the default Palenight theme; tweak it for other themes. Target the `theme-code-block-highlighted-line` class for other styling.

## Checked

2026-11-04. Read in full against the Docusaurus Code blocks page: highlight comments, supported comment styles table, metastring ranges with parse-number-range, magic comments ignored when a highlight metastring is present, --docusaurus-highlighted-code-line-bg values and the theme-code-block-highlighted-line class all match. Nothing removed.

Method: documentation only; no commands were run.
