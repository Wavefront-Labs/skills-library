---
id: computing-software.web-development.vitepress.directory-level-config-overrides
name: directory-level-config-overrides
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, directory-config, defineadditionalconfig, config-overrides, per-directory, locale-config]
level: advanced
status: docs-checked
description: "Override description, lang, head and similar settings per directory with a nested config.ts, merged down the tree."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some site settings can be overridden for every page in a directory without repeating frontmatter on each page.

**How.** Add a file named `config.ts` (or `.js`, `.mjs`, `.mts`) inside the directory, and default-export a config object. Nested directories inherit from their parent directory, and overrides are merged in order.

The helper `defineAdditionalConfig` gives TypeScript IntelliSense for the options allowed here (its use is optional, like `defineConfig`):

```ts
// es/config.ts
import { defineAdditionalConfig } from 'vitepress'

export default defineAdditionalConfig({
  description: 'Generador de Sitios Estáticos desarrollado con Vite y Vue.'
})
```

Every page under `es/` now uses that description.

**Which options.** The site-config reference marks these as overridable at the directory level: `title`, `titleTemplate`, `description`, `lang`, `dir`, and appending to `head`.

**Compare with `locales`.** With the built-in i18n features you can instead override a locale directory's settings through `locales` in the main config. Note the markdown renderer is created once for the whole site, so locale `markdown` strings must be declared in the main config, not in additional configs.

**Precedence (documented for `head`).** Head entries from site config, locale config, directory-level config, frontmatter and `transformHead` are merged in that order; a later entry replaces an earlier one with the same key.

## Checked

2026-11-04. Confirmed against the VitePress site-config page (Directory-Level Overrides, per-option 'can be overridden at the directory level' notes, head merge order) and the i18n guide (locales, markdown renderer created once). Removed: the claim that other options are global only, the claim that directory config is an alternative that keeps settings near content, a general precedence ordering (the page documents it only for head), and the Verify step.

Method: documentation only; no commands were run.
