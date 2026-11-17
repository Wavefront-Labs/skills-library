---
id: computing-software.web-development.astro.sessions-configure-drivers
name: sessions-configure-drivers
category: computing-software
field: web-development
product: astro
tags: [sessions, session-driver, unstorage, redis, session-false]
level: advanced
status: docs-checked
description: "Configure server-side sessions in Astro: adapter default drivers, sessionDrivers.lruCache, a runtime-configured Redis entrypoint, and disabling sessions."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/sessions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sessions share data between requests for on-demand rendered pages. Unlike cookies, data is stored on the server, so size and security limits are less of a concern, and it works without client JavaScript. A storage driver is required. The Node, Cloudflare and Netlify adapters configure a default; other adapters need one set manually:

```js title="astro.config.mjs"
import { defineConfig, sessionDrivers } from 'astro/config'
import vercel from '@astrojs/vercel'

export default defineConfig({
  adapter: vercel(),
  session: {
    driver: sessionDrivers.lruCache({
      max: 800,
    }),
  }
})
```

Drivers are configured at build time and environment variables are inlined, so runtime override is impossible. For that, put the driver in its own file and use it as the `entrypoint`. The docs example uses `unstorage` and `ioredis`:

```ts title="src/session-driver.ts"
import type { SessionDriver } from "astro";
import redisDriver from "unstorage/drivers/redis";
import { REDIS_HOST, REDIS_PORT } from "astro:env/server";

export default function (): SessionDriver {
  const driver = redisDriver({ host: REDIS_HOST, port: REDIS_PORT });

  return {
    async getItem(key) { return await driver.getItem(key); },
    async setItem(key, value) { await driver.setItem?.(key, value, {}); },
    async removeItem(key) { await driver.removeItem?.(key, {}); },
  };
}
```

```js
session: {
  driver: {
    entrypoint: new URL("./src/session-driver.ts", import.meta.url),
  },
},
```

Opt out entirely (adapters then supply no default driver, which can reduce cold starts): `session: false`.

## Checked

2026-11-04. Confirmed against the Astro sessions guide: server-side storage, default drivers for the Node, Cloudflare and Netlify adapters, sessionDrivers.lruCache, build-time inlining of env vars, driver entrypoint with unstorage and ioredis, session false. Nothing removed.

Method: documentation only; no commands were run.
