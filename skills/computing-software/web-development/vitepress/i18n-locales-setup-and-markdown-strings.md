---
id: computing-software.web-development.vitepress.i18n-locales-setup-and-markdown-strings
name: i18n-locales-setup-and-markdown-strings
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, i18n, locales, localespecificconfig, locale-label, translations-menu, markdown-labels, codecopybutton]
level: practitioner
status: docs-checked
description: "Set up multilingual sites with the locales option, per-locale overrides, and translated container, alert and copy-button labels."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/i18n.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create one directory per extra language beside the root content:

```
docs/
├─ es/foo.md
├─ fr/foo.md
├─ foo.md
```

Then declare locales in the config:

```ts
export default defineConfig({
  locales: {
    root: { label: 'English', lang: 'en' },
    fr: {
      label: 'French',
      lang: 'fr',          // becomes the lang attribute on the html tag
      link: '/fr/guide'    // default /fr/; shown in the navbar translations menu, may be external
    }
  }
})
```

Properties overridable per locale (root included): `lang`, `dir`, `title`, `titleTemplate`, `description`, `head` (merged with existing entries, duplicate meta tags removed) and `themeConfig` (shallow merged, so shared values stay in the top-level themeConfig). See the `DefaultTheme.Config` type for the placeholder texts you can translate. Do not override `themeConfig.algolia` or `themeConfig.carbonAds` at locale level; use the Algolia i18n options for multilingual search.

Tip: the config may live at `docs/.vitepress/config/index.ts`, so you can keep one file per locale and merge them in `index.ts`.

**Per-locale Markdown strings.** Text baked in by the Markdown renderer, namely default container titles, GitHub-style alert titles and the code copy button strings, is overridden via a `markdown` key inside the locale entry (`container.tipLabel`, `warningLabel`, ..., `codeCopyButton.tooltipText`, `copiedText`). Unset values fall back to the root `markdown` options. A locale can retitle only containers registered at the root; it cannot register new ones. Because one renderer serves the whole site, these must be declared in the main config file, not in additional configs.

Verify: the language menu appears in the navbar and a container title shows the translated word.

## Checked

2026-11-08. Read the VitePress docs source page guide/i18n. Confirmed the directory layout, the locales example with label, lang and link, the LocaleSpecificConfig properties and their merge rules, the algolia and carbonAds warning, the config/index.ts tip, and the per-locale markdown key with its fallback, root-container and main-config-only limits. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
