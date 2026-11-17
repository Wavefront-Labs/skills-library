---
id: computing-software.web-development.vite.json-imports
name: json-imports
category: computing-software
field: web-development
product: vite
tags: [json-import, json-named-exports, json-tree-shaking]
level: intro
status: docs-checked
description: "Import JSON files directly in Vite, either as one object or as named root-field exports that help tree-shaking."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
JSON files import directly, and named imports are supported.

```js
// import the entire object
import json from './example.json'
// import a root field as named exports - helps with tree-shaking!
import { field } from './example.json'
```

Prefer named imports of root fields when you only need part of a large JSON file, so unused fields can be tree-shaken from the build.

## Checked

2026-11-07. Confirmed against the "JSON" section of guide/features.md (read in full, including the Dynamic Import, Glob Import, JSON, JSX, HTML and TypeScript sections): direct and named imports and the tree-shaking comment. Nothing removed.

Method: documentation only; no commands were run.
