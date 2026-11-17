---
id: computing-software.web-development.nuxt.nuxt-config-file-basics
name: nuxt-config-file-basics
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, nuxt-config, define-nuxt-config, configuration, typescript]
level: intro
status: docs-checked
description: "Create and use nuxt.config.ts with defineNuxtConfig, and know which external config files Nuxt ignores in favour of config keys."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/03.configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt is configured with defaults for most use cases, and the `nuxt.config.ts` file at the project root can override or extend them. It exports `defineNuxtConfig({...})`, a helper that is globally available without import. You do not have to use TypeScript to build a Nuxt app, but the docs strongly recommend the `.ts` extension for this file so IDE hints help avoid typos and mistakes.

```ts
export default defineNuxtConfig({
  // My Nuxt config
})
```

Nuxt uses `nuxt.config.ts` as the single source of truth and skips reading external configuration files. Configure these through the matching key instead:

| Tool | Ignored file | Use this key |
|---|---|---|
| Nitro | nitro.config.ts | `nitro` |
| PostCSS | postcss.config.js | `postcss` |
| Vite | vite.config.ts | `vite` |
| webpack | webpack.config.ts | `webpack` |

Other tools keep their own files: `tsconfig.json`, `eslint.config.js`, `prettier.config.js`, `stylelint.config.js`, `tailwind.config.js`, `vitest.config.ts`. If you use Vite+, its `vite.config.ts` configures Vite+ commands such as `vp lint`, `vp fmt` and `vp test`; Nuxt does not read Vite options from it, so configure Vite for your app with the `vite` key in `nuxt.config`.

Every option is described in the Configuration Reference of the Nuxt docs.

## Checked

2026-11-04. Confirmed against the Nuxt configuration page: defineNuxtConfig global helper, .ts recommendation, single source of truth, the four ignored files and their keys, the list of other config files, the Vite+ note. Removed the cited reference-page file path (not read) and the Verify step.

Method: documentation only; no commands were run.
