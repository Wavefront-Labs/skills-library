---
id: computing-software.web-development.vitepress.sidebar-groups-multi-collapsed-base
name: sidebar-groups-multi-collapsed-base
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, sidebar, multiple-sidebars, collapsible-sidebar, sidebar-base, sidebaritem, path-prefix]
level: practitioner
status: docs-checked
description: "Build sidebars: groups, nesting to six levels, per-path multiple sidebars, collapsed groups, and base path prefixes."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-sidebar.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`themeConfig.sidebar` is an array of groups (`text` plus `items`) or an object keyed by path prefix.

```js
sidebar: [
  { text: 'Guide', items: [
    { text: 'Introduction', link: '/guide/' },     // trailing slash shows index.md
    { text: 'Getting Started', link: '/getting-started' }
  ]}
]
```

Items nest up to 6 levels from the root; deeper levels are ignored.

**Multiple sidebars** show different menus by URL prefix:

```js
sidebar: {
  '/guide/':  [{ text: 'Guide',  items: [{ text: 'Index', link: '/guide/' }, { text: 'One', link: '/guide/one' }] }],
  '/config/': [{ text: 'Config', items: [{ text: 'Index', link: '/config/' }] }]
}
```

**Collapsible groups.** `collapsed: false` (collapsible, open), `collapsed: true` (collapsible, closed initially); omitted means not collapsible.

**`base`** prefixes paths of immediate children to avoid repetition, in a multi-sidebar section or a nested group:

```js
sidebar: {
  '/guide/': { base: '/guide/', items: [{ text: 'Introduction', link: 'introduction' }] }
}
// nested group
{ text: 'Default Theme', base: '/reference/default-theme-', items: [{ text: 'Nav', link: 'nav' }] }
```

A nested `base` overrides the parent's prefix.

`SidebarItem` also has `docFooterText` (text in the prev/next footer), `rel` and `target`. Hide the sidebar for a page with frontmatter `sidebar: false`. The `useLayout()` composable (from `vitepress/theme`) exposes `sidebar`, `hasSidebar` and more for custom components.

Verify: navigating between `/guide/` and `/config/` swaps the menu.

## Checked

2026-11-08. Read the VitePress docs source pages default-theme-sidebar, default-theme-config (sidebar, useLayout) and frontmatter-config (sidebar). Confirmed array and object forms, the trailing-slash index rule, the 6-level nesting limit, multiple sidebars, collapsed semantics, base in multi-sidebar and nested groups with the override rule, SidebarItem extras, and useLayout. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
