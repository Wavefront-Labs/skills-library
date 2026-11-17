---
id: computing-software.web-development.vite.deploy-cloudflare-workers
name: deploy-cloudflare-workers
category: computing-software
field: web-development
product: vite
tags: [cloudflare-vite-plugin, cloudflare-workers, wrangler-deploy]
level: practitioner
status: docs-checked
description: "Add the Cloudflare Vite plugin to run server code in the Workers runtime during dev via the Environment API, then deploy the build with wrangler."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/static-deploy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Cloudflare Vite plugin integrates with Cloudflare Workers and uses Vite's Environment API to run server-side code in the Workers runtime during development.

```bash
npm install --save-dev @cloudflare/vite-plugin
```

```js
import { cloudflare } from '@cloudflare/vite-plugin'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [cloudflare()],
})
```

Add a Wrangler config:

```jsonc
{
  "name": "my-vite-app",
}
```

After `npm run build`, deploy with `npx wrangler deploy`.

You can add backend APIs to the Vite app to communicate with Cloudflare resources; they run in the Workers runtime in dev and deploy alongside the frontend.

## Checked

Date: 2026-11-07. Read static-deploy.md in full (Cloudflare Workers subsection: plugin package, `cloudflare()` config, wrangler config, `npx wrangler deploy`, backend APIs note). All matched; nothing trimmed.

Method: documentation only; no commands were run.
