---
id: computing-software.web-development.vite.backend-render-tags
name: backend-render-tags
category: computing-software
field: web-development
product: vite
tags: [render-manifest-tags, imported-chunks, chunk-import-map-backend, modulepreload-links]
level: advanced
status: docs-checked
description: "Render production tags from the manifest in a backend: CSS links, recursive imports, the entry script, optional modulepreload, an importedChunks sketch, and import maps."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/backend-integration.md
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Given a manifest and an entry, emit in this recommended order:
1. A `<link rel="stylesheet">` for each file in the entry chunk's `css` list.
2. Recursively follow the entry's `imports`, and add a stylesheet link for each imported chunk's `css`.
3. A tag for the entry's `file`: `<script type="module">` for JS, `<link rel="stylesheet">` for CSS.
4. Optionally `<link rel="modulepreload">` for each imported JS chunk's `file`, again recursing.

Example for `views/foo.js` in the docs' sample manifest:

```html
<link rel="stylesheet" href="assets/foo-5UjPuW-k.css" />
<link rel="stylesheet" href="assets/shared-ChJ_j-JJ.css" />
<script type="module" src="assets/foo-BRBmoGS9.js"></script>
<link rel="modulepreload" href="assets/shared-B7PI925R.js" />
```

`importedChunks(manifest, name)` is illustrative, not provided by Vite: walk `chunk.imports`, track a `seen` set, push nested imports first then the importee.

Chunk import maps: if the experimental `build.chunkImportMap` option (default `false`) is on, the map is written to `importmap.json` in the output directory. Inject its `<script type="importmap">` before any `<script type="module">` or `<link rel="modulepreload">` tag.

## Checked

Date: 2026-11-07. Read backend-integration.md in full, including step 4 (the four recommended tag steps, the views/foo.js example tags, the collapsed importedChunks pseudo implementation) and the chunk import map info box. Added that `build.chunkImportMap` is experimental with default false, confirmed in build-options.md (read in full). No claims removed.

Method: documentation only; no commands were run.
