---
id: computing-software.web-development.nuxt.nuxt-error-page-and-createerror
name: nuxt-error-page-and-createerror
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, error-vue, createerror, clearerror, useerror]
level: practitioner
status: docs-checked
description: "Customise the full-screen error page with error.vue, throw errors with createError, and clear them with clearError and useError."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/12.error-handling.md
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.app/3.error.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When Nuxt encounters a fatal error (any unhandled error on the server, or an error created with `fatal: true` on the client) it triggers a full-screen error page. An error thrown in a server route or server middleware returns a JSON response instead. Customize the page by adding `error.vue` in the source directory, alongside `app.vue`:

```vue
<script setup lang="ts">
import type { NuxtError } from '#app'
const props = defineProps({ error: Object as () => NuxtError })
const handleError = () => clearError({ redirect: '/' })
</script>
<template>
  <div>
    <h2>{{ error?.status }}</h2>
    <button @click="handleError">Clear errors</button>
  </div>
</template>
```

`error.vue` is not a route: do not put it in `~/pages` and do not use `definePageMeta` in it, though you can use layouts via `<NuxtLayout>` with a layout name. Its single prop `error` has the fields `status`, `fatal`, `unhandled`, `statusText?`, `data?` and `cause?`. When rendered on the server in production it only receives the `message` and `data` of an error created with `createError`; custom fields are lost, so assign them to `data`. Other errors (such as a failed `$fetch`) are marked `unhandled` and reach the page with their status and a generic message.

Utilities:
- `useError()` returns the global Nuxt error being handled (typed as `Ref<Error | { url, status, statusText, message, description, data }>`).
- `createError(string | { cause, data, message, name, stack, status, statusText, fatal })`, meant to be thrown, usable in the Vue and server portions of the app. Thrown on the server it triggers the full-screen error page, which you can clear with `clearError`; thrown on the client it is a non-fatal error unless `fatal: true`.
- `clearError({ redirect })` clears the handled error and optionally redirects to a path, for example a safe page.

```ts
const { data } = await useFetch(`/api/movies/${route.params.slug}`)
if (!data.value) {
  throw createError({ status: 404, statusText: 'Page Not Found' })
}
```

`statusText` is for short, HTTP-compliant status texts containing only horizontal tabs, spaces and visible ASCII characters; use `message` for detailed, multi-line or non-ASCII text. In development an error `cause` is preserved and exposed to your error page; in production causes are never included in error responses or the error page payload.

Rendering the error page is an entirely separate page load, so registered middleware runs again; use `useError` in middleware to check. If you are on Node 16, cookies set while rendering the error page overwrite previously set cookies (Node 16 reached end-of-life in September 2023, per the docs).

## Checked

2026-11-04. Confirmed against the Nuxt error handling page and the error.vue page: fatal error behaviour, error.vue example and constraints, NuxtError fields, production message/data rule, useError/createError/clearError signatures and behaviour, statusText rule, cause handling, middleware and Node 16 notes. Removed the Verify step.

Method: documentation only; no commands were run.
