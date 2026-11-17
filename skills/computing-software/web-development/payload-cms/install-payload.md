---
id: computing-software.web-development.payload-cms.install-payload
name: install-payload
category: computing-software
field: web-development
product: payload-cms
tags: [install, create-payload-app, nextjs, requirements]
level: intro
status: docs-checked
description: "Scaffold a new Payload app with create-payload-app or add Payload packages and a database adapter to an existing Next.js app."
sources:
  - https://payloadcms.com/docs/getting-started/installation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install Payload

Goal: get a working Payload app, new or inside an existing Next.js project.

Requirements listed in the docs: a JS package manager (pnpm preferred, yarn 1.x unsupported), Node.js 24.22.1+, Next.js 16.4.0+, TypeScript 6.0.3+, and a database (MongoDB, Postgres or SQLite).

New app:

```bash
npx create-payload-app@beta
```

Existing Next.js app (App Router; the Admin Panel can also run on TanStack Start via `@payloadcms/tanstack-start`):

```bash
pnpm i payload @payloadcms/next
pnpm i @payloadcms/richtext-lexical sharp graphql   # optional
pnpm i @payloadcms/db-mongodb   # or db-postgres, db-sqlite (install one)
```

- `@payloadcms/richtext-lexical` is only needed for rich text fields.
- `sharp` is only needed for upload collections with image manipulation.
- `graphql` is only needed if you use the GraphQL API.
- With npm you may need `npm i --legacy-peer-deps`.

Then copy the Payload files from the Blank Template's `(payload)` folder into `app/(payload)` and wrap your Next config with `withPayload` from `@payloadcms/next/withPayload` (the config must be ESM: `"type": "module"` or an `.mjs` file). Create `payload.config.ts` with at least `secret`, `db` and `collections` (plus `editor` for rich text), and add a `@payload-config` path in `tsconfig`.

Gotcha: not every Next.js 16 release is compatible; stay inside the supported range from the docs.

Run the dev script and open `http://localhost:3000/admin` to create the first user.

## Checked

2026-11-04. Read getting-started/installation in the payloadcms/payload docs. Confirmed: requirements and versions, create-payload-app, package list, optional packages, legacy peer deps note, TanStack Start alternative, supported-version warning. Added: withPayload, ESM requirement, tsconfig alias, minimal config.
Method: documentation only; no commands were run.
