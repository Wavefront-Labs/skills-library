---
id: computing-software.web-development.docusaurus.static-assets
name: static-assets
category: computing-software
field: web-development
product: docusaurus
tags: [static-folder, static-directories, usebaseurl, baseurl, asset-references]
level: practitioner
status: docs-checked
description: "Handle Docusaurus static assets: the static folder, staticDirectories, referencing assets from JSX, Markdown and CSS without hardcoding baseUrl, and caveats."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/static-assets.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Files in `static` are copied to the root of `build`, hierarchy preserved. With `baseUrl: '/subpath/'`, `static/img/docusaurus.png` is served at `/subpath/img/docusaurus.png`. Add more source folders:

```js title="docusaurus.config.js"
staticDirectories: ['public', 'static'],
```

JSX: a hardcoded `src="/img/x.png"` breaks when `baseUrl` changes. Use any of these, which prepend `baseUrl`:

```jsx
import Url from '@site/static/img/docusaurus.png';
<img src={Url} />;
<img src={require('@site/static/img/docusaurus.png')} />;
<img src={new URL('@site/static/img/docusaurus.png', import.meta.url).href} />;

import useBaseUrl from '@docusaurus/useBaseUrl';
<img src={useBaseUrl('/img/docusaurus.png')} />;
```

Imported SVG files become React components.

Markdown: absolute paths in Markdown syntax (`[Download](/files/note.docx)`) are converted to `require` calls. JSX `<a>` and `<img>` tags are not processed.

CSS: use absolute paths in `url()`, for example `url('/font/Caroline.otf')`; the bundler loads the asset.

Rule of thumb: never hardcode the base URL. Pretend the base is `/test/` in JSX (so use `require`) and `/` in Markdown or CSS.

Caveats: files in `static` are not post-processed, hashed or minified unless converted to `require`. Missing files behind hard-coded absolute paths are not caught at compile time and return 404. On GitHub Pages add an empty `.nojekyll` to `static`.

## Checked

2026-11-04. Read in full against the Docusaurus Static Assets page (static-assets.mdx): static folder copy and baseUrl example, staticDirectories, the JSX options, SVG components, Markdown and CSS handling, the rule of thumb and the three caveats (including .nojekyll) all match. Nothing removed.

Method: documentation only; no commands were run.
