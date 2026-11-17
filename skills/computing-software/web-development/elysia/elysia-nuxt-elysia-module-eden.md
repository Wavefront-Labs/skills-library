---
id: computing-software.web-development.elysia.elysia-nuxt-elysia-module-eden
name: elysia-nuxt-elysia-module-eden
category: computing-software
field: web-development
product: elysia
tags: [integrations-frameworks, nuxt, eden, nitro, community-plugin]
level: practitioner
status: docs-checked
description: "Run Elysia on Nuxt API routes with the community nuxt-elysia module, Nitro Bun preset, and an auto-configured Eden Treaty client."
sources:
  - https://elysiajs.com/integrations/nuxt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve Elysia from Nuxt and call it type-safely.

1. Install:

```bash
bun add elysia @elysia/eden
bun add -d nuxt-elysia
```

2. Register the module and switch Nitro to Bun in the Nuxt config (`defineNuxtConfig`):

```ts
export default defineNuxtConfig({
    modules: ['nuxt-elysia'],
    nitro: { preset: 'Bun' }
})
```

The docs say `nitro.preset: 'Bun'` is required because Elysia runs on the Bun runtime rather than Node.js.

3. Create `api.ts` in the project root, exporting a function that returns an Elysia instance:

```typescript
export default () => new Elysia()
    .get('/hello', () => ({ message: 'Hello world!' }))
```

4. Call it with the injected Eden Treaty client `$api`:

```vue
<script setup lang="ts">
const { $api } = useNuxtApp()
const { data } = await useAsyncData(async () => {
    const { data, error } = await $api.hello.get()
    if (error) throw new Error('Failed to call API')
    return data
})
</script>
```

5. Mount path: Elysia is mounted on `/_api` by default; change it with `nuxtElysia: { path: '/api' }` in the Nuxt config.

pnpm: `pnpm add @sinclair/typebox openapi-types`.

Gotchas:
- `nuxt-elysia` is a community plugin (tkesgar/nuxt-elysia); the docs point to its repository for more configuration options.
- The `api.ts` sample omits the `import { Elysia } from 'elysia'` line; add it.

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/nuxt.html); each claim, option name and default was compared with the page text. Removed the invented Verify step and the unsupported maintainer claim.

Method: documentation only; no commands were run.
