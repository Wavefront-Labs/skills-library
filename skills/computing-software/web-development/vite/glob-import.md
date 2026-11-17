---
id: computing-software.web-development.vite.glob-import
name: glob-import
category: computing-software
field: web-development
product: vite
tags: [import-meta-glob, glob-eager, glob-negative-patterns, glob-caveats]
level: practitioner
status: docs-checked
description: "Import many modules with import.meta.glob: lazy versus eager, multiple and negative patterns, and the literal-arguments and path rules."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`import.meta.glob` returns an object keyed by path. Matches are lazy dynamic imports, split into separate chunks at build:

```js
const modules = import.meta.glob('./dir/*.js')
for (const path in modules) {
  modules[path]().then((mod) => console.log(path, mod))
}
```

Eager (static imports, for side effects first):

```js
const modules = import.meta.glob('./dir/*.js', { eager: true })
```

Multiple patterns and exclusion with `!`:

```js
import.meta.glob(['./dir/*.js', './another/*.js'])
import.meta.glob(['./dir/*.js', '!**/bar.js'])
```

Caveats:
- Vite-only; not a web or ES standard.
- Patterns act like import specifiers: relative (`./`), absolute (`/`, from project root) or an alias path.
- Matching uses `tinyglobby`.
- All arguments must be passed as literals; no variables or expressions.

## Checked

2026-11-07. Confirmed against the "Glob Import" section of guide/features.md (read in full, including the Dynamic Import, Glob Import, JSON, JSX, HTML and TypeScript sections): lazy dynamic imports split into chunks, the iteration example, `{ eager: true }`, array and `!` negative patterns, and the caveats (Vite-only, specifier-like patterns including `/` from project root and alias paths, `tinyglobby`, literal arguments only). Nothing removed.

Method: documentation only; no commands were run.
