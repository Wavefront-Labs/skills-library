---
id: computing-software.web-development.docusaurus.inline-svg-and-themed-images
name: inline-svg-and-themed-images
category: computing-software
field: web-development
product: docusaurus
tags: [inline-svg, themedimage, dark-mode-images, usebaseurl, svg-css]
level: practitioner
status: docs-checked
description: "Inline SVGs as components and restyle them per theme, switch images by light and dark mode with ThemedImage, or with GitHub-style path fragments and CSS."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-assets.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Inline SVGs work out of the box; import and render as a component:

```jsx
import DocusaurusSvg from './docusaurus.svg';

<DocusaurusSvg className="themedDocusaurus" />
```

This lets CSS alter parts of the SVG, for example per theme:

```css
[data-theme='light'] .themedDocusaurus [fill='#FFFF50'] {
  fill: greenyellow;
}
[data-theme='dark'] .themedDocusaurus [fill='#FFFF50'] {
  fill: seagreen;
}
```

SVG ids are prefixed to avoid clashes between inline SVGs, so target elements with attribute selectors or class names, not ids.

Themed images: `ThemedImage` switches source by current theme.

```jsx
import useBaseUrl from '@docusaurus/useBaseUrl';
import ThemedImage from '@theme/ThemedImage';

<ThemedImage
  alt="Docusaurus themed image"
  sources={{
    light: useBaseUrl('/img/docusaurus_light.svg'),
    dark: useBaseUrl('/img/docusaurus_dark.svg'),
  }}
/>
```

GitHub-style alternative: path fragments plus CSS. Use your own suffix if you do not want to be coupled to GitHub.

```css title="src/css/custom.css"
[data-theme='light'] img[src$='#gh-dark-mode-only'],
[data-theme='dark'] img[src$='#gh-light-mode-only'] {
  display: none;
}
```

```md
![alt](/img/light.svg#gh-light-mode-only)![alt](/img/dark.svg#gh-dark-mode-only)
```

## Checked

2026-11-04: read the Docusaurus Assets page in full. Confirmed inline SVG import and CSS, the SVG id prefix note, ThemedImage with useBaseUrl, and the GitHub-style fragment approach with its CSS. Nothing removed.

Method: documentation only; no commands were run.
