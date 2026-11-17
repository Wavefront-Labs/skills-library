---
id: computing-software.web-development.vite.resolve-alias-dedupe
name: resolve-alias-dedupe
category: computing-software
field: web-development
product: vite
tags: [resolve-alias, alias-array-format, resolve-dedupe, alias-absolute-paths]
level: practitioner
status: docs-checked
description: "Configure resolve.alias in object or array form with absolute paths and regex replacements, SSR alias caveats, and resolve.dedupe for duplicate dependencies."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`resolve.alias` replaces values in `import` / `require`, like `@rollup/plugin-alias`. Earlier entries apply first. When aliasing to file system paths use absolute paths; relative values are used as-is and not resolved.

```js
resolve: {
  alias: {
    utils: '../../../utils',
    'batman-1.0.0': './joker-1.5.0',
  },
}
```

Array form for complex pairs; with a RegExp `find`, `replacement` may use patterns such as `$1`:

```js
resolve: {
  alias: [
    { find: 'utils', replacement: '../../../utils' },
    { find: /^(.*)\.js$/, replacement: '$1.alias' },
  ],
}
```

Using with SSR: if you alias SSR externalized dependencies, alias the actual `node_modules` packages instead (Yarn and pnpm support the `npm:` prefix).

`resolve.dedupe` (`string[]`): force listed dependencies to always resolve to one copy from the project root, for duplicates caused by hoisting or linked monorepo packages. In SSR builds it does not work for ESM outputs configured from `build.rolldownOptions.output`; the workaround is CJS output.

## Checked

2026-11-07. Re-read the Shared Options page (docs/config/shared-options.md) in full. Confirmed resolve.alias behaviour (like @rollup/plugin-alias, first rules first, absolute paths, relative values used as-is), the object and array formats with the RegExp replacement pattern, the SSR externalized dependencies warning with the npm: prefix, and resolve.dedupe including the SSR plus ESM warning and CJS workaround. Nothing removed.

Method: documentation only; no commands were run.
