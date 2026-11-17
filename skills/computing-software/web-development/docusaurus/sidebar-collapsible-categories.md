---
id: computing-software.web-development.docusaurus.sidebar-collapsible-categories
name: sidebar-collapsible-categories
category: computing-software
field: web-development
product: docusaurus
tags: [collapsible, collapsed, sidebar-collapsible, sidebar-collapsed, precedence]
level: practitioner
status: docs-checked
description: "Control whether sidebar categories collapse and start collapsed, per category or globally, and which setting wins when collapsible and collapsed conflict."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/docs/sidebar/items.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Categories are collapsible by default and start collapsed. Per category in `sidebars.js`:

```js title="sidebars.js"
{
  type: 'category',
  label: 'Docs',
  collapsible: false, // cannot be collapsed
  collapsed: false,   // starts expanded
  items: ['introduction'],
}
```

Global defaults are options of `@docusaurus/plugin-content-docs`:

```js title="docusaurus.config.js"
presets: [
  ['@docusaurus/preset-classic', {
    docs: {
      sidebarCollapsible: false,
      sidebarCollapsed: false,
    },
  }],
],
```

Precedence:

- Options in `sidebars.js` win over plugin configuration, so individual categories can be collapsible even if `sidebarCollapsible` is `false` globally. The same holds for `collapsed` versus `sidebarCollapsed`.
- If a category has `collapsed: true` but `collapsible: false` (from either place), the latter wins and the category renders expanded.

## Checked

2026-11-04. Read in full against the Docusaurus Sidebar items page: collapsible and collapsed defaults, sidebarCollapsible and sidebarCollapsed in the docs plugin options, sidebars.js precedence and the collapsed true with collapsible false warning all match. Nothing removed.

Method: documentation only; no commands were run.
