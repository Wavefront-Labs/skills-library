---
id: computing-software.ai-ml-engineering.mastra.simple-auth-and-jwt
name: simple-auth-and-jwt
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, auth, jwt, simpleauth, mastrajwtauth, bearer-token, mastraclient]
level: practitioner
status: docs-checked
description: "Protect a Mastra server with SimpleAuth (static token map) or MastraJwtAuth (shared-secret JWT) and send authenticated requests with curl or MastraClient."
sources:
  - https://mastra.ai/docs/auth/simple-auth
  - https://mastra.ai/docs/auth/jwt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn on token authentication for `server.auth` with the two lightweight built-in providers.

## SimpleAuth (dev, tests, static API keys)
Included in `@mastra/core/server`; no extra install.

```typescript
import { Mastra } from '@mastra/core'
import { SimpleAuth } from '@mastra/core/server'

type User = { id: string; name: string; role: 'admin' | 'user' }

export const mastra = new Mastra({
  server: {
    auth: new SimpleAuth<User>({
      tokens: {
        'sk-admin-token-123': { id: 'user-1', name: 'Admin User', role: 'admin' },
      },
    }),
  },
})
```

Options: `tokens` (required, token to user map), `headers` (extra headers to check, string or array), `name` (for logging), `authorizeUser(user, request)`, `protected` and `public` (arrays of RegExp or string paths).

Headers checked by default: `Authorization` (with or without `Bearer`) and `X-Playground-Access`.

Custom authorization: read the path with `getWebRequest(request)` from `@mastra/core/server`, e.g. return `user.role === 'admin'` when the path includes `/admin`. Load tokens from env vars (`process.env.ADMIN_API_KEY`) rather than hard-coding.

Limits stated by the docs: tokens live in memory, no expiry or refresh, no cryptographic verification, all tokens known at startup. For production use JWT, Clerk, Auth0 or another identity provider.

## MastraJwtAuth (shared secret)
```bash
npm install @mastra/auth@latest
```
```typescript
import { MastraJwtAuth } from '@mastra/auth'
new Mastra({ server: { auth: new MastraJwtAuth({ secret: process.env.MASTRA_JWT_SECRET }) } })
```
To create a dev token: on jwt.io choose JWT Encoder, enter your secret in Sign JWT: Secret, click Generate example, and store the result as `MASTRA_JWT_TOKEN` in `.env`. In Studio, Settings, Headers, Add Header: `Authorization` = `Bearer <your-jwt>`.

## Calling with credentials
```typescript
const client = new MastraClient({
  baseUrl: 'http://localhost:4111',
  headers: { Authorization: `Bearer ${process.env.MASTRA_JWT_TOKEN}` },
})
```
curl equivalent:
```bash
curl -X POST http://localhost:4111/api/agents/weatherAgent/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt>" \
  -d '{"messages": "Weather in London"}'
```

With SimpleAuth the `Bearer` prefix is optional; a bare token in `Authorization` also works. Extra header names go in `headers`, for example `['X-API-Key', 'X-Custom-Auth']`. The JWT page defers to a reference page for the full `MastraJwtAuth` options, which is not covered here.

## Checked
Confirmed 2026-11-08 against the Mastra Simple Auth and JSON Web Token docs pages (both fetched as markdown and read in full): usage, options table, default headers, custom authorization, env-var loading, limitations, install, JWT creation steps, Studio header and client usage. Added the optional `Bearer` prefix and `headers` example. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08
