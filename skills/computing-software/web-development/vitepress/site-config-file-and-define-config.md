---
id: computing-software.web-development.vitepress.site-config-file-and-define-config
name: site-config-file-and-define-config
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, site-config, defineconfig, config-file, config-ts, config-mts, intellisense]
level: practitioner
status: docs-checked
description: "Locate and write the VitePress config file, use defineConfig for typing, and know the supported extensions and ESM syntax."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/getting-started.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Resolution.** The config is always read from `<root>/.vitepress/config.[ext]` where ext is `.js`, `.ts`, `.mjs` or `.mts`. TypeScript works out of the box. Use ES module syntax and default-export an object:

```ts
import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'en-US',
  title: 'VitePress',
  description: 'Vite & Vue powered static site generator.',
  themeConfig: { /* theme-level options */ }
})
```

`defineConfig` exists only for TypeScript-powered IntelliSense; it works in JS and TS if your IDE supports it. Without it you still just export a plain object.

**Three kinds of option.** App-level options (title, base, srcDir, cleanUrls...) apply to every site regardless of theme; `themeConfig` is passed to whichever theme is active; and pass-through blocks configure the engines underneath:
- `vite`: raw Vite `UserConfig`, so you never need a separate Vite config file.
- `vue`: options for the bundled `@vitejs/plugin-vue`.
- `markdown`: the markdown-it instance and Shiki highlighter.

**Overrides.** Some settings can be overridden per page in frontmatter and per directory with a nested config file.

**Pitfalls.** VitePress is an ESM-only package: do not `require()` it, and either set `"type": "module"` in the nearest `package.json` or use the `.mjs`/`.mts` extension for files such as the config.

Verify: restarting dev after editing the config shows the new title in the browser tab.

## Checked

2026-11-08. Read the VitePress docs source pages site-config (overview sections) and getting-started (ESM note). Confirmed config resolution and extensions, defineConfig for IntelliSense, the vite, vue and markdown pass-through options (markdown-it and Shiki), and page and directory overrides. Replaced the config.mts pitfall with the documented ESM-only note.

Method: docs-only read of cited pages, 2026-11-08
