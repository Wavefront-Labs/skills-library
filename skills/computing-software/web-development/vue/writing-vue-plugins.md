---
id: computing-software.web-development.vue.writing-vue-plugins
name: writing-vue-plugins
category: computing-software
field: web-development
product: vue
tags: [vue, vue-plugins, app-use, provide-inject, global-properties, injection-keys, web-development]
level: practitioner
status: verified
description: "Writing and installing Vue 3 plugins: install(app, options), providing services with typed injection keys, global components/directives and avoiding globalProperties sprawl."
sources:
  - https://vuejs.org/guide/reusability/plugins.html
  - https://vuejs.org/api/application.html
  - https://vuejs.org/guide/typescript/composition-api.html#typing-provide-inject
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing Vue plugins

**Goal:** package app-level setup (services, components, directives) in one installable unit with typed access.

## 1. Plugin shape
```ts
// plugins/i18n.ts
import { inject, ref, type App, type InjectionKey, type Ref } from "vue";

export interface I18n { t: (key: string) => string; locale: Ref<string> }
export const I18nKey: InjectionKey<I18n> = Symbol("i18n");

export function createI18n(options: { messages: Record<string, Record<string, string>>; locale: string }) {
  const locale = ref(options.locale);
  const i18n: I18n = { locale, t: (k) => options.messages[locale.value]?.[k] ?? k };
  return {
    install(app: App) {
      app.provide(I18nKey, i18n);
      app.directive("t", (el, b) => { el.textContent = i18n.t(b.value); });
    },
  };
}
export function useI18n() {
  const i = inject(I18nKey);
  if (!i) throw new Error("i18n plugin not installed");
  return i;
}
```
```ts
// main.ts
createApp(App).use(createI18n({ messages, locale: "en" })).mount("#app");
```
`install` can also be a plain function plugin: `app.use((app, opts) => {...}, opts)`.

## 2. What plugins typically register
- `app.provide` for services (prefer over globals; works with `inject` in composition API).
- `app.component` / `app.directive` for global components and directives (hurts tree-shaking - only for truly global ones).
- `app.config.errorHandler` / `warnHandler` for reporting.
- `app.config.globalProperties.$x` only for Options-API compatibility. Type it via module augmentation:
```ts
declare module "vue" { interface ComponentCustomProperties { $t: (k: string) => string } }
```

## 3. SSR
On the server every request creates a new app: plugins must create state per `install`/factory call, not at module level, or data leaks between users.

## 4. Order
Install router/pinia before plugins that depend on them; `app.use` ignores a plugin installed twice.

## Verify
- [ ] `useI18n()` outside an app with the plugin throws a clear error.
- [ ] Types: `inject(I18nKey)` is typed without casts.
- [ ] SSR: two concurrent requests don't share plugin state.
