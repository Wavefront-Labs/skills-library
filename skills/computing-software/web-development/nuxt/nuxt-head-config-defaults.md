---
id: computing-software.web-development.nuxt.nuxt-head-config-defaults
name: nuxt-head-config-defaults
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, head, unhead, app-head, seo]
level: practitioner
status: docs-checked
description: "Set static head tags in nuxt.config app.head, override the default charset and viewport, and handle favicon URLs when app.cdnURL is set."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/08.seo-meta.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt head tag management is powered by Unhead. Providing an `app.head` property in `nuxt.config.ts` statically customizes the head for your entire app:

```ts
export default defineNuxtConfig({
  app: {
    head: {
      title: 'Nuxt', // default fallback title
      htmlAttrs: { lang: 'en' },
      link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    },
  },
})
```

This method does not allow reactive data; the docs recommend `useHead()` in `app.vue` for that. It is good practice to set tags here that won't change, such as your default site title, language and favicon.

Default tags provided by Nuxt: `viewport` (`width=device-width, initial-scale=1`) and `charset` (`utf-8`). Update them with the keyed shortcuts inside `app.head`, for example `charset: 'utf-16'` or `viewport: 'width=device-width, initial-scale=1, maximum-scale=1'`.

CDN note: when you set `app.cdnURL`, assets in `public/` (including `favicon.ico`) are served from that CDN, and Nuxt resolves public assets against `cdnURL`, falling back to `app.baseURL`. A static `app.head` link such as `href: '/favicon.ico'` is a literal path and is not resolved against `cdnURL`. The docs build the href from runtime config with `useHead()` in `app.vue`: `const { cdnURL, baseURL } = useRuntimeConfig().app`, then `href: `${cdnURL || baseURL}favicon.ico``.

The head object accepts these keys (the docs' `MetaObject` type): `title`, `titleTemplate`, `templateParams`, `base`, `link`, `meta`, `style`, `script`, `noscript`, `htmlAttrs`, `bodyAttrs`.

## Checked

2026-11-04. Confirmed against the Nuxt SEO and Meta page: Unhead, app.head example, the non-reactive warning and best-practice note, default viewport and charset with override example, the cdnURL note and useHead workaround, the MetaObject keys. Removed the Verify step.

Method: documentation only; no commands were run.
