---
id: computing-software.web-development.vitepress.migrating-from-vuepress-and-vitepress-0x
name: migrating-from-vuepress-and-vitepress-0x
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, migration, vuepress, vitepress-0x, breaking-changes, sidebar-items, editlink, home-layout, withbase]
level: intro
status: docs-checked
description: "Migrate from VuePress or VitePress 0.x: sidebar items key, removed repo options, edit link, lastUpdated split, home layout, and image base handling."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/migration-from-vuepress.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/migration-from-vitepress-0.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**From VuePress** (the guide is marked "more to follow"):
- The sidebar is no longer auto-populated from frontmatter. Read frontmatter yourself to build it dynamically.
- Static images handle `base` automatically, so `<img :src="$withBase('/foo.png')" alt="foo">` becomes `![foo](/foo.png)`. Dynamic images still need `withBase`. A find regex from the guide: `<img.*withBase\('(.*)'\).*alt="([^"]*)".*>` replace with `![$2]($1)`.

**From VitePress 0.x**

App config: the guide states internationalization is not yet implemented.

Theme config:
- `sidebar` structure changed: `children` is now `items`; top-level items cannot have a `link` for now.
- `repo`, `repoLabel`, `docsDir`, `docsBranch`, `editLinks`, `editLinkText` are removed. Use Social Links for the GitHub icon in the navbar and the Edit Link feature for "Edit this page".
- `lastUpdated` is split into the site-level `lastUpdated` and `themeConfig.lastUpdated.text`.
- `carbonAds.carbon` is now `carbonAds.code`.

Frontmatter:
- `home: true` is now `layout: home`, and many home-page settings changed (hero and features; see the home page skill).
- `footer` moved to `themeConfig.footer`.

Checklist derived from the lists above: rename sidebar keys, delete removed options, move footer, convert home pages, then run the build.

Verify: `vitepress build` completes and the home page renders its hero.

## Checked

Read both migration guides in full. Confirmed the sidebar change (`children` to `items`, no top-level `link`), the removed repo options, the `lastUpdated` split, `carbonAds.code`, `home: true` to `layout: home`, the `footer` move, and the image `withBase` regex and replacement. Removed the claim about fixing dead links from build output, which the guides do not state.

Method: docs-only read of cited pages, 2026-11-08
