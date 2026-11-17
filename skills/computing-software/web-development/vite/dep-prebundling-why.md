---
id: computing-software.web-development.vite.dep-prebundling-why
name: dep-prebundling-why
category: computing-software
field: web-development
product: vite
tags: [pre-bundling-purpose, commonjs-to-esm, lodash-es-requests, dev-only-prebundle]
level: practitioner
status: docs-checked
description: "Why Vite pre-bundles dependencies: CommonJS/UMD to ESM conversion with smart named-import analysis, and collapsing many-module packages like lodash-es."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/dep-pre-bundling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On first `vite` run, dependencies are pre-bundled automatically and transparently. Two purposes:

1. CommonJS and UMD compatibility. Dev serves native ESM, so CJS/UMD dependencies must become ESM. Vite does smart import analysis so named imports from CJS modules work even when exports are assigned dynamically (React):

```js
// works as expected
import React, { useState } from 'react'
```

2. Performance. ESM packages with many internal modules are merged into one. `lodash-es` has over 600 internal modules, so `import { debounce } from 'lodash-es'` would fire 600+ HTTP requests at once and congest the browser; pre-bundled it is one request.

Pre-bundling applies in development only, and is done with Rolldown, so it is typically very fast.

## Checked

Date: 2026-11-07. Read dep-pre-bundling.md in full (The Why, the development-only note, discovery section for the Rolldown mention). The two purposes, the React named-import example and the `lodash-es` figures (over 600 internal modules, 600+ requests) matched; nothing trimmed.

Method: documentation only; no commands were run.
