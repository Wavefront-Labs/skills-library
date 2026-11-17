---
id: computing-software.web-development.vite.glob-import-options
name: glob-import-options
category: computing-software
field: web-development
product: vite
tags: [glob-import-option, glob-query-option, glob-base-option, glob-case-sensitive]
level: advanced
status: docs-checked
description: "import.meta.glob options: import for named or default exports, query for ?raw and ?url or custom queries, base path, and caseSensitive."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Options are the second argument of `import.meta.glob`.

`import` picks one export; with `eager` it enables tree-shaking. Use `'default'` for the default export:

```ts
import.meta.glob('./dir/*.js', { import: 'setup' })
import.meta.glob('./dir/*.js', { import: 'default', eager: true })
```

`query` appends a query to each import:

```ts
import.meta.glob('./dir/*.svg', { query: '?raw', import: 'default' })
import.meta.glob('./dir/*.svg', { query: '?url', import: 'default' })
import.meta.glob('./dir/*.js', { query: { foo: 'bar', bar: true } })
```

`base` sets a base directory, relative to the importer or absolute against the project root. Aliases and virtual modules are not supported. Only relative globs are interpreted against it, and result keys become relative to it:

```ts
import.meta.glob('./**/*.js', { base: './base' })
```

`caseSensitive: false` makes matching ignore case (default is case-sensitive).

## Checked

2026-11-07. Confirmed against the "Glob Import" subsections (Named Imports, Custom Queries, Base Path, Case Sensitive Matching) of guide/features.md (read in full, including the Dynamic Import, Glob Import, JSON, JSX, HTML and TypeScript sections): `import` with `eager` and tree-shaking, `'default'`, `query` string and object forms, `base` rules (relative to the importer or absolute against the project root, no aliases or virtual modules, only relative globs, keys relative to base) and `caseSensitive: false`. Nothing removed.

Method: documentation only; no commands were run.
