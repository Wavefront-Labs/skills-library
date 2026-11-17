---
id: computing-software.web-development.nuxt.nuxt-shared-directory
name: nuxt-shared-directory
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, shared, auto-import, utils, types]
level: practitioner
status: docs-checked
description: "Share utilities and types between the Vue app and Nitro server through shared/utils and shared/types, with import limits."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.shared.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `shared/` directory (Nuxt v3.14 and later) holds code usable by both the Vue app and the Nitro server. Code in it cannot import any Vue or Nitro code.

Why: Nuxt builds two separate bundles (the Vue app for client and SSR, and the Nitro server) that are bundled independently and run in different contexts. Components and composables need the Vue runtime and often the Nuxt context (`useNuxtApp()`, `useRoute()`), which does not exist in Nitro; importing them into server code can cause build or runtime errors and pull Vue app dependencies into the server bundle. Server-only code (Node APIs, Nitro utilities, route handlers) must not run in the browser; importing it into the app can break the client build, cause browser runtime errors or leak server logic into the client bundle. `import type` is erased at compile time, so type-only crossings may appear to work, but keep shared types in `shared/types/` for clarity.

Usage:

```ts
// shared/utils/capitalize.ts
export const capitalize = (input: string) => input[0] ? input[0].toUpperCase() + input.slice(1) : ''
```

A default export also works. It is then auto-imported in both `app/app.vue` and `server/api/hello.get.ts`.

Scanning: only files directly in `shared/utils/` and `shared/types/` are auto-imported. Nested subdirectories are not, unless you add them to `imports.dirs` and `nitro.imports.dirs`. The scanning is identical to `app/composables/` and `app/utils/`. Other files in `shared/` must be imported with the `#shared` alias, for example `import lower from '#shared/formatters/lower'`.

Types used in one context only can live in `app/types/` (auto-imported in the Vue app only) or `server/types/` (Nitro server only); use `shared/types/` when a type is needed in both.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/2.directory-structure/1.shared.md. Confirmed: all claims above. Changed: the old "leak secrets" wording became the page's "leak server logic"; added nitro.imports.dirs and the #shared alias, both on the page. Removed the invented Verify step.

Method: documentation only; no commands were run.
