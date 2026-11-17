---
id: computing-software.web-development.nuxt.nuxt-config-environment-overrides
name: nuxt-config-environment-overrides
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, nuxt-config, c12, env-name, per-environment]
level: practitioner
status: docs-checked
description: "Use $production, $development and $env keys in nuxt.config for typed per-environment overrides and select one with the nuxt build --envName flag."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/03.configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nuxt.config` supports fully typed per-environment overrides with the `$production`, `$development` and `$env` keys.

```ts
export default defineNuxtConfig({
  $production: {
    routeRules: {
      '/**': { isr: true },
    },
  },
  $development: {
    //
  },
  $env: {
    staging: {
      //
    },
  },
})
```

- `$env.<name>` defines a custom environment such as `staging`. To select an environment when running a Nuxt CLI command, pass its name to the `--envName` flag, for example `nuxt build --envName staging`.
- For the mechanism behind the overrides, see the `c12` documentation section "environment-specific configuration".
- If you are authoring layers, the `$meta` key provides metadata that you or the consumers of your layer might use.

## Checked

2026-11-04. Confirmed against the Nuxt configuration page: $production, $development and $env keys, the isr route-rule example, --envName with the nuxt build staging example, the c12 pointer and the $meta note for layers. Removed: claims about when $production/$development apply, the troubleshooting paragraph, the typical-use paragraph and the Verify step (none in the page).

Method: documentation only; no commands were run.
