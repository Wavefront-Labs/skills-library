---
id: computing-software.web-development.vue.vue-i18n-internationalisation
name: vue-i18n-internationalisation
category: computing-software
field: web-development
product: vue
tags: [vue-i18n, vue-internationalization, nuxt-i18n, pluralization, lazy-loading-locales, vue]
level: practitioner
status: gated
description: "Vue i18n with vue-i18n: Composition API setup, plurals, number/date formats, lazy locales, precompiled messages for CSP, i18n-t for markup, and Nuxt i18n."
sources:
  - https://vue-i18n.intlify.dev/guide/
  - https://vue-i18n.intlify.dev/guide/advanced/lazy
  - https://i18n.nuxtjs.org/docs/getting-started
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vue-i18n internationalisation

## 1. Setup (Composition API mode)
```ts
import { createI18n } from "vue-i18n";
import en from "./locales/en.json";
export const i18n = createI18n({
  legacy: false, locale: "en", fallbackLocale: "en", messages: { en },
  numberFormats: { en: { currency: { style: "currency", currency: "GBP" } } },
  datetimeFormats: { en: { short: { year: "numeric", month: "short", day: "numeric" } } },
});
app.use(i18n);
```
```vue
<script setup lang="ts">
import { useI18n } from "vue-i18n";
const { t, n, d, locale } = useI18n();
</script>
<template>
  <h1>{{ t("greeting", { name: user.name }) }}</h1>
  <p>{{ t("inbox", { count: unread }, unread) }}</p>
  <p>{{ n(total, "currency") }} - {{ d(order.date, "short") }}</p>
</template>
```
```json
{ "greeting": "Hello {name}", "inbox": "No messages | One message | {count} messages" }
```
Pipe-separated plural forms cover English; for languages with more plural categories supply `pluralRules` per locale. ICU MessageFormat syntax is not supported: `{count, plural, one {...} other {...}}` fails with "Invalid token in placeholder" (vue-i18n 11.4.2).

## 2. Markup inside translations
Use the `<i18n-t>` component with slots instead of `v-html`:
```vue
<i18n-t keypath="terms" tag="p"><template #link><a href="/terms">{{ t("termsLink") }}</a></template></i18n-t>
```

## 3. Lazy-load locales
```ts
export async function setLocale(l: string) {
  if (!i18n.global.availableLocales.includes(l)) {
    const messages = await import(`./locales/${l}.json`);
    i18n.global.setLocaleMessage(l, messages.default);
  }
  i18n.global.locale.value = l;
  document.documentElement.lang = l;
}
```

## 4. Build: precompile messages
`@intlify/unplugin-vue-i18n` precompiles locale messages, so production builds bundle the runtime-only vue-i18n module (smaller bundle, no runtime compilation). Before v9.3 the compiling build used eval and broke under a strict CSP; from v9.3 JIT compilation avoids that and from v10 it is the default (vue-i18n optimization guide). `<i18n>` custom blocks in SFCs: unconfirmed (gated: unconfirmed, source is paywalled or blocked).

## 5. Nuxt
`@nuxtjs/i18n` configures Vue I18n v11 inside Nuxt (install with `npx nuxi@latest module add @nuxtjs/i18n`, configure under `i18n` in `nuxt.config`). Its routing strategies, `useLocalePath()`, `useLocaleHead()` and lazy locale files are documented at i18n.nuxtjs.org; confirm option names there (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Switching locale updates text, numbers, dates and `<html lang>`; production build has no runtime compiler and passes a strict CSP.
