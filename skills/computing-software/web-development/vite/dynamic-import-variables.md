---
id: computing-software.web-development.vite.dynamic-import-variables
name: dynamic-import-variables
category: computing-software
field: web-development
product: vite
tags: [dynamic-import-vars, import-variable-rules, one-level-deep]
level: practitioner
status: docs-checked
description: "Dynamic imports with variables in Vite: the three bundling rules (start with ./, end with extension, filename pattern) and the one-directory-level limit."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vite supports dynamic import with variables:

```ts
const module = await import(`./dir/${file}.js`)
```

Variables represent file names only one level deep. If `file` is `'foo/bar'` the import fails; use glob import for deeper cases.

To be bundled, the import must:
- start with `./`, `../` or `#`: `` import(`./dir/${foo}.js`) `` is valid, `` import(`${foo}.js`) `` is not;
- end with a file extension: `` `./dir/${foo}.js` `` is valid, `` `./dir/${foo}` `` is not;
- specify a file name pattern for imports into its own directory: `` `./prefix-${foo}.js` `` is valid, `` `./${foo}.js` `` is not.

These rules prevent accidentally bundling unintended files; without them `import(foo)` would bundle everything on the file system.

## Checked

2026-11-07. Confirmed against the "Dynamic Import" section of guide/features.md (read in full, including the Dynamic Import, Glob Import, JSON, JSX, HTML and TypeScript sections): the sample import, the one-level-deep limit with the `foo/bar` failure, the three rules (start with `./`, `../` or `#`; end with a file extension; file name pattern for own-directory imports) with their valid and invalid examples, and the `import(foo)` rationale. Nothing removed.

Method: documentation only; no commands were run.
