---
id: computing-software.web-development.vite.css-options-modules-postcss
name: css-options-modules-postcss
category: computing-software
field: web-development
product: vite
tags: [css-modules-option, css-postcss-option, scoped-name, postcss-load-config]
level: advanced
status: docs-checked
description: "Configure css.modules (postcss-modules options such as localsConvention, generateScopedName) and css.postcss inline config or search directory."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`css.modules` passes options to postcss-modules:

```ts
interface CSSModulesOptions {
  getJSON?: (cssFileName: string, json: Record<string, string>, outputFileName: string) => void
  scopeBehaviour?: 'global' | 'local'
  globalModulePaths?: RegExp[]
  exportGlobals?: boolean
  generateScopedName?: string | ((name: string, filename: string, css: string) => string)
  hashPrefix?: string
  localsConvention?: 'camelCase' | 'camelCaseOnly' | 'dashes' | 'dashesOnly' | ((originalClassName: string, generatedClassName: string, inputFile: string) => string)
}
```

`localsConvention` defaults to `undefined`. The option has no effect with Lightning CSS; use `css.lightningcss.cssModules` instead.

`css.postcss`: a string (a directory to search for PostCSS config, default the project root) or an inline config (`postcss.ProcessOptions` plus `plugins`). Inline `plugins` must be array format. Search uses `postcss-load-config` and only supported file names. Config files outside the workspace root (or project root if no workspace) are not searched by default; give a custom path to load one. An inline config stops Vite searching other sources.

## Checked

Date: 2026-11-07. Read shared-options.md (read in full) (`css.modules`, `css.postcss`). The CSSModulesOptions fields, `localsConvention` default `undefined`, the Lightning CSS caveat, string-or-inline `css.postcss`, array-only `plugins`, the search/workspace-root rules and the inline-config rule matched; nothing trimmed.

Method: documentation only; no commands were run.
