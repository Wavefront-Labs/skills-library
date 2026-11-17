---
id: computing-software.web-development.vitepress.nav-bar-links-dropdowns-and-components
name: nav-bar-links-dropdowns-and-components
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, nav, navbar, nav-links, dropdown-menu, activematch, sitetitle, logo, social-links, custom-nav-component]
level: practitioner
status: docs-checked
description: "Configure the navbar: title and logo, links, nested dropdowns, activeMatch regex strings, target/rel, and custom components."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-nav.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Title and logo.** `themeConfig.siteTitle` replaces the displayed title (`false` hides it); `logo` takes a path under `public` or an object for alt text and dark/light variants:

```js
themeConfig: { logo: '/my-logo.svg', siteTitle: false }
```

**Links.**

```js
nav: [
  { text: 'Guide', link: '/guide' },
  { text: 'Changelog', link: 'https://github.com/...' },
  {
    text: 'Dropdown Menu',
    items: [
      { text: 'Item A', link: '/item-1' },
      { text: 'Section A Title', items: [{ text: 'Sub item', link: '...' }] }
    ]
  }
]
```

`link` is a path to the file without `.md`, starting with `/`, or a function `(pageData) => path`. A dropdown title cannot have a `link` (it becomes the button). Sections may omit their title.

**Active state.** `activeMatch` is a regex **string** (not a RegExp, which is not serializable at build time): `{ text: 'Guide', link: '/guide', activeMatch: '/config/' }`.

**Target/rel.** Auto-detected from external vs internal; override with `target: '_self', rel: 'sponsored'`.

**Social links** are in `themeConfig.socialLinks`: `{ icon: 'github', link }` (any simple-icons name), `'lucide:rss'` style iconify names if the collection is installed, or `{ svg: '<svg>...' }` with an `ariaLabel`.

**Custom components.** `{ component: 'MyCustomComponent', props: { title: '...' } }`, registered globally in `enhanceApp`. They receive `screenMenu` (inside the mobile menu) and `menu` (inside a dropdown/`...` panel) booleans; render a flat list in those cases.

Verify: resize to mobile width and check the same items in the hamburger menu.

## Checked

2026-11-08. Read the VitePress docs source pages default-theme-nav and default-theme-config (logo, siteTitle, nav, socialLinks). Confirmed siteTitle and logo behaviour, link forms, dropdown sections, activeMatch as a regex string, target and rel handling, social link forms, and the custom component props screenMenu and menu. Removed the description of what noIcon does, which the pages do not give.

Method: docs-only read of cited pages, 2026-11-08
