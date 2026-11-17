---
id: computing-software.web-development.nuxt.nuxt-composables-utils-auto-import-scanning
name: nuxt-composables-utils-auto-import-scanning
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, composables, utils, auto-import, imports-dirs]
level: practitioner
status: docs-checked
description: "How Nuxt scans app/composables and app/utils for auto-imports, named vs default exports, nested folders and generated types."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.composables.md
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/1.utils.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The two directories are scanned identically. Export named or default:

```ts
// app/composables/useFoo.ts
export const useFoo = () => useState('foo', () => 'bar')
// default export: use-foo.ts or useFoo.ts -> available as useFoo() (camelCase of the filename without extension)
export default function () { return useState('foo', () => 'bar') }
```

Auto-imported functions work in `.js`, `.ts` and `.vue` files.

Rules:
- `app/composables/` adds no reactivity itself; reactivity comes from Vue's Composition API (`ref`, `reactive`) and is not limited to that directory.
- `app/utils/` exists for a semantic distinction between composables and other auto-imported utility functions (for example `formatNumber`). These utils are only available in the Vue part of the app; in `server/` only `server/utils` is auto-imported.
- Only files at the top level of the directory are scanned (for example `index.ts` and `useFoo.ts`, not `nested/utils.ts`). For nested folders either re-export from `app/composables/index.ts` (recommended) or configure the scanner with `imports.dirs`:

```ts
export default defineNuxtConfig({
  imports: { dirs: ['~/composables', '~/composables/*/index.{ts,js,mjs,mts}', '~/composables/**'] },
})
```

- Types are auto-generated into `.nuxt/imports.d.ts`; run `nuxt prepare`, `nuxt dev` or `nuxt build` to generate them. A composable created without the dev server running makes TypeScript throw an error such as `Cannot find name 'useBar'.`
- Composables can call other composables via auto-imports, and can read plugin injections, for example `useNuxtApp().$hello`.
- Types can be auto-imported the same way: app-only types go in `app/types/`, server-only types in `server/types/`, shared types in `shared/types/`.

## Checked

2026-11-04. Confirmed against the Nuxt composables and utils directory pages: export styles and camelCase naming, reactivity note, utils purpose and Vue-only scope, top-level scanning with re-export or imports.dirs, imports.d.ts and the nuxt prepare/dev/build requirement and error text, nested composables, plugin injections, types directories. Corrected: subfolder index files are not scanned (only the top level is). Removed the Verify step.

Method: documentation only; no commands were run.
