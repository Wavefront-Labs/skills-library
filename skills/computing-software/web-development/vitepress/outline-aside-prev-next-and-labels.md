---
id: computing-software.web-development.vitepress.outline-aside-prev-next-and-labels
name: outline-aside-prev-next-and-labels
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, outline, aside, prev-next-links, docfooter, themeconfig-labels, externallinkicon, returntotoplabel]
level: practitioner
status: docs-checked
description: "Tune the right-hand outline and aside, prev/next link text, and translated UI labels like sidebarMenuLabel and skipToContentLabel."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-config.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-prev-next-links.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/frontmatter-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Outline.** `themeConfig.outline` is `false`, a level, or `{ level, label }`. `level` is a number (that heading level only), `[min, max]`, or `'deep'` (= `[2, 6]`); default `2`. `label` defaults to `On this page`. Per page: frontmatter `outline: [2, 4]`.

**Aside.** `aside: true` right (default), `'left'`, or `false` (no aside container). To hide the outline everywhere use `outline: false`, not aside. In RTL layouts both sides mirror.

**Prev/next links.** Text and links are inferred from the sidebar. Override per page:

```yaml
---
prev: 'Get Started | Markdown'
next:
  text: 'Markdown'
  link: '/guide/markdown'
---
```

`prev: false` hides the link. `themeConfig.docFooter = { prev: 'Pagina prior', next: 'Proxima pagina' }` translates the labels above the links, or `false` values disable them globally.

**Interface labels (all strings)**, useful for non-English sites and accessibility: `darkModeSwitchLabel` (default `Appearance`, mobile only), `lightModeSwitchTitle`, `darkModeSwitchTitle`, `sidebarMenuLabel` (`Menu`), `returnToTopLabel` (`Return to top`), `langMenuLabel` (`Change language`), `navMenuLabel` (`Main Navigation`), `mobileMenuLabel` (`Menu`), `extraMenuLabel` (`More options`), `skipToContentLabel` (`Skip to content`).

**Other flags:** `externalLinkIcon` (default false) shows an icon on external links in Markdown; `i18nRouting` (boolean or function) controls whether switching locale rewrites the URL, with a function for custom mappings.

Verify: rebuild and confirm the changed text appears in the page.

## Checked

2026-11-08. Read the VitePress docs source pages default-theme-config, default-theme-prev-next-links and frontmatter-config. Confirmed outline level and label defaults, aside values and the outline: false advice, prev/next frontmatter forms, docFooter, the label options with their defaults, externalLinkIcon and i18nRouting. Added frontmatter-config as a source for the per-page outline override. Removed the claim that labels show up as aria attributes.

Method: docs-only read of cited pages, 2026-11-08
