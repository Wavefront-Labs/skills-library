---
id: computing-software.web-development.nuxt.nuxt-component-directories-and-packages
name: nuxt-component-directories-and-packages
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, components, custom-directories, add-component, nuxt-module]
level: advanced
status: docs-checked
description: "Scan extra component directories with pathPrefix, prefix, pattern, extensions, and auto-import npm package components with addComponent."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.components.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default only `~/components` is scanned. Extend with an array in `nuxt.config`. Nested directories need to be added first because they are scanned in order; put the generic `~/components` last if you have overrides for its sub-directories.

```ts
export default defineNuxtConfig({
  components: [
    // ~/calendar-module/components/event/Update.vue => <EventUpdate />
    { path: '~/calendar-module/components' },
    // ~/user-module/components/account/UserDeleteDialog.vue => <UserDeleteDialog />
    { path: '~/user-module/components', pathPrefix: false },
    // ~/components/special-components/Btn.vue => <SpecialBtn />
    { path: '~/components/special-components', prefix: 'Special' },
    '~/components',
  ],
})
```

Entries also accept `pattern` and `ignore` globs that control which files are scanned within `path`, useful for nested domain folders:

```ts
{ path: '~/domains', pattern: '*/components/**', pathPrefix: false }
```

If `pattern` is specified, the `extensions` option has no effect, so make the pattern match the file extensions you want. To restrict extensions otherwise, use `{ path: '~/components', extensions: ['.vue'] }`; by default any file with an extension in the `extensions` key of `nuxt.config` is treated as a component.

npm packages: register them from a local module (for example `~/modules/register-component.ts`) with `addComponent` from `@nuxt/kit` inside `defineNuxtModule`'s `setup`:

```ts
addComponent({ name: 'MyAutoImportedComponent', export: 'MyComponent', filePath: 'my-npm-package' })
```

`<MyAutoImportedComponent />` is then auto-imported under the name you gave.

## Checked

2026-11-04. Confirmed against the Nuxt components directory page: custom directory array and its example comments, scan order note, pattern/ignore, pattern overriding extensions, extensions key, addComponent example. Removed: the Verify step about components.d.ts and the closing paragraph explaining order and prefix (not in the page).

Method: documentation only; no commands were run.
