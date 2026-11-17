---
id: computing-software.web-development.vitepress.frontmatter-default-theme-options
name: frontmatter-default-theme-options
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, frontmatter-config, layout, navbar, sidebar, aside, outline, pageclass, ishome, per-page-options]
level: practitioner
status: docs-checked
description: "Reference of default-theme frontmatter keys: layout, navbar, sidebar, aside, outline, lastUpdated, editLink, footer, pageClass, isHome."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/frontmatter-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Frontmatter overrides site/theme config for one page. Default-theme-only keys:

| Key | Type / default | Effect |
|---|---|---|
| `layout` | `doc` (default) / `home` / `page` | page layout; see layouts skill |
| `hero`, `features` | home page only | hero and feature sections |
| `navbar` | boolean, true | show the navbar |
| `sidebar` | boolean, true | show the sidebar |
| `aside` | `boolean \| 'left'`, true | `false` removes the aside container, `true` renders it right, `'left'` renders it left |
| `outline` | `number \| [number, number] \| 'deep' \| false`, 2 | heading levels in the outline; same as `themeConfig.outline.level` |
| `lastUpdated` | `boolean \| Date`, true | show last-updated text; a date shows that instead of the git timestamp |
| `editLink` | boolean, true | show the edit link |
| `footer` | boolean, true | show the footer |
| `pageClass` | string | extra CSS class for this page |
| `isHome` | boolean | force home-page elements in a custom layout |

Examples:

```yaml
---
outline: [2, 4]
aside: left
pageClass: custom-page-class
---
```

```css
/* .vitepress/theme/custom.css */
.custom-page-class { /* page-specific styles */ }
```

Common core keys also available: `title`, `titleTemplate`, `description`, `head` (merged with site `head`), `dir`.

`isHome` exists because the default theme decides "home" by `frontmatter.layout === 'home'`; set `isHome: true` when a custom layout should still show home elements.

## Checked

2026-11-04. Confirmed against the VitePress Frontmatter Config page (layout, hero, features, navbar, sidebar, aside, outline, lastUpdated, editLink, footer, pageClass, isHome with types and defaults; title, titleTemplate, description, head, dir). Removed: the Verify step.

Method: documentation only; no commands were run.
