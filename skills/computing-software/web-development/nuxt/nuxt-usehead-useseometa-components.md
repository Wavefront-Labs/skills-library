---
id: computing-software.web-development.nuxt.nuxt-usehead-useseometa-components
name: nuxt-usehead-useseometa-components
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, usehead, useseometa, head-components, seo]
level: practitioner
status: docs-checked
description: "Three ways to manage head tags in Nuxt: useHead, type-safe useSeoMeta, and capitalised head components, plus reactivity and dedupe rules."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/08.seo-meta.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/2.composables/use-seo-meta.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt offers three APIs for head tags.

`useHead` supports reactive input and covers everything:

```ts
useHead({
  title: 'My App',
  meta: [{ name: 'description', content: 'My amazing site.' }],
  bodyAttrs: { class: 'test' },
  script: [{ innerHTML: 'console.log(\'Hello world\')' }],
})
```

`useSeoMeta` takes a flat, fully typed object, which prevents common mistakes such as `name` instead of `property` for Open Graph tags:

```ts
useSeoMeta({
  title: 'My Amazing Site',
  ogTitle: 'My Amazing Site',
  description: 'This is my amazing site.',
  ogImage: 'https://example.com/image.png',
  twitterCard: 'summary_large_image',
})
```

Components exist for template-based authors: `<Title>`, `<Base>`, `<NoScript>`, `<Style>`, `<Meta>`, `<Link>`, `<Body>`, `<Html>`, `<Head>`. The capitalisation avoids clashing with native tags. Wrap them in `<Head>` or `<Html>` so tags dedupe more intuitively; nested tags inside `<Head>`/`<Body>` do not change where they render. Add a `key` attribute on `<Head>` if tags must be duplicated across client/server boundaries.

Reactivity works on every property: pass a ref, a computed, a getter or a reactive object (for example `{ name: 'description', content: description }` where `description` is a ref).

The docs recommend `useHead` in all cases; components are a personal preference. The docs also point to the `useHeadSafe` composable.

Verify: change the ref value and watch the meta tag update in DevTools Elements.

## Checked

2026-11-08. Read the Nuxt SEO and Meta doc and the useSeoMeta API doc in full. Confirmed useHead, useSeoMeta, the head components, dedupe and key advice, reactivity and the recommendation of useHead. Removed the claim that the three APIs are equivalent and the 'untrusted input' reason for useHeadSafe, which the docs do not state.

Method: documentation only; no commands were run.
