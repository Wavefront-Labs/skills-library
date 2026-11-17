---
id: computing-software.web-development.payload-cms.environment-variables
name: environment-variables
category: computing-software
field: web-development
product: payload-cms
tags: [environment-variables, dotenv, next-public, client-bundle]
level: intro
status: docs-checked
description: "Use .env files with Payload, expose variables to client components safely with NEXT_PUBLIC_ or VITE_ prefixes, and load dotenv outside Next.js."
sources:
  - https://payloadcms.com/docs/configuration/environment-vars
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Environment variables

Goal: load secrets and expose only safe values to the Admin Panel client bundle.

Next.js: create a `.env` in the project root and read from `process.env` in the config:

```bash
SERVER_URL=localhost:3000
DATABASE_URL=mongodb://localhost:27017/my-database
```

```ts
export default buildConfig({ serverURL: process.env.SERVER_URL })
```

The Admin Panel client bundle does not include environment variables by default. For a Custom Component running in the browser:

- Next.js: prefix with `NEXT_PUBLIC_` and read `process.env.NEXT_PUBLIC_X`.
- TanStack Start (Vite): prefix with `VITE_` and read `import.meta.env.VITE_X`.

Only expose keys that are safe to publish in plain text (for example a Stripe publishable key, never the secret key).

Outside Next.js, use `dotenv` and import it as high as possible so it runs before the config is evaluated:

```ts
import dotenv from 'dotenv'
dotenv.config()
```

By default dotenv reads `.env` in the working directory; pass a path to use a different file.

## Checked

2026-11-04. Read configuration/environment-vars in the payloadcms/payload docs. Confirmed: .env usage, NEXT_PUBLIC_ and VITE_ prefixes, dotenv outside Next.js, only expose publishable values. Removed: the console.log verify step (not on the page).
Method: documentation only; no commands were run.
