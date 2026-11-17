---
id: computing-software.web-development.drizzle-orm.drizzle-studio-local
name: drizzle-studio-local
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, drizzle-studio, drizzle-kit-studio, database-browser, mkcert]
level: intro
status: docs-checked
description: "Browse and edit data with drizzle-kit studio: host and port, verbose logging, Safari and Brave localhost workaround, and the license limits of Studio."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/drizzle-kit-studio.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: open Drizzle Studio against a dev database.

```sh
npx drizzle-kit studio
```

It requires database credentials in `drizzle.config.ts` (the example uses `dialect: "postgresql"` and `dbCredentials: { url }`). By default it starts a Drizzle Studio server on `127.0.0.1:4983`, with the UI hosted at local.drizzle.studio.

Options:

```sh
drizzle-kit studio --port=3000
drizzle-kit studio --host=0.0.0.0
drizzle-kit studio --host=0.0.0.0 --port=3000
drizzle-kit studio --verbose      # log every SQL statement
```

Safari and Brave block access to localhost by default: install mkcert (follow its installation steps), run `mkcert -install`, then restart `drizzle-kit studio`.

Limits stated in the docs:
- The hosted Studio is meant for local development, not for remote hosts (VPS, etc). To deploy to a VPS use Drizzle Gateway; Studio also comes as a Chrome extension for serverless database vendors and an embeddable component for your own product.
- Drizzle ORM and Drizzle Kit are fully open source; Studio is not. Studio for local development is free to use.

## Checked

Date: 2026-11-07

Confirmed against `pg/drizzle-kit-studio.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 80 lines): config requirement and example, default address, host/port options, `--verbose`, the mkcert steps, the other flavours, the limitation and the open-source answer.

Removed: the security remark about `0.0.0.0` and the invented Verify step (neither on the page).

Method: documentation only; no commands were run.
