---
id: computing-software.web-development.vite.config-devtools-tsconfig-future
name: config-devtools-tsconfig-future
category: computing-software
field: web-development
product: vite
tags: [vite-devtools, tsconfig-option, future-flags]
level: advanced
status: docs-checked
description: "Options devtools (experimental), tsconfig (discouraged override of per-file discovery) and future (opt in to upcoming breaking changes with warn)."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`devtools` (experimental): `boolean | DevToolsConfig`, default `false`. Install `@vitejs/devtools`, plus `@vitejs/devtools-vite` to inspect the dev server and `@vitejs/devtools-rolldown` for build analysis. It runs for both serve and build; limit with `apply`. Plugin `config` hooks cannot change it; set it in the user config.

```ts
export default defineConfig({
  devtools: { apply: 'serve' },
})
```

`tsconfig` (string): path to the tsconfig Vite uses, relative paths resolved from `root`. Unset by default, so Vite finds the closest matching `tsconfig.json` per file. Setting it is discouraged because it overrides that discovery. Prefer a nearby `tsconfig.json` with `references`; to remap imports prefer `resolve.alias` or `package.json` `imports`/`exports`.

`future` (`Record<string, 'warn' | undefined>`): enables future breaking changes ahead of the next major to ease migration. The list may change at any time; see the Breaking Changes page for options.

## Checked

Date: 2026-11-07. Read shared-options.md (read in full) (`devtools`, `tsconfig`, `future`). Package names, `apply: 'serve'`, the rule that plugin `config` hooks cannot change `devtools`, per-file tsconfig discovery, the discouragement of `tsconfig` and the `future` type all matched; nothing trimmed.

Method: documentation only; no commands were run.
