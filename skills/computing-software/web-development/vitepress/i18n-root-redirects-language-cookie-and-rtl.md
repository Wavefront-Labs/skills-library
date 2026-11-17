---
id: computing-software.web-development.vitepress.i18n-root-redirects-language-cookie-and-rtl
name: i18n-root-redirects-language-cookie-and-rtl
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, i18n-redirects, language-cookie, nf-lang, rtl, dir-rtl, logical-properties, netlify-redirects]
level: advanced
status: docs-checked
description: "Redirect / to a language directory, persist a language cookie, and support right-to-left locales with dir and logical CSS."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/i18n.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**No root locale.** A layout with `en/`, `es/` and `fr/` directories and no root content is valid, but VitePress does not redirect `/` to `/en/`; configure the host. On Netlify put this in `docs/public/_redirects`:

```
/*  /es/:splat  302  Language=es
/*  /fr/:splat  302  Language=fr
/*  /en/:splat  302
```

**Persist the choice.** The guide uses an `nf_lang` cookie to remember the user's language with the redirects above. Extend the default theme with a wrapper layout that writes the cookie whenever the language changes:

```vue
<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { useData, inBrowser } from 'vitepress'
import { watchEffect } from 'vue'
const { lang } = useData()
watchEffect(() => {
  if (inBrowser) {
    document.cookie = `nf_lang=${lang.value}; expires=Mon, 1 Jan 2030 00:00:00 UTC; path=/`
  }
})
</script>
<template><DefaultTheme.Layout /></template>
```

Register it in `theme/index.ts` with `{ extends: DefaultTheme, Layout }`.

**RTL.** Set `dir: 'rtl'` (with the matching `lang`, e.g. `fa-IR`) in the config; for a multilingual site set it per locale, or per page with the `dir` frontmatter option. The default theme uses CSS logical properties, so layout, navigation and directional icons mirror themselves. No PostCSS RTL plugin is needed; leaving an RTLCSS plugin in place would flip the already-mirrored styles a second time, so remove it. Code blocks always stay left to right.

In your own CSS prefer `margin-inline-start` over `margin-left`, and mirror custom directional icons:

```css
[dir='rtl'] .my-arrow-icon { scale: -1 1; }
```

Verify: load an RTL page and confirm the sidebar sits on the right.

## Checked

2026-11-08. Read the VitePress docs source page guide/i18n (separate directory per locale and RTL sections). Confirmed the no-redirect statement, the Netlify _redirects example, the nf_lang cookie layout code, RTL setup with dir, logical properties, the RTLCSS warning, code blocks staying left to right, and the CSS mirroring snippet. Reworded the claim that Netlify honours the cookie, which the page does not state.

Method: docs-only read of cited pages, 2026-11-08
