---
id: computing-software.web-development.nuxt.nuxt-title-template-and-tag-position
name: nuxt-title-template-and-tag-position
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, title-template, template-params, tag-position, usehead]
level: practitioner
status: docs-checked
description: "Build page titles with titleTemplate strings or functions, templateParams placeholders, tagPosition for body scripts, and route-meta head tags."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/08.seo-meta.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dynamic titles use `titleTemplate`. As a string, `%s` is replaced by the page title: `useHead({ titleTemplate: '%s - Site Title' })`. As a function you get full control and can return a fallback when a page has no title:

```ts
useHead({
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} - Site Title` : 'Site Title'
  },
})
```

A function cannot be set in `nuxt.config`; put it in `app.vue` so it applies to every page. A page that calls `useHead({ title: 'My Page' })` then renders "My Page - Site Title". You can also pass `null` to fall back to the plain site title.

`templateParams` adds placeholders beyond `%s`:

```ts
useHead({
  titleTemplate: (t) => t ? `${t} %separator %siteName` : '%siteName',
  templateParams: { siteName: 'Site Title', separator: '-' },
})
```

Body placement: scripts and other applicable tags accept `tagPosition: 'head' | 'bodyClose' | 'bodyOpen'`; use `bodyClose` for third-party scripts that should load at the end of the body.

Route-driven tags: `definePageMeta({ title: 'Some Page' })` is extracted at build time by a macro, so it cannot be dynamic; read it in a layout through `useRoute().meta.title` and feed `useHead({ meta: [{ property: 'og:title', content: `App Name - ${route.meta.title}` }] })`.

External CSS such as Google Fonts is added with `link` entries (preconnect then stylesheet) or the `<Link>` component.

Verify: navigate between pages and confirm the browser tab title follows the template.

## Checked

2026-11-08. Read the Nuxt SEO and Meta doc in full. Confirmed titleTemplate string and function forms, the nuxt.config restriction, templateParams, tagPosition values, definePageMeta with useRoute().meta, and the external CSS example. Nothing removed.

Method: documentation only; no commands were run.
