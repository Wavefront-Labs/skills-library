---
id: computing-software.web-development.vitepress.distributing-and-consuming-custom-themes
name: distributing-and-consuming-custom-themes
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, theme-distribution, npm-theme, template-repository, theme-config-type, extends, consume-theme]
level: sme
status: docs-checked
description: "Package a theme for npm or a template repo, export ThemeConfig and a config sub-path, and consume or extend it in a site."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/custom-theme.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Distribute.** The easiest route is a GitHub **template repository**. For npm:

1. export the theme object as the default export of the package entry;
2. export the theme config type as `ThemeConfig` if applicable;
3. if the theme needs VitePress config changes, export that config from a sub path (e.g. `my-theme/config`) so users can extend it;
4. document the theme config options, both for the config file and for frontmatter;
5. give clear consumption instructions.

**Consume.**

```js
// .vitepress/theme/index.js
import Theme from 'awesome-vitepress-theme'
export default Theme
```

Extend it:

```js
import Theme from 'awesome-vitepress-theme'
export default {
  extends: Theme,
  enhanceApp(ctx) { /* ... */ }
}
```

If the theme needs special VitePress config, extend that too, with types:

```ts
// .vitepress/config.ts
import baseConfig from 'awesome-vitepress-theme/config'
import { defineConfig } from 'vitepress'
import type { ThemeConfig } from 'awesome-vitepress-theme'

export default defineConfig<ThemeConfig>({
  extends: baseConfig,
  themeConfig: { /* Type is ThemeConfig */ }
})
```

For themes with a non-default config type, `defineConfigWithTheme<ThemeConfig>` is the typed helper. `extends` on a Theme calls the base theme's `enhanceApp` and `setup` before yours; `extends` in config pulls in the base config.

## Checked

2026-11-04. Confirmed against the VitePress custom-theme guide (Distributing a Custom Theme, Consuming a Custom Theme, Theme Interface extends) and the site-config page (defineConfigWithTheme). Removed: the invented 'Mistakes' paragraph, the word 'merges' for config extends, and the Verify step.

Method: documentation only; no commands were run.
