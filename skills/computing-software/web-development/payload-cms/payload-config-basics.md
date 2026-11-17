---
id: computing-software.web-development.payload-cms.payload-config-basics
name: payload-config-basics
category: computing-software
field: web-development
product: payload-cms
tags: [payload-config, buildconfig, secret, db-adapter]
level: intro
status: docs-checked
description: "Author payload.config.ts with buildConfig, including the required secret and db options and the main top-level config options."
sources:
  - https://payloadcms.com/docs/configuration/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Payload config basics

Goal: write a minimal, valid `payload.config.ts`.

```ts
import { buildConfig } from 'payload'
import { mongooseAdapter } from '@payloadcms/db-mongodb'

export default buildConfig({
  secret: process.env.PAYLOAD_SECRET,
  db: mongooseAdapter({ url: process.env.DATABASE_URL }),
  collections: [
    { slug: 'pages', fields: [{ name: 'title', type: 'text' }] },
  ],
})
```

`secret` and `db` are required. Other top-level options from the docs table: `admin`, `cli`, `editor`, `serverURL` (protocol plus domain, no path), `collections`, `globals`, `compatibility`, `cors`, `csrf`, `localization`, `logger`, `graphQL`, `cookiePrefix`, `defaultDepth`, `maxDepth`, `upload`, `routes`, `email`, `onInit`, `hooks`, `plugins`, `endpoints`, `custom`, `sharp`, `typescript`, `telemetry`.

- The config location can be customised; the CLI also honours the `PAYLOAD_CONFIG_PATH` environment variable.

Verify: `pnpm payload generate:types` loads the config without errors.

## Checked

2026-11-04. Read configuration/overview. Confirmed: the minimal config example, secret and db as the required options, the top-level option table (admin, cli, editor, serverURL without a path, collections, globals, compatibility, cors, csrf, localization, logger, graphQL, cookiePrefix, defaultDepth, maxDepth, upload, routes, email, onInit, hooks, plugins, endpoints, custom, sharp, typescript, telemetry), and PAYLOAD_CONFIG_PATH for a custom config location. Removed: the advice to keep collections in separate files (not on the page).
Method: documentation only; no commands were run.
