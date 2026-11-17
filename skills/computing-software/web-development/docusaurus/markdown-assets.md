---
id: computing-software.web-development.docusaurus.markdown-assets
name: markdown-assets
category: computing-software
field: web-development
product: docusaurus
tags: [assets, images, require, new-url, pathname-protocol]
level: practitioner
status: docs-checked
description: "Reference co-located images and files from Docusaurus Markdown by Markdown syntax, require, import or new URL, absolute static paths, and the pathname:// escape."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-assets.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Co-locate assets next to the doc, for example `docs/assets/banner.png`. Four ways to show an image:

```md
![Example banner](./assets/banner.png)
```

```jsx
<img src={require('./assets/banner.png')} alt="Example banner" />

import myImageUrl from './assets/banner.png';
<img src={myImageUrl} alt="Example banner" />

<img src={new URL('./assets/banner.png', import.meta.url).href} alt="Example banner" />
```

`new URL()` relative to `import.meta.url` is portable (browsers, Node.js, other bundlers) and always returns the asset URL even when a plugin like ideal-image or SVGR transforms imports. With `@docusaurus/plugin-ideal-image`, use its dedicated image component instead.

Files work the same: use `require` (or `new URL`) in `video` and `a` tags, or Markdown link syntax:

```md
[Download this docx](./assets/example.docx)
```

With Markdown image or link syntax, paths are resolved as file paths and converted to `require()` automatically. In JSX you must do it yourself.

Absolute paths such as `![alt](/img/docusaurus.png)` are resolved from the configured static directories (for example `['public', 'static']`, looked up in both). They become `require()` calls, so base URL is handled and the file enters the build pipeline with a hash in its name for aggressive caching.

To keep a plain URL with no processing or existence check, use `pathname://`:

```md
![banner](pathname:///img/banner.png)
```

## Checked

2026-11-04. Read in full against the Docusaurus Assets page (markdown-features-assets.mdx): the four image methods, new URL portability, ideal-image note, files via require and Markdown syntax, automatic require conversion, absolute paths resolved from static directories, hash in the file name, and pathname:// all match. Nothing removed.

Method: documentation only; no commands were run.
